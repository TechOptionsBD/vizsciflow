from datetime import datetime
import hashlib
import os

import json
import bleach
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from flask_login import current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
from sqlalchemy.engine import default
from sqlalchemy.orm import backref
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_

from app.exceptions import ValidationError

from . import db, login_manager
from sqlalchemy.sql.expression import desc

class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    WRITE_WORKFLOWS = 0x08
    MODERATE_COMMENTS = 0x10
    MODERATE_WORKFLOWS = 0x20
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES |
                     Permission.WRITE_WORKFLOWS, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.WRITE_WORKFLOWS |
                          Permission.MODERATE_COMMENTS |
                          Permission.MODERATE_WORKFLOWS, False),
            'Administrator': (0xff, False)
        }
        try:
            for r in roles:
                role = Role.query.filter_by(name=r).first()
                if role is None:
                    role = Role(name=r)
                role.permissions = roles[r][0]
                role.default = roles[r][1]
                db.session.add(role)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
            

    def __repr__(self):
        return '<Role %r>' % self.name


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, index=True)
    username = db.Column(db.Text, unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.Text)
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.Text)
    location = db.Column(db.Text)
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.Text)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    workflows = db.relationship('Workflow', backref='user', lazy='dynamic')
    services = db.relationship('Service', backref='user', lazy='dynamic')
    data_permissions = db.relationship('DataPermission', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password=forgery_py.lorem_ipsum.word(),
                     confirmed=True,
                     name=forgery_py.name.full_name(),
                     location=forgery_py.address.city(),
                     about_me=forgery_py.lorem_ipsum.sentence(),
                     member_since=forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                raise

    @staticmethod
    def add_self_follows():
        for user in User.query.all():
            if not user.is_following(user):
                user.follow(user)
                db.session.add(user)
                db.session.commit()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['PHENOPROC_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()
        self.followed.append(Follow(followed=self))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        return True

    def can(self, permissions):
        return self.role is not None and \
            self.role.permissions is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        return self.followed.filter_by(
            followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    @property
    def followed_posts(self):
        return Post.query.join(Follow, Follow.followed_id == Post.author_id)\
            .filter(Follow.follower_id == self.id)

    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id, _external=True),
            'username': self.username,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'posts': url_for('api.get_user_posts', id=self.id, _external=True),
            'followed_posts': url_for('api.get_user_followed_posts',
                                      id=self.id, _external=True),
            'post_count': self.posts.count()
        }
        return json_user

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
                     timestamp=forgery_py.date.date(True),
                     author=u)
            db.session.add(p)
            db.session.commit()

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        json_post = {
            'url': url_for('api.get_post', id=self.id, _external=True),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author': url_for('api.get_user', id=self.author_id,
                              _external=True),
            'comments': url_for('api.get_post_comments', id=self.id,
                                _external=True),
            'comment_count': self.comments.count()
        }
        return json_post

    @staticmethod
    def from_json(json_post):
        body = json_post.get('body')
        if body is None or body == '':
            raise ValidationError('post does not have a body')
        return Post(body=body)


db.event.listen(Post.body, 'set', Post.on_changed_body)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        json_comment = {
            'url': url_for('api.get_comment', id=self.id, _external=True),
            'post': url_for('api.get_post', id=self.post_id, _external=True),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author': url_for('api.get_user', id=self.author_id,
                              _external=True),
        }
        return json_comment

    @staticmethod
    def from_json(json_comment):
        body = json_comment.get('body')
        if body is None or body == '':
            raise ValidationError('comment does not have a body')
        return Comment(body=body)


db.event.listen(Comment.body, 'set', Comment.on_changed_body)
  
class DataSource(db.Model):
    __tablename__ = 'datasources'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    type = db.Column(db.String(30), nullable=False)
    url = db.Column(db.Text, nullable=True)
    root = db.Column(db.Text, nullable=True)
    public = db.Column(db.Text, nullable=True)
    user = db.Column(db.String(30), nullable=True)
    password = db.Column(db.String(50), nullable=True)
    prefix = db.Column(db.String(30), nullable=True)
    active = db.Column(db.Boolean, nullable=True, default=True)
    
    @staticmethod
    def insert_datasources():
        try:
            datasrc = DataSource(name='HDFS', type='hdfs', url='hdfs://206.12.102.75:54310/', root='/user', user='hadoop', password='spark#2018', public='/public', prefix='HDFS')
            db.session.add(datasrc)
            datasrc = DataSource(name='LocalFS', type='posix', url='/home/phenodoop/phenoproc/storage/', root='/', public='/public')
            db.session.add(datasrc)
            datasrc = DataSource(name='GalaxyFS', type='gfs', url='http://sr-p2irc-big8.usask.ca:8080', root='/', password='7483fa940d53add053903042c39f853a', prefix='GalaxyFS')
            db.session.add(datasrc)
            datasrc = DataSource(name='HDFS-BIG', type='hdfs', url='http://sr-p2irc-big1.usask.ca:50070', root='/user', user='hdfs', public='/public', prefix='HDFS-BIG')
            db.session.add(datasrc)
            db.session.commit()
        except:
            db.session.rollbakc()
            raise

    def __repr__(self):
        return '<DataSource %r>' % self.name


class AccessRights:
    NotSet = 0x00
    Read = 0x01
    Write = 0x02
    Owner = 0x07
    Request = 0x8
    
    @staticmethod
    def hasRight(rights, checkRight):
        if checkRight == 0:
            return rights == 0
        return (rights & checkRight) == checkRight
    
    @staticmethod
    def requested(rights):
        return AccessRights.Requested(rights, AccessRights.Request)
    
    @staticmethod
    def readRequested(rights):
        return AccessRights.Requested(rights) and (AccessRights.Requested(rights, AccessRights.Read) or AccessRights.Requested(rights, AccessRights.Write))
    
    @staticmethod
    def writeRequested(rights):
        return AccessRights.Requested(rights) and AccessRights.Requested(rights, AccessRights.Write)
    
    @staticmethod
    def rights_to_string(checkRights):
        if checkRights & AccessRights.Owner:
            return "Owner"
        
        rightStr = ""
        if checkRights & AccessRights.Request:
            rightStr = "Request"
        else:
            if checkRights & AccessRights.Read:
                rightStr = "Read"
            if checkRights & AccessRights.Write:
                rightStr += "Write"
            
        return rightStr

class AccessType:
    PUBLIC = 0
    SHARED = 1
    PRIVATE = 2
        
class Workflow(db.Model):
    __tablename__ = "workflows"
    id = db.Column(db.Integer, primary_key=True)
    #parent_id = db.Column(db.Integer, db.ForeignKey('workflows.id'), default=-1, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    modified_on = db.Column(db.DateTime, default=datetime.utcnow)
    
    name = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, default='', nullable=True)
    script = db.Column(db.Text, nullable=False)
    public = db.Column(db.Boolean, default=False)
    temp = db.Column(db.Boolean, default=False)
    derived = db.Column(db.Integer, nullable=True)
    
    accesses = db.relationship('WorkflowAccess', backref='workflow', lazy=True, cascade="all,delete-orphan") 
    runnables = db.relationship('Runnable', cascade="all,delete-orphan", backref='workflow', lazy='dynamic')
    #children = db.relationship("Workflow", cascade="all, delete-orphan", backref=db.backref("parent", remote_side=id), collection_class=attribute_mapped_collection('name'))
    
    def add_access(self, user_id, rights =  AccessRights.NotSet):
        try:
            wfAccess = WorkflowAccess(rights=rights)
            wfAccess.user_id = user_id
            self.accesses.append(wfAccess)
            db.session.commit()
            return wfAccess
        except SQLAlchemyError:
            db.session.rollback()
            raise
    
    @staticmethod
    def create(user_id, name, desc, script, access, users, temp=False, derived = 0):
        try:
            wf = Workflow()
            wf.user_id = user_id
            wf.name = name
            wf.desc = desc
            wf.script = script
            wf.public = (access == AccessType.PUBLIC)
            wf.temp = temp
            if (access == AccessType.SHARED and users):
                for username in users:
                    user = User.query.filter(User.username == username).first()
                    if user:
                        wf.accesses.append(WorkflowAccess(user_id = user.id, rights = 0x01))
            
            db.session.add(wf)
            db.session.commit()
            return wf
        except SQLAlchemyError:
            db.session.rollback()
            raise
    
    def update_script(self, script):
        try:
            self.script = script
            self.modified_on = datetime.utcnow() 
            db.session.commit()
        except:
            db.session.rollbakc()
            raise
            
    def to_json(self):
        json_post = {
            'id': self.id,
            'user': self.user.username,
            'name': self.name,
            'desc': self.desc,
            'script': self.script
        }
        return json_post
    
    def to_json_tooltip(self):
        json_post = {
            'id': self.id,
            'user': self.user.username,
            'name': self.name,
            'public': str(self.public),
            'desc': self.desc,
            'script': (self.script[:100] + '...') if len(self.script) > 100 else self.script
        }
        return json_post
    
    def to_json_info(self):
        json_post = {
            'id': self.id,
            'user': self.user.username,
            'name': self.name
        }
        return json_post
    

    @staticmethod
    def from_json(json_post):
        name = json_post.get('name')
        if name is None:
            raise ValidationError('workflow does not have a name')
        return Workflow(name=name)
    
#db.event.listen(Workflow.body, 'set', Workflow.on_changed_body)

class Param(db.Model):
    __tablename__ = 'params'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    service_id = db.Column(db.Integer, ForeignKey('services.id'))
    type = db.Column(db.Integer)
             
class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    name = db.Column(db.Text)
    internal_name = db.Column(db.Text)
    package = db.Column(db.Text)
    module = db.Column(db.Text)
    example = db.Column(JSON, nullable=True)
    desc = db.Column(db.Text)
    runmode = db.Column(db.Text)
    level = db.Column(db.Integer)
    group = db.Column(db.Text)
    returns = db.Column(db.Text)
    example2 = db.Column(JSON, nullable=True)
    
    accesses = db.relationship('ServiceAccess', backref='service', lazy=True, cascade="all,delete-orphan") #cascade="all,delete-orphan", 
    params = db.relationship('Param', backref='service', lazy=True, cascade="all,delete-orphan") #cascade="all,delete-orphan",
    
    def to_json(self):
        json_post = {
            'id': self.id,
            'user': self.user.username,
            'name': self.name,
            'desc': self.desc,
            'example': json.loads(self.example),
            'example2': json.loads(self.example2)
        }
        return json_post
    
    def to_json_info(self):
        json_post = {
            'id': self.id,
            'user': self.user.username,
            'name': self.name,
            'desc': self.desc
        }
        return json_post
    
class ServiceAccess(db.Model):
    __tablename__ = 'serviceaccesses'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, ForeignKey('services.id'))
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    rights = db.Column(db.Integer, default = 0)
    
    def hasRight(self, checkRight):
        return AccessRights.hasRight(self.rights, checkRight)
    
class WorkflowAccess(db.Model):
    __tablename__ = 'workflowaccesses'
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, ForeignKey('workflows.id'), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    rights = db.Column(db.Integer, default = 0)
    
class DataType:
    Unknown = 0x00
    Folder = 0x01
    File = 0x02
    Image = 0x04
    Video = 0x08
    Binary = 0x10
    Text = 0x20
    CSV = 0x40
    SQL = 0x80
    Custom = 0x100
    Root = 0x200
    FileList = 0x400
    FolderList = 0x800,
    Value = 0x1000
    
class DataSourceAllocation(db.Model):
    __tablename__ = 'datasource_allocations'  
    id = db.Column(db.Integer, primary_key=True)
    datasource_id = db.Column(db.Integer, db.ForeignKey('datasources.id'))
    url = db.Column(db.Text, nullable=False)
    
    visualizers = db.relationship('Visualizer', secondary = "data_visualizers")
    mimetypes = db.relationship('MimeType', secondary='data_mimetypes', lazy='dynamic')
    annotations = db.relationship('DataAnnotation', backref='datasource_allocation', lazy='dynamic')
    properties = db.relationship('DataProperty', backref='datasource_allocation', lazy='dynamic', cascade='all, delete-orphan')
    permissions = db.relationship('DataPermission', backref='datasource_allocation', lazy='dynamic', cascade='all, delete-orphan')
    
    def has_read_access(self):
        return self.has_right(AccessRights.Read)
    
    def has_write_access(self):
        return self.has_right(AccessRights.Write)
    
    @staticmethod
    def add(user_id, ds_id, url, rights):
        try:
            data = DataSourceAllocation.query.filter(and_(DataSourceAllocation.datasource_id == ds_id, DataSourceAllocation.url == url)).first()
            if not data:
                data = DataSourceAllocation()
                data.datasource_id = ds_id
                data.url = url
                db.session.add(data)
                db.session.commit()
            
            DataPermission.add(user_id, data.id, rights)
            return data
        except SQLAlchemyError:
            db.session.rollback()
            raise
    
    @staticmethod
    def get(user_id, ds_id, url):
        return DataSourceAllocation.query.join(DataPermission, DataPermission.data_id == DataSourceAllocation.id).filter(and_(DataPermission.user_id == user_id, DataSourceAllocation.datasource_id == ds_id, DataSourceAllocation.url == url)).first()

    @staticmethod
    def get_by_url(ds_id, url):
        return DataSourceAllocation.query.filter(and_(DataSourceAllocation.datasource_id == ds_id, DataSourceAllocation.url == url)).first()
        
    def has_right(self, user_id, checkRight):
        dataPermission = DataPermission.query.filter(and_(DataPermission.user_id == user_id, DataPermission.data_id == self.id)).first()
        return AccessRights.hasRight(dataPermission.rights, checkRight)
    
    @staticmethod
    def has_access_rights(user_id, path, checkRights):
        allocations = DataSourceAllocation.query.join(DataPermission, DataPermission.data_id == DataSourceAllocation.id).filter(DataPermission.user_id == user_id)
        for allocation in allocations:
            if path.startswith(allocation.url):
                for permission in allocation.permissions: 
                    if AccessRights.hasRight(permission.rights, checkRights):
                        return True
        return False

    @staticmethod
    def get_access_rights(user_id, path):
        allocations = DataSourceAllocation.query.join(DataPermission, DataPermission.data_id == DataSourceAllocation.id).filter(DataPermission.user_id == user_id)
        for allocation in allocations:
            if path.startswith(allocation.url):
                for permission in allocation.permissions:
                    return permission.rights 
        return AccessRights.NotSet
    
    @staticmethod
    def check_access_rights(user_id, path, checkRights):
        if not DataSourceAllocation.has_access_rights(user_id, path, checkRights):
            raise DataAccessError(path)
    
    @staticmethod
    def access_rights_to_string(user_id, path):
        return AccessRights.rights_to_string(DataSourceAllocation.get_access_rights(user_id, path))
    
class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    datasource_id = db.Column(db.Integer, db.ForeignKey('datasources.id'), nullable=True)
    datatype = db.Column(db.Integer)
    url = db.Column(db.Text)

class TaskStatus(db.Model):
    __tablename__ = 'taskstatus'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
            }
class Status:
    PENDING = 'PENDING'
    RECEIVED = 'RECEIVED'
    STARTED = 'STARTED'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    REVOKED = 'REVOKED'
    RETRY = 'RETRY'

class LogType:
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    runnable_id = db.Column(db.Integer, db.ForeignKey('runnables.id'))
    name = db.Column(db.Text)
    started_on = db.Column(db.DateTime, default=datetime.utcnow)
    ended_on = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Text)    
    datatype = db.Column(db.Integer)
    data = db.Column(db.Text)
    comment = db.Column(db.Text)
    
    tasklogs = db.relationship('TaskLog', cascade="all,delete-orphan", backref='task', lazy='dynamic')

    @staticmethod
    def create_task(runnable_id, name = None):
        try:
            task = Task()
            task.runnable_id = runnable_id
            task.name = name
            task.status = Status.RECEIVED
            task.tasklogs.append(TaskLog(log=Status.RECEIVED, type=LogType.INFO)) # 2 = Created
            db.session.add(task)
            db.session.commit()
            return task
        except SQLAlchemyError:
            db.session.rollback()
            raise
        
    def update(self):
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
    
    def start(self):
        try:
            self.status = Status.STARTED
            self.started_on = datetime.utcnow()
            self.add_log(Status.STARTED, LogType.INFO)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
    
    def succeeded(self, datatype, result):
        try:
            self.status = Status.SUCCESS
            self.add_log(Status.SUCCESS, LogType.INFO)
            self.ended_on = datetime.utcnow()
            self.data = result
            self.datatype = datatype
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
    
    def failed(self, log = "Task Failed."):
        try:
            self.status = Status.FAILURE
            self.datatype = DataType.Unknown
            self.add_log(log, LogType.ERROR)
            self.add_log(Status.FAILURE, LogType.INFO)        
            self.ended_on = datetime.utcnow()
            db.session.commit()            
        except SQLAlchemyError:
            db.session.rollback()
            raise
                    
    def add_log(self, log, logtype =  LogType.ERROR):
        try:
            tasklog = TaskLog(type=logtype, log = log)
            self.tasklogs.append(tasklog)
            db.session.commit()
            return tasklog
        except SQLAlchemyError:
            db.session.rollback()
            raise
        
    def to_json_log(self):
        data = self.data
        if data and data.startswith('[') and data.endswith(']'):
            data = data[1:]
            data = data[:-1]
            
        log = { 
            'name': self.name if self.name else "", 
            'datatype': self.datatype, 
            'status': self.status,
            'data': data
        }
        if self.status == Status.SUCCESS and (self.datatype & DataType.FileList) > 0:
            log['data'] = log['data'].strip('}{').split(',')
        return log
       
class TaskLog(db.Model):
    __tablename__ = 'tasklogs'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    time = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.Text, default=LogType.ERROR)
    log = db.Column(db.Text)
    
    def updateTime(self):
        try:
            self.time = datetime.utcnow()
            db.session.add(self)
        except SQLAlchemyError:
            db.session.rollback()
            raise
    
class Runnable(db.Model):
    __tablename__ = 'runnables'
    id = db.Column(db.Integer, primary_key=True)
    workflow_id  = db.Column(db.Integer, db.ForeignKey('workflows.id'), nullable=True)
    #user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    celery_id = db.Column(db.String(64))
    #name = db.Column(db.String(64))
    status = db.Column(db.String(30), default=Status.PENDING)
    script = db.Column(db.Text, nullable=False)
    arguments = db.Column(db.Text, default='')
    out = db.Column(db.Text, default='')
    err = db.Column(db.Text, default='')
    duration = db.Column(db.Integer, default = 0)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    modified_on = db.Column(db.DateTime, default=datetime.utcnow)
    
    tasks = db.relationship('Task', backref='runnable', order_by="asc(Task.id)", lazy='subquery', cascade="all,delete-orphan") 
    
    def updateTime(self):
        try:
            self.modified_on = datetime.utcnow()
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
    
    def update_status(self, status):
        try:
            self.status = status
            self.modified_on = datetime.utcnow()
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
    
    def update(self):
        try:
            self.modified_on = datetime.utcnow()
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
    
    def completed(self):
        return self.status == 'SUCCESS' or self.status == 'FAILURE' or self.status == 'REVOKED'
    
    def to_json(self):
        
        return {
            'id': self.id,
            'name': self.workflow.name,
            'script': self.script,
            'status': self.status,
            'out': self.out,
            'err': self.err,
            'duration': self.duration,
            'created_on': str(self.created_on),
            'modified_on': str(self.modified_on)
        }
    
    def to_json_tooltip(self):
        err = ""
        if err:
            err = (self.err[:60] + '...') if len(self.err) > 60 else self.err
        return {
            'id': self.id,
            'name': self.workflow.name,
            'status': self.status,
            'err': err,
            'duration': self.duration,
            'created_on': self.created_on.strftime("%d-%m-%Y %H:%M:%S") if self.created_on else '',
            'modified_on': self.modified_on.strftime("%d-%m-%Y %H:%M:%S") if self.modified_on else ''
        }
        
    def to_json_log(self):
        log = []

        for task in self.tasks:
            log.append(task.to_json_log())

        return {
            'id': self.id,
            'script': self.script,
            'status': self.status,
            'out': self.out,
            'err': self.err,
            'duration': self.duration,
            'log': log
        }
        
    def to_json_info(self):
        return {
            'id': self.id,
            'name': self.workflow.name,
            'modified': self.modified_on.strftime("%d-%m-%Y %H:%M:%S") if self.modified_on else '',
            'status': self.status
        }
        
    @staticmethod
    def create(workflow_id, script, args):
        try:
            runnable = Runnable()
            runnable.workflow_id = workflow_id
            runnable.script = script
            runnable.args = args
            runnable.status = Status.PENDING
            
            db.session.add(runnable)
            db.session.commit()
            return runnable
        except SQLAlchemyError:
            db.session.rollback()
            raise
    
    def get_user(self):
        workflow = Workflow.query.get(self.workflow_id)
        return User.query.get(workflow.user_id)

class Filter(db.Model):
    __tablename__ = 'filters'
    id = db.Column(db.Integer, primary_key=True)
    user_id  = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.Text, nullable = False)
    value = db.Column(JSON, nullable = False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    
    @staticmethod
    def add(user_id, name, value):
        try:
            filterobj = Filter()
            filterobj.user_id = user_id
            filterobj.name = name
            filterobj.value = value
            filterobj.created_on = datetime.utcnow()
            db.session.add(filterobj)
            db.session.commit()
            return filterobj
        except SQLAlchemyError:
            db.session.rollback()
            raise
    
    def name_from_value(self):
        name = ""
        for v in json.loads(self.value):
            name += v["name"] + "-"
        if name:
            name = name[:-1]
        return name
    
    def to_json_info(self):
        return {
            'id': self.id,
            'name': self.name,
            'value': self.value,
            'created_on': self.created_on.strftime("%d-%m-%Y %H:%M:%S") if self.created_on else '',
        }
        
    def to_json_tooltip(self):
        return {
            'id': self.id,
            'name': self.name_from_value(),
            'value': self.value,
            'created_on': self.created_on.strftime("%d-%m-%Y %H:%M:%S") if self.created_on else '', 
        }
        
class FilterHistory(db.Model):
    __tablename__ = 'filter_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id  = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    value = db.Column(JSON, nullable = False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    
    @staticmethod
    def add(user_id, value):
        try:
            filterobj = FilterHistory()
            filterobj.user_id = user_id
            filterobj.value = value
            filterobj.created_on = datetime.utcnow()
            
            db.session.add(filterobj)
            db.session.commit()
            return filterobj
        except SQLAlchemyError:
            db.session.rollback()
            raise
    
    def name_from_value(self):
        name = ""
        for v in json.loads(self.value):
            name += v["name"] + "-"
        if name:
            name = name[:-1]
        return name
    
    def to_json_info(self):
        return {
            'id': self.id,
            'name': self.name_from_value(),
            'value': self.value,
            'created_on': self.created_on.strftime("%d-%m-%Y %H:%M:%S") if self.created_on else '',
        }
        
    def to_json_tooltip(self):
        return {
            'id': self.id,
            'name': self.name_from_value(),
            'value': self.value,
            'created_on': self.created_on.strftime("%d-%m-%Y %H:%M:%S") if self.created_on else '', 
        }
        
        
class DataPermission(db.Model):
    __tablename__ = 'data_permissions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    data_id  = db.Column(db.Integer, db.ForeignKey('datasource_allocations.id'))
    rights = db.Column(db.Integer, default = 0)
    
    @staticmethod
    def add(user_id, data_id, rights):
        try:
            permission = DataPermission.query.filter(and_(DataPermission.user_id == user_id, DataPermission.data_id == data_id)).first()
            if not permission:
                permission = DataPermission()
                permission.user_id = user_id
                permission.data_id = data_id
                db.session.add(permission)
            elif permission.rights == rights:
                return permission
                
            permission.rights = rights

            db.session.commit()
            return permission
        except SQLAlchemyError:
            db.session.rollback()
            raise
        
class DataAnnotation(db.Model):
    __tablename__ = 'data_annotations'
    id = db.Column(db.Integer, primary_key=True)
    data_id  = db.Column(db.Integer, db.ForeignKey('datasource_allocations.id'), nullable=True)
    tag = db.Column(db.Text, nullable = False)
    
    @staticmethod
    def add(data_id, tag):
        try:
            annotation = DataAnnotation.query.filter_by(data_id = data_id).first()
            if not annotation:            
                annotation = DataAnnotation()
                annotation.data_id = data_id
                db.session.add(annotation)
            elif annotation.tag == tag:
                return annotation
                
            annotation.tag = tag
            
            db.session.commit()
            return annotation
        except SQLAlchemyError:
            db.session.rollback()
            raise

class DataProperty(db.Model):
    __tablename__ = 'data_properties'
    id = db.Column(db.Integer, primary_key=True)
    data_id  = db.Column(db.Integer, db.ForeignKey('datasource_allocations.id'), nullable=True)
    key = db.Column(db.Text, nullable = False)
    value = db.Column(JSON, nullable = False)
    
    @staticmethod
    def add(data_id, key, value):
        try:
            dataproperty = DataProperty.query.filter(and_(DataProperty.data_id == data_id, DataProperty.key == key)).first()
            if not dataproperty:            
                dataproperty = DataProperty()
                dataproperty.data_id = data_id
                dataproperty.key = key
                db.session.add(dataproperty)
            elif dataproperty.value == value:
                return property
            
            dataproperty.value = value
            
            db.session.commit()
            return dataproperty
        except SQLAlchemyError:
            db.session.rollback()
            raise
    
    @staticmethod
    def add_key_value(data_id, key, value, datatype = DataType.Text):
        return DataProperty.add(data_id, {key: value}, datatype)      
                    
class Visualizer(db.Model):
    __tablename__ = 'visualizers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable = False)
    desc = db.Column(db.Text, nullable = True)
    
    dataAllocations = db.relationship("DataSourceAllocation", secondary="data_visualizers")
    
    @staticmethod
    def add(name, desc):
        try:
            visualizer = Visualizer.query.filter_by(name = name).first()
            if not visualizer:            
                visualizer = Visualizer()
                visualizer.name = name
                db.session.add(visualizer)
            elif visualizer.desc == desc:
                    return visualizer
            
            visualizer.desc = desc
            
            db.session.commit()
            return visualizer
        except SQLAlchemyError:
            db.session.rollback()
            raise
    
    
class DataVisualizer(db.Model):
    __tablename__ = 'data_visualizers'
    id = db.Column(db.Integer, primary_key=True)
    data_id  = db.Column(db.Integer, db.ForeignKey('datasource_allocations.id'), nullable=False)
    visualizer_id  = db.Column(db.Integer, db.ForeignKey('visualizers.id'), nullable=False)
    
    dataAllocation = db.relationship(DataSourceAllocation, backref=backref("data_visualizers", cascade="all, delete-orphan"))
    visualizer = db.relationship(Visualizer, backref=backref("data_visualizers", cascade="all, delete-orphan"))
    
    @staticmethod
    def add(data_id, visualizer_id):
        try:
            dataVisualizer = DataVisualizer.query.filter(and_(DataVisualizer.data_id == data_id, DataVisualizer.visualizer_id == visualizer_id)).first() 
            if dataVisualizer:
                return dataVisualizer
            
            dataVisualizer = DataVisualizer()
            dataVisualizer.data_id = data_id
            dataVisualizer.visualizer_id = visualizer_id
            
            db.session.add(dataVisualizer)
            db.session.commit()
            return dataVisualizer
        except SQLAlchemyError:
            db.session.rollback()
            raise
        
class MimeType(db.Model):
    __tablename__ = 'mimetypes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable = False)
    desc = db.Column(db.Text, nullable = True)
    
    dataAllocations = db.relationship("DataSourceAllocation", secondary="data_mimetypes")
    
    @staticmethod
    def add(name, desc):
        try:
            mimetype = MimeType.query.filter_by(name = name).first()
            if not mimetype:            
                mimetype = MimeType()
                mimetype.name = name
                db.session.add(mimetype)                
            elif mimetype.desc == desc:
                return mimetype
            
            mimetype.desc = desc

            db.session.commit()
            return mimetype
        except SQLAlchemyError:
            db.session.rollback()
            raise

class DataMimeType(db.Model):
    __tablename__ = 'data_mimetypes'
    id = db.Column(db.Integer, primary_key=True)
    data_id  = db.Column(db.Integer, db.ForeignKey('datasource_allocations.id'), nullable=False)
    mimetype_id  = db.Column(db.Integer, db.ForeignKey('mimetypes.id'), nullable=False)
    
    dataAllocation = db.relationship(DataSourceAllocation, backref=backref("data_mimetypes", cascade="all, delete-orphan"))
    mimetype = db.relationship(MimeType, backref=backref("data_mimetypes", cascade="all, delete-orphan"))
    
    @staticmethod
    def add(data_id, mimetype_id):
        try:
            dataMimeType = DataMimeType.query.filter(and_(DataMimeType.data_id == data_id, DataMimeType.mimetype_id == mimetype_id)).first() 
            if dataMimeType:
                return dataMimeType
            
            dataMimeType = DataMimeType()
            dataMimeType.data_id = data_id
            dataMimeType.mimetype_id = mimetype_id
            
            db.session.add(dataMimeType)
            db.session.commit()
            return dataMimeType
        except SQLAlchemyError:
            db.session.rollback()
            raise
        
class DataAccessError(Exception):
    def __init__(self, url):

        # Call the base class constructor with the parameters it needs
        super().__init__("You do not have access rights for this path: " + url)