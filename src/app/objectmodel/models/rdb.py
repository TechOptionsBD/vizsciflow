from datetime import datetime
import hashlib
import os
import io
import json
import bleach
import logging
from flask import current_app, request, url_for
from flask_login import UserMixin

from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from markdown import markdown
from sqlalchemy.orm import backref
from sqlalchemy.sql import exists
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, or_, cast
from sqlalchemy.types import Unicode
from sqlalchemy import func
from sqlalchemy.ext.declarative import DeclarativeMeta
from app.exceptions import ValidationError

from app import db
from dsl.datatype import DataType
from sqlalchemy.orm.attributes import flag_modified
from app.objectmodel.common import Permission, AccessRights, AccessType, Status, LogType, git_access, ActivityType
from .loader import Loader

from collections import namedtuple
     
class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields
    
        return json.JSONEncoder.default(self, obj)

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
    confirmed = db.Column(db.Boolean, default=True)
    name = db.Column(db.Text)
    location = db.Column(db.Text)
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.Text)
    oid = db.Column(db.Integer, default=0, nullable=True)

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

    def verify_and_update_password(self, oldpassword, password):
        if not check_password_hash(self.password_hash, oldpassword):
            return False
        self.password = password
        db.session.add(self)
        return True


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
        
        hash = None
        if self.email:
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
        #return '%r , %i' %(self.username, self.id)
        #return "<User(id='%s', username='%s')>" %(self.id, self.username)
        #'{'id' : self.id, 'username' : self.username}' #

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
    prefix = db.Column(db.Text, nullable=True)
    active = db.Column(db.Boolean, nullable=True, default=True)
    temp = db.Column(db.Text, nullable=True)
    
    @staticmethod
    def insert_datasources():
        try:
            datasources = Loader.get_datasources()
            datasourceitems = []
            for datasrc in datasources:
                datasourceitem = DataSource(**datasrc)
                datasourceitems.append(datasourceitem)
            
            db.session.add_all(datasourceitems)
            db.session.commit()
            return datasourceitems
        except:
            db.session.rollback()
            raise

    def __repr__(self):
        return '<DataSource %r>' % self.name
    
    def to_json(self):
        try:
            from app.util import Utility
            fs = Utility.create_fs(self)
            return {
                    'id': self.id if self.id else "",
                    'title': self.name if self.name else "",
                    'url': fs.strip_root(self.url) if self.url else "",
                    'type': self.type if self.type else "",
                    #'root': self.root if self.root else "",
                    'public': self.public if self.public else "",
                    'user': self.user if self.user else "",
                    'password': self.password if self.password else "",
                    'active': str(self.active) if self.active else "False",
                    'user': self.temp if self.temp else "",
                    'group': ""
                }
        except:
            logging.error(f"Cannot connect to the file system {self.name}")
            raise
        
    @staticmethod
    def add_item_in_list_view(selected_items, count,floor,celling, items, has_more, selected_item_ids, restricted_items, user_id, filtered_items=None):
        #error will not handle in helper method
        for each_item in selected_items:
            try:
                if each_item.id not in selected_item_ids and each_item.id not in restricted_items:
                    count += 1
                    if count > floor and count <= celling:
                        items['data'].append(each_item.to_json())
                    if count > celling :
                        has_more = True
                    selected_item_ids.append(each_item.id)
                    if filtered_items is not None and filtered_items != []:
                        filtered_items.remove(each_item.id)
            except:
                pass
        return items, count, has_more, selected_item_ids, filtered_items
    
    @staticmethod
    def get_child_details_for_plugin(parent, child, data_dir):
        fullPath = child
        if parent != '-1':
            fullPath = os.path.join(parent, child)

        if os.path.isdir(os.path.join(data_dir, child)):
            is_child = True if os.path.isdir(os.path.join(data_dir, child)) else False
            data_json = {
                'id': fullPath,
                'text': child,
                'children': is_child,
                'type': 'folder'
            }
        else:
            dir_name,base_name = os.path.split(fullPath)
            data_json = {
                'id': fullPath,
                'text': child,
                'children': False,
                'type': 'file'
            }
        return data_json
    
    @staticmethod
    def load_dataset_data_for_plugin(user_id, dataset_id, data_id, page=1, no_of_item=10):
        try:
            count = 0
            has_more = False
            dataset_details = {}
            all_data = []
            celling = page * no_of_item
            floor = (page - 1) * no_of_item
            datasource = DataSource.query.get(dataset_id)
            data_dir = os.path.join(datasource.url, data_id) if data_id != '-1' else datasource.url
            users_dir = os.path.join(datasource.url, 'users')

            user = User.query.get(user_id) if data_dir == users_dir else None
            for f in os.listdir(data_dir):
                if f.startswith('T_'): continue
                if user and f != user.username: continue
                if not os.path.exists(os.path.join(data_dir, f)):
                    try:
                        os.makedirs(os.path.join(data_dir, f))
                    except Exception as e:
                        logging.error(f"Cannot add user folder for error:{str(e)}")
                all_data.append(f)

            root_childrens = []
            for each_data in all_data:
                count += 1
                if count > floor and count <= celling:
                    data_details = DataSource.get_child_details_for_plugin(data_id, each_data, data_dir)
                    root_childrens.append(data_details) 
                if count > celling :
                    has_more = True
                    break

            if data_id == '-1' and page == '1':
                dataset_details['nodes'] = {"id": "", "text":"Root node", "children": root_childrens}
            else:
                dataset_details['nodes'] = root_childrens

            dataset_details["loadNodeId"] = "#>" + str(dataset_id) if data_id == '-1' else str(data_id) + ">" + str(dataset_id)
            dataset_details['hasMore'] = has_more
            dataset_details['pageNum'] = page
            dataset_details['itemCount'] = len(all_data)

            return dataset_details

        except Exception as e:
            logging.error(f"Exception thrown while loading dataset from the storage: {str(e)}")
            raise
           
    @staticmethod
    def load_listview_datasets(user_id: int, page: int, no_of_item: int):
        count = 0
        has_more = False
        selected_dataset_ids = []
        
        celling = page * no_of_item
        floor = (page - 1) * no_of_item
        datasets = {"data": [], "pageNum": page}
        
        datasources = DataSource.query.filter_by(active = True)
        logging.info(datasources.count())
        # restricted_items = DatasetUtility.access_restricted_of_dataset(my_groups, child_groups, selected_datasets)
        datasets,count,has_more, selected_dataset_ids, filtered_datasets = DataSource.add_item_in_list_view(datasources, 
                                                        count, floor, celling, datasets, has_more, 
                                                        selected_dataset_ids, [], user_id, [])


        datasets['hasMore'] = has_more
        datasets['itemCount'] = count
        if filtered_datasets!=None:
            datasets['dataset_ids'] = selected_dataset_ids
        
        return datasets

class Dataset(db.Model):
    __tablename__ = 'datasets'
    id = db.Column(db.Integer, primary_key=True)
    schema = db.Column(JSON, nullable = False)
    
    @staticmethod
    def add(schema):
        try:
            dataset = Dataset()
            dataset.schema = schema
            db.session.add(dataset)
            db.session.commit()
            return dataset
        except SQLAlchemyError:
            db.session.rollback()
            raise
    
    @staticmethod
    def remove(dataset_id):
        try:
            Dataset.query.filter_by(id = dataset_id).delete()
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
        
    @staticmethod
    def update(dataset_id, schema):
        try:
            dataset = Dataset.query.get(dataset_id)
            dataset.schema = schema
            db.session.commit()
            return dataset
        except SQLAlchemyError:
            db.session.rollback()
            raise
            
    def to_json(self):
        json_post = {
            'id': self.id,
            'schema': self.schema
        }
        return json_post
        
    def __repr__(self):
        return '<Dataset %r>' % self.id
          
class Workflow(db.Model):
    __tablename__ = "workflows"
    id = db.Column(db.Integer, primary_key=True)
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
    annotations = db.relationship('WorkflowAnnotation', backref='workflow', lazy='dynamic', cascade="all,delete-orphan")
    params = db.relationship('WorkflowParam', backref='workflow', lazy='dynamic', cascade="all,delete-orphan") #cascade="all,delete-orphan",
    returns = db.relationship('WorkflowReturn', backref='workflow', lazy='dynamic', cascade="all,delete-orphan")
    
    def can_remove(self, user_id):
        if self.public or self.user_id != user_id:
            return False
        q = WorkflowAccess.query.filter(WorkflowAccess.workflow_id == self.id, WorkflowAccess.user_id != user_id, WorkflowAccess.rights != AccessRights.NotSet)
        return not q or q.count() == 0

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
    def get_returns_json(workflow_id):
        workflow = Workflow.query.get(workflow_id)
        if workflow and workflow.returns:
            return [ret.value for ret in workflow.returns]
        return []

    @staticmethod
    def insert_workflows(path):
        admin = User.query.filter(User.username=='admin').first()
        samples = Loader.load_samples_recursive(path)
        for sample in samples:
            if isinstance(sample["script"], list):
                sample["script"] = "\n".join(sample["script"])
            if admin and "user_id" not in sample:
                sample["user_id"] = admin.id

        return [Workflow.create(**s) for s in samples]

    def update_accesses(self, users):
        if isinstance(users, str):
            users = users.strip()
            if not users:
                return
            users = list(users.split(","))
        if not users:
            return
        for user_id in users:
            user = User.query.get(user_id)
            if user:
                self.accesses.append(WorkflowAccess(user_id = user.id, rights = AccessRights.Read))
                    
    @staticmethod
    def create(**kwargs):
        try:
            access = int(kwargs.pop('access', 0))
            users = kwargs.pop('users', None)
            paramargs = kwargs.pop('params', [])
            returnsargs = kwargs.pop('returns', [])

            wf = Workflow(**kwargs)
            wf.public = (access == AccessType.PUBLIC)
            if users and access == AccessType.SHARED:
                wf.update_accesses(access, users)

            wf.update(params=paramargs, returns=returnsargs)
            db.session.add(wf)
            db.session.commit()
            
            if git_access():
                # save the script in workflows folder for git version
                try:
                    with open(wf.scriptpath, "w+") as f:
                        f.write(kwargs['script'])
                        git_access().git.add(wf.scriptpath)
                        git_access().git.commit('-m', 'create workflow ' + str(wf.id))
                except Exception as e:
                    logging.error("Git error: " + e)
            
            return wf
        except SQLAlchemyError:
            db.session.rollback()
            raise
    
    def update(self, **kwargs):
        if 'access' in kwargs:
            access = int(kwargs['access'])
            self.public = (access == AccessType.PUBLIC)
            
        if 'users' in kwargs and not self.public:
            self.update_accesses(kwargs['users'])

        if 'user_id' in kwargs:
            self.user_id = kwargs['user_id']
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'desc' in kwargs:
            self.desc = kwargs['desc']
        if 'script' in kwargs:
            self.update_script(kwargs['script'])
        if 'temp' in kwargs:
            self.temp = kwargs['temp']
        if 'derived' in kwargs:
            self.derived = kwargs['derived']
        
        if 'params' in kwargs:
            params = kwargs['params']
            if isinstance(params, str):
                params = json.loads(params)
            self.params = [WorkflowParam(value = p) for p in params] if params else []
        
        if 'returns' in kwargs:
            returns = kwargs['returns']
            if isinstance(returns, str):
                returns = json.loads(returns)
            self.returns = [WorkflowReturn(value = r) for r in returns] if returns else []
        
        return self

    def isEqual(self, **kwargs):
        if 'script' in kwargs:
            if self.script != kwargs['script']:
                return False
        
        if 'params' in kwargs:
            params = kwargs['params']
            if isinstance(params, str):
                params = json.loads(params)
            if params and not self.params:
                return False
            if not params and self.params and self.params.count():
                return False
            if params.length != self.params.count():
                return False
            for i in range(0, params.length):
                if params[i] != self.params[0].value:
                    return False
        
        if 'returns' in kwargs:
            returns = kwargs['returns']
            if isinstance(returns, str):
                returns = json.loads(returns)
            if returns and not self.returns:
                return False
            if not returns and self.returns and self.returns.count():
                return False
            if returns.length != self.returns.count():
                return False
            for i in range(0, returns.length):
                if returns[i] != self.returns[0].value:
                    return False
                
        return True
            
        
    @staticmethod
    def add(user_id, value, access, users):
        try:
            service = Service()
            service.user_id = user_id
            service.active = True
            service.public = True if access == AccessType.PUBLIC else False

            if (access == AccessType.SHARED and users):
                for user_id in users:
    #                 for usr in user:
    #                     print(usr)
    #                     user_id, rights = usr.split(":")
                    matchuser = User.query.get(user_id)
                    if matchuser:
                        service.accesses.append(ServiceAccess(user_id = matchuser.id, rights = 0x01))

            service.update(value)

            db.session.add(service)
            db.session.commit()
            return service
        except SQLAlchemyError:
            db.session.rollback()
            raise

    @staticmethod
    def remove(current_user_id, workflow_id):
        try:
            #Workflow.query.filter(and_(Workflow.id == workflow_id, Workflow.user_id == current_user_id)).delete()
            db.session.delete(Workflow.query.filter(and_(Workflow.id == workflow_id, Workflow.user_id == current_user_id)).first())
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise

    @staticmethod
    def commit_changes(branch = 'master', message='update' ):
        has_changed = False
        if git_access().is_dirty():
            for file in git_access().git.diff(None, name_only=True).split('\n'):
                git_access().git.add(file)
                if not has_changed:
                    has_changed = True

        if has_changed:
            git_access().git.commit('-m', message)
            #git_access().git.push('origin', branch) # if you have remote repository too
                
    def git_write(self, script):
        if git_access():
            with open(self.scriptpath, 'w') as f:
                f.write(script)
            return Workflow.commit_changes()
            #g = git.cmd.Git(app.config['WORKFLOW_VERSIONS_DIR'])
            #if not g.ls_files(str(self.id)):
            
#             git_access().git.add(str(self.id))
#             return git_access().git.commit('-m', 'update script')
                
    def update_script(self, script):
        if self.script == script:
            return True                       
        try:
            self.script = script
            self.modified_on = datetime.utcnow() 
            db.session.commit()
            
            try:
                self.git_write(script)
            except Exception as e:
                logging.error("Git error while updating workflow: " + e.message)
        except:
            db.session.rollback()
            raise
    
    @property
    def scriptpath(self):
        from app import app
        return os.path.join(app.config['WORKFLOW_VERSIONS_DIR'], str(self.id))
    
    @property                        
    def revisions(self):
        from app import app
        revisions = []
        if not git_access():
            return revisions
        commits = list(git_access().iter_commits(paths=app.config['WORKFLOW_VERSIONS_DIR']))
        for c in commits:
            try:
                f = c.tree / str(self.id)
                revision = {
                    'hex': f.hexsha,
                    'summary': c.summary,
                    'committer': c.committer.name,
                    'time': str(c.committed_datetime)
                    }
                revisions.append(revision)
            except Exception as e:
                logging.error("Git error in revisions: " + e.message)

        if revisions:
            return revisions
        if app.config['USE_GIT']:
            self.git_write(self.script)
        return self.revision()
    
    def revision_by_commit(self, hexsha):
        from app import app

        if not git_access():
            return self.script
        commits = list(git_access().iter_commits(paths=app.config['WORKFLOW_VERSIONS_DIR']))
        for c in commits:
            try:
                f = c.tree / str(self.id)
                if f.hexsha != hexsha:
                    continue
                with io.BytesIO(f.data_stream.read()) as fd:
                    return fd.read().decode('utf-8')
            except:
                pass

    def get_access_for_user(self, user_id):
        if self.public:
            return 0
        if self.user_id == user_id:
            q = WorkflowAccess.query.filter(WorkflowAccess.workflow_id == self.id, WorkflowAccess.user_id != user_id, WorkflowAccess.rights != AccessRights.NotSet)
            return 1 if  q and q.count() else 2
        else:
            q = WorkflowAccess.query.filter(WorkflowAccess.workflow_id == self.id, WorkflowAccess.user_id == user_id, WorkflowAccess.rights != AccessRights.NotSet)
            return 1 if  q and q.count() else 2

    def to_json(self):
        json_post = {
            'id': self.id,
            'user': self.user.username,
            'name': self.name,
            'desc': self.desc,
            'script': self.script,
            'public': self.public
        }
        json_post.update(Service.get_params_returns_json(self))
        return json_post
    
    def to_json_tooltip(self):
        json_post = {
            'id': self.id,
            'user': self.user.username,
            'name': self.name,
            'public': str(self.public),
            'desc': self.desc
            #'script': (self.script[:100] + '...') if len(self.script) > 100 else self.script
        }
        return json_post
    
    def to_json_info(self):
        json_post = {
            'id': self.id,
            'user': self.user.username,
            'name': self.name,
        }
        return json_post
    

    @staticmethod
    def from_json(json_post):
        name = json_post.get('name')
        if name is None:
            raise ValidationError('workflow does not have a name')
        return Workflow(name=name)   
    
#db.event.listen(Workflow.body, 'set', Workflow.on_changed_body)

class WorkflowAccess(db.Model):
    __tablename__ = 'workflowaccesses'
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, ForeignKey('workflows.id'), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    rights = db.Column(db.Integer, default = 0)
        
    def remove(Workflowed_id):
        try:
            WorkflowAccess.query.filter(WorkflowAccess.workflow_id == Workflowed_id).delete()
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
        
    def check(Workflowed_id):
        try:
            val = db.session.query(exists().where(WorkflowAccess.workflow_id == Workflowed_id)).scalar()
            if val:
                return True 
            else:
                return False
        except SQLAlchemyError:
            db.session.rollback()
            raise  
     
class WorkflowParam(db.Model):
    __tablename__ = 'workflowparams'
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, ForeignKey('workflows.id'))
    value = db.Column(JSON, nullable = False)

class WorkflowReturn(db.Model):
    __tablename__ = 'workflowreturns'
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, ForeignKey('workflows.id'))
    value = db.Column(JSON, nullable = False)

class RunnableArg(db.Model):
    __tablename__ = 'runnableargs'
    id = db.Column(db.Integer, primary_key=True)
    runnable_id = db.Column(db.Integer, ForeignKey('runnables.id'))
    value = db.Column(JSON, nullable = False)

class RunnableReturn(db.Model):
    __tablename__ = 'runnablereturns'
    id = db.Column(db.Integer, primary_key=True)
    runnable_id = db.Column(db.Integer, ForeignKey('runnables.id'))
    value = db.Column(JSON, nullable = False)

class Param(db.Model):
    __tablename__ = 'params'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, ForeignKey('services.id'))
    value = db.Column(JSON, nullable = False)
    
    #service = db.relationship("Service", foreign_keys=service_id)

class Return(db.Model):
    __tablename__ = 'returns'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, ForeignKey('services.id'))
    value = db.Column(JSON, nullable = False)

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    value = db.Column(JSON, nullable = False)
    public = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    pipenv = db.Column(db.Text, nullable = True)
    pippkgs = db.Column(db.Text, nullable = True)
    reqfile = db.Column(db.Text, nullable = True)
    #accesses = db.relationship('ServiceAccess', backref='service', lazy=True, cascade="all,delete-orphan") #cascade="all,delete-orphan", 
    accesses = db.relationship('ServiceAccess', backref='service', cascade="all,delete-orphan") #cascade="all,delete-orphan",
    params = db.relationship('Param', backref='service', lazy='dynamic', cascade="all,delete-orphan") #cascade="all,delete-orphan",
    returns = db.relationship('Return', backref='service', lazy='dynamic', cascade="all,delete-orphan")
    tasks = db.relationship('Task', cascade="all,delete-orphan", backref='service', lazy='dynamic')

    @staticmethod
    def insert_module(f):
        try:
            admin = User.query.filter(User.username == "admin").first()

            service = None
            user_id = f.pop("user_id", None)
            if not user_id and admin:
                user_id = admin.id
            
            service = Service.get_service_by_name_package(f["name"], f["package"]).first()
            if service:
                if service.user_id == user_id or user_id == admin.id:
                    service.update(f)
                    logging.info("Module {0} is updated.".format(f["name"]))
                else:
                    logging.error("Module {0} already exists.".format(f["name"]))
            else:
                service = Service.add(user_id, f, AccessType.PUBLIC, None)
                logging.info("Module {0} is added.".format(f["name"]))

            db.session.commit()
            return service
        except SQLAlchemyError:
            db.session.rollback()
            raise

    @staticmethod
    def insert_modules(funclist, user_id = None):
        try:
            admin = User.query.filter(User.username == "admin").first()

            modules = []
            for f in funclist:
                if not user_id and admin:
                    user_id = admin.id
                
                service = Service.get_service_by_name_package(f["name"], f["package"]).first()
                if service:
                    if service.user_id == user_id or user_id == admin.id:
                        service.update(f)
                        modules.append(service)
                        logging.info("Module {0} is updated.".format(f["name"]))
                    else:
                        logging.error("Module {0} already exists.".format(f["name"]))
                else:
                    modules.append(Service.add(user_id, f, AccessType.PUBLIC, None))
                    logging.info("Module {0} is added.".format(f["name"]))

            db.session.commit()
            return modules
        except SQLAlchemyError:
            db.session.rollback()
            raise
    
    def update(self, value):

        Param.query.filter(Param.service_id==self.id).delete()
        Return.query.filter(Return.service_id==self.id).delete()
        db.session.commit()

        params = value.pop('params', [])
        for p in params:
            self.params.append(Param(value = p))
        
        returns = value.pop('returns', [])
        for p in returns:
            self.returns.append(Return(value = p))

        self.value = value

    @staticmethod
    def add(user_id, value, access, users, pipenv='', pippkgs='', reqfile=''):
        try:
            service = Service()
            service.user_id = user_id
            service.active = True
            service.public = (access == AccessType.PUBLIC)

            if (access == AccessType.SHARED and users):
                for user_id in users:
    #                 for usr in user:
    #                     print(usr)
    #                     user_id, rights = usr.split(":")
                    matchuser = User.query.filter(User.id == user_id).first()
                    if matchuser:
                        service.accesses.append(ServiceAccess(user_id = matchuser.id, rights = 0x01))

            service.pipenv = pipenv
            service.pippkgs = pippkgs
            service.reqfile = reqfile
            service.update(value)

            db.session.add(service)
            db.session.commit()
            return service
        except SQLAlchemyError:
            db.session.rollback()
            raise
        
    @staticmethod
    def add_users(service_id, users):
        try:
            service =  Service.query.filter(Service.id == service_id)
            if users:
                for user_id in users:
                    user = User.query.filter(User.id == user_id).first()
                    if user:
                        service.accesses.append(ServiceAccess(user_id = user.id, rights = 0x01))

        except SQLAlchemyError:
            db.session.rollback
    
    def remove(current_user_id, service_id):
        try:
            #Service.query.filter(and_(Service.id == service_id, Service.user_id == current_user_id)).delete()
            db.session.delete(Service.query.filter(and_(Service.id == service_id, Service.user_id == current_user_id)).first())
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
    
    def to_json_info(self):
        json_post = {
            'id': self.id,
            'user': self.user.username if self.user else "",
            'package': self.value["package"] if "package" in self.value else "",
            'name': self.value["name"],
            'desc': self.value["desc"]
        }
        return json_post
   
    @staticmethod
    def get_first_service_by_name_package(name, package = None):
        return Service.get_service_by_name_package(name, package).first()
    
    @staticmethod
    def get_first_service_by_name_package_json(name, package = None):
        service = Service.get_first_service_by_name_package(name, package)
        if service and service.value:
            value = service.value
            value.update(Service.get_params_returns_json(service))
            return value

    @staticmethod
    def get_service_by_name_package(name, package = None):
#         if package:
#             return Service.query.filter(and_(func.lower(Service.value["name"].astext).cast(Unicode) == name.lower(), func.lower(Service.value["package"].astext).cast(Unicode) == package.lower()))
#         else:
#             return Service.query.filter(func.lower(Service.value["name"].astext).cast(Unicode) == name.lower())
        
        return Service.query.filter(and_(func.lower(Service.value["name"].astext).cast(Unicode) == name.lower(), not package or func.lower(Service.value["package"].astext).cast(Unicode) == package.lower()))
    
    # @staticmethod
    # def add_access_to_json(id, services, access, is_owner, accesses):
    #     i=0
    #     for s in services:
    #         s['access'] = access
    #         s['service_id'] =  id[i]
    #         s['is_owner'] = is_owner[i]
    #         if accesses[i] != []:
    #             sharedWith = ServiceAccess.get_by_service_id(id[i])
    #             #ServiceAccess.query.filter(ServiceAccess.service_id == id[i]).with_entities(ServiceAccess.id, ServiceAccess.user_id)
    #             s['sharedWith'] = sharedWith
            
    #         i+=1
            
    #     return services

    @staticmethod
    def get_access_json(id, access, is_owner):
        return {
            'access': access,
            'service_id':  id,
            'is_owner': is_owner,
            'shared_with':  ServiceAccess.get_by_service_id(id)
        }

    @staticmethod
    def get_params_returns_json(service):
        result = { 'params': [], 'returns': [] }
        if service:
            if service.params:
                result['params'] = [param.value for param in service.params]
            
            if service.returns:
                result['returns'] = [param.value for param in service.returns]
                
        return result

    @staticmethod
    def get_full_user_json(service, user_id, access):
        json = service.value
        json.update(Service.get_params_returns_json(service))
        json.update(Service.get_access_json(service.id, access, service.user_id == user_id))
        return json

    @staticmethod
    def get_full_by_user_json(user_id, access):
        samples = []
        if access == 0 or access == 3:
            services = Service.query.filter(and_(Service.public == True, Service.active == True))
            samples = [Service.get_full_user_json(s, user_id, 0) for s in services]
        if access == 1 or access == 3:
            services = Service.query.filter(and_(Service.public != True, Service.active == True)).filter(Service.accesses.any(and_(ServiceAccess.user_id == user_id, Service.user_id != user_id)))
            samples.extend([Service.get_full_user_json(s, user_id, 1) for s in services])
        if access == 2 or access == 3:
            services = Service.query.filter(and_(Service.public != True, Service.active == True, Service.user_id == user_id))
            samples.extend([Service.get_full_user_json(s, user_id, 2) for s in services])

        return samples
        
    @staticmethod
    def get_module_by_name_package_for_user_access_json(user_id, name, package = None):
        service = Service.get_service_by_name_package(name, package).first()
        if service:
            value = service.value
            value.update(Service.get_params_returns_json(service))
            if service.public:
                value["access"] = "public"
            else:
                if service.user_id == user_id:
                    value["access"] = "private" # user_id is the owner
                for access in service.accesses:
                    if access.user_id == user_id:
                        value["access"] = "shared" if service.user_id != user_id else "private"
                        break
            return value


    @staticmethod
    def check_function(name, package = None):
        services = Service.get_service_by_name_package(name, package)
        return services and services.count() > 0
                
    @staticmethod
    def get_by_user1(username, access):
        #fields = ['name', 'addr', 'phone', 'url']
        #companies = session.query(SomeModel).options(load_only(*fields)).all()
        #session.query(SomeModel.col1.label('some alias name'))
        #return Service.query.options(db.joinedload(Service.accesses))
        #Service.query.all().join(Service.accesses).filter_by(user_id == username)
        #Service.query.filter(Service.accesses.contains())
        q1 = []
        if access == 0 or access == 3:
            q1 = Service.query.filter(and_(Service.public == True, Service.active == True))
        if access > 0: 
            q2 = Service.query.join(Service.accesses).join(ServiceAccess.user).filter(and_(Service.public == False, Service.active == True, User.username == username, or_(access == 3, ServiceAccess.rights == rights )))
        q1list = [q for q in q1]
        q1list.extend([q for q in q2])
        return q1list
    
    @staticmethod
    def update_access(service_id, access):
        try:
            service = Service.query.filter(Service.id == service_id).first()
            service.public = access
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise

    @property
    def package(self):
        return self.value["package"]
    
    @property
    def name(self):
        return self.value["name"]

class ServiceAccess(db.Model):
    __tablename__ = 'serviceaccesses'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, ForeignKey('services.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    rights = db.Column(db.Integer, default = 0)
    
    user = db.relationship("User", foreign_keys=user_id)
    #service = db.relationship("Service", backref=backref("serviceaccesses", cascade="all, delete-orphan"))

    @staticmethod
    def add(service_id, users):
        try:
            for user in users:
                serviceaccess = ServiceAccess()
                serviceaccess.service_id = str(service_id)
                serviceaccess.user_id = str(user)
                serviceaccess.rights = 0x01
        
                db.session.add(serviceaccess)
            db.session.commit()
            return serviceaccess
        except SQLAlchemyError:
            db.session.rollback()
            raise
        
    def get_by_service_id(service_id):
        try:
            shared = ServiceAccess.query.filter(ServiceAccess.service_id == service_id).with_entities(ServiceAccess.id, ServiceAccess.user_id)
            shared_user = json.dumps([r.user_id for r in shared], cls=AlchemyEncoder)
            return shared_user
        except SQLAlchemyError:
            db.session.rollback()
            raise

    @staticmethod
    def get(self, **kwargs):
        try:
            shared = Service.query.filter_by(**kwargs).with_entities(ServiceAccess.id, ServiceAccess.user_id)
            shared_user = json.dumps([r.user_id for r in shared], cls=AlchemyEncoder)
            return shared_user
        except SQLAlchemyError:
            db.session.rollback()
            raise

        
    
    def remove(serviced_id):
        try:
            ServiceAccess.query.filter(ServiceAccess.service_id == serviced_id).delete()
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
        
    def remove_user(service_id, user):
        try:
            ServiceAccess.query.filter(and_(ServiceAccess.user_id == user, ServiceAccess.service_id == service_id)).delete()
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
    
    def check(serviced_id):
        try:
            return bool(db.session.query(exists().where(ServiceAccess.service_id == serviced_id)).scalar())
        except SQLAlchemyError:
            db.session.rollback()
            raise    
    
    def hasRight(self, checkRight):
        return AccessRights.hasRight(self.rights, checkRight)
       
class DataSourceAllocation(db.Model):
    __tablename__ = 'datasource_allocations'  
    id = db.Column(db.Integer, primary_key=True)
    datasource_id = db.Column(db.Integer, db.ForeignKey('datasources.id'))
    url = db.Column(db.Text, nullable=False)
    
    visualizers = db.relationship('Visualizer', secondary = "data_visualizers")
    mimetypes = db.relationship('MimeType', secondary='data_mimetypes', lazy='dynamic')
    annotations = db.relationship('DataAnnotation', backref='datasource_allocation', lazy='dynamic')
    #properties = db.relationship('DataProperty', backref='datasource_allocation', lazy='dynamic', cascade='all, delete-orphan')
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
    
    def update_url(self, url):
        try:
            self.url = url
            db.session.commit()
            return self
        except SQLAlchemyError:
            db.session.rollback()
            raise
        
    @staticmethod
    def get(user_id, ds_id, url):
        return DataSourceAllocation.query.join(DataPermission, DataPermission.data_id == DataSourceAllocation.id).filter(and_(DataPermission.user_id == user_id, DataSourceAllocation.datasource_id == ds_id, DataSourceAllocation.url == url)).first()

    @staticmethod
    def get_allocation_by_url(ds_id, url):
        return DataSourceAllocation.query.filter(and_(DataSourceAllocation.datasource_id == ds_id, DataSourceAllocation.url == url)).first()
    
    def has_right(self, user_id, checkRight):
        dataPermission = DataPermission.query.filter(and_(DataPermission.user_id == user_id, DataPermission.data_id == self.id)).first()
        return AccessRights.hasRight(dataPermission.rights, checkRight)
    
    @staticmethod
    def has_access_rights(user_id, path, checkRights):
        defaultRights = AccessRights.NotSet
        
        if path == os.sep:
            defaultRights = AccessRights.Read # we are giving read access to our root folder to all logged in user

        prefixedDataSources = DataSource.query.filter(or_(DataSource.prefix == path, DataSource.url == path))
        if prefixedDataSources:
            defaultRights = AccessRights.Read

        allocations = DataSourceAllocation.query.join(DataPermission, DataPermission.data_id == DataSourceAllocation.id).filter(DataPermission.user_id == user_id)
        for allocation in allocations:
            if path.startswith(allocation.url):
                for permission in allocation.permissions: 
                    if AccessRights.hasRight(permission.rights, checkRights):
                        return True
                    
        return defaultRights >= checkRights

    @staticmethod
    def get_access_rights(user_id, path):
        defaultRights = AccessRights.NotSet
        
        if path == os.sep:
            defaultRights = AccessRights.Read # we are giving read access to our root folder to all logged in user

        prefixedDataSources = DataSource.query.filter(or_(DataSource.prefix == path, DataSource.url == path))
        if prefixedDataSources:
            defaultRights = AccessRights.Read
        
        allocations = DataSourceAllocation.query.join(DataPermission, DataPermission.data_id == DataSourceAllocation.id).filter(DataPermission.user_id == user_id)
        for allocation in allocations:
            if path.startswith(allocation.url):
                for permission in allocation.permissions:
                    return permission.rights 
        
        return defaultRights
    
    @staticmethod
    def check_access_rights(user_id, path, checkRights):
        if not DataSourceAllocation.has_access_rights(user_id, path, checkRights):
            raise DataAccessError(path)
    
    @staticmethod
    def access_rights_to_string(user_id, path):
        return AccessRights.rights_to_string(DataSourceAllocation.get_access_rights(user_id, path))
    
# class Data(db.Model):
#     __tablename__ = 'data'
#     id = db.Column(db.Integer, primary_key=True)
#     datasource_id = db.Column(db.Integer, db.ForeignKey('datasources.id'), nullable=True)
#     datatype = db.Column(db.Integer)
#     url = db.Column(db.Text)

class TaskStatus(db.Model):
    __tablename__ = 'taskstatus'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
            }
    
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    runnable_id = db.Column(db.Integer, db.ForeignKey('runnables.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    started_on = db.Column(db.DateTime, default=datetime.utcnow)
    ended_on = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Text)    
    comment = db.Column(db.Text)
    duration = db.Column(db.Float, default=0.0)
    
    tasklogs = db.relationship('TaskLog', cascade="all,delete-orphan", backref='task', lazy='dynamic')
    outputs = db.relationship('TaskData', cascade="all,delete-orphan", backref='task', order_by="asc(TaskData.id)", lazy='subquery')
    inputs = db.relationship('InData', cascade="all,delete-orphan", backref='task', order_by="asc(InData.id)", lazy='subquery')

    @staticmethod
    def create_task(runnable_id, service_id):
        try:
            task = Task(runnable_id=runnable_id, service_id=service_id, status=Status.RECEIVED)
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
    
    def succeeded(self):
        try:
            self.status = Status.SUCCESS
            self.add_log(Status.SUCCESS, LogType.INFO)
            self.ended_on = datetime.utcnow()
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
        
    def add_input(self, user_id, datatype, value, rights, **kwargs):
        data = Data.get_by_type_value(datatype, value)
        if not data:
            data = Data.add(value, datatype, **kwargs)
        
        data.allocate_for_user(user_id, rights)

        InData.add(self.id, data.id)
        #self.inputs.append()
        return data
    
    def add_output(self, datatype, value, **kwargs):
        # data = Data.get_by_type_value(datatype, value)
        # if not data:
        #     data = Data.add(value, datatype, **kwargs)
        data = Data.add(value, datatype, **kwargs)
        
        data.allocate_for_user(self.runnable.user_id, AccessRights.Owner)
        DataProperty.add(data.id, "execution {0}".format(self.id), { 'workflow': { 'task_id': self.id, 'job_id': self.runnable_id, 'workflow_id': self.runnable.workflow_id, 'inout': 'out'} })
        TaskData.add(self.id, data.id)

        return data

    def to_json_log(self):
#         data = self.data
#         if data and data.startswith('[') and data.endswith(']'):
#             data = data[1:]
#             data = data[:-1]
        
        data = []#[{ "datatype": data.value["valuetype"], "data": data.value["value"]} for data in self.outputs]
        for output in self.outputs:
            dataitem = Data.query.get(output.data_id)
            datavalue = dataitem.value["value"]
            if int(dataitem.value["type"]) == DataType.FileList or int(dataitem.value["type"]) == DataType.FolderList:
                datavalue = datavalue.strip('][').split(', ')
            data.append({ "id": dataitem.id, "datatype": dataitem.value["type"], "data": datavalue})
            
        log = {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'data': data,
            'duration': self.duration if self.duration != None else (self.ended_on - self.started_on).seconds
        }
#         if self.status == Status.SUCCESS and (self.datatype & DataType.FileList) > 0:
#             log['data'] = log['data'].strip('}{').split(',')
        return log

    @property
    def name(self):
        return self.service.value["name"]
    @property
    def package(self):
        return self.service.value["package"] if "package" in self.service.value else ""
    @property
    def moduledef(self):
        v = self.service.value
        return namedtuple("value", v.keys())(*v.values())
    
    @staticmethod
    def get_logs(task_id):
        task = Task.query.get(task_id)
        return [tasklog.to_json_log() for tasklog in task.tasklogs.filter(or_(TaskLog.type==LogType.STDERR, TaskLog.type==LogType.STDOUT))]
       
class TaskLog(db.Model):
    __tablename__ = 'tasklogs'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    time = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.Text, default=LogType.ERROR)
    log = db.Column(db.Text)
    
    def to_json_log(self):
        return {
            'time': str(self.time),
            'type': self.type,
            'log': self.log
        }
        
    def updateTime(self):
        try:
            self.time = datetime.utcnow()
            db.session.add(self)
        except SQLAlchemyError:
            db.session.rollback()
            raise

class ActivityLog(db.Model):
    __tablename__ = 'activitylogs'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))
    time = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.Text, default=LogType.ERROR)
    log = db.Column(db.Text)
    
    def to_json(self):
        return {
            'time': self.time.strftime("%d-%m-%Y %H:%M:%S"),
            'type': self.type,
            'log': self.log
        }
        
class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.String(30), default=ActivityType.ADDTOOL)
    status = db.Column(db.String(30), default=Status.NEW)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    modified_on = db.Column(db.DateTime, default=datetime.utcnow)

    logs = db.relationship('ActivityLog', backref='activity', lazy='subquery', cascade="all,delete-orphan") 
    def add_log(self, log, type =  LogType.INFO):
        try:
            tasklog = ActivityLog(type=type, log = log)
            self.logs.append(tasklog)
            db.session.commit()
            return tasklog
        except SQLAlchemyError:
            db.session.rollback()
            raise

    @staticmethod
    def create(user_id, type):
        try:
            activity = Activity(user_id = user_id, type = type)
            db.session.add(activity)
            db.session.commit()
            return activity
        except SQLAlchemyError:
            db.session.rollback()
            raise

    def updateTime(self):
        try:
            self.modified_on = datetime.utcnow()
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
    
    def json(self):
        return {
            'id': self.id,
            'type': self.type,
            'status': self.status,
            'modified_on': self.modified_on.strftime("%d-%m-%Y %H:%M:%S")
        }

    def to_json(self):
        data = self.json()
        data.update({'logs': [log.to_json() for log in self.logs]})
        return data

class Runnable(db.Model):
    __tablename__ = 'runnables'
    id = db.Column(db.Integer, primary_key=True)
    workflow_id  = db.Column(db.Integer, db.ForeignKey('workflows.id', ondelete='CASCADE'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    celery_id = db.Column(db.String(64))
    status = db.Column(db.String(30), default=Status.PENDING)
    script = db.Column(db.Text, nullable=False)
    out = db.Column(db.Text, default='')
    error = db.Column(db.Text, default='')
    view = db.Column(db.Text, default='')
    duration = db.Column(db.Float, default = 0.0)
    started_on = db.Column(db.DateTime, default=datetime.utcnow)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    modified_on = db.Column(db.DateTime, default=datetime.utcnow)
    
    tasks = db.relationship('Task', backref='runnable', order_by="asc(Task.id)", lazy='subquery', cascade="all,delete-orphan") 
    args = db.relationship('RunnableArg', backref='runnable', lazy='dynamic', cascade="all,delete-orphan") #cascade="all,delete-orphan",
    returns = db.relationship('RunnableReturn', backref='runnable', lazy='dynamic', cascade="all,delete-orphan")

    @staticmethod
    def add_return(runnable_id, datatype, value, **kwargs):
        runnable = Runnable.query.get(runnable_id)
        data = Data.get_by_type_value(datatype, value)
        if not data:
            data = Data.add(value, datatype, **kwargs)
        
        data.allocate_for_user(runnable.user_id, AccessRights.Owner)
        DataProperty.add(data.id, "execution {0}".format(runnable_id), { 'workflow': { 'job_id': runnable_id, 'workflow_id': runnable.workflow_id, 'inout': 'out'} })

        return data

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
    
    def set_status(self, value, update = True):
        self.status = value
    
        if value == Status.STARTED:
            self.started_on = datetime.utcnow()
    
        if update:
            self.update()

    # @property
    # def view(self):
    #     if 'view' in self.value:
    #         return self.value['view']
    
    # @view.setter
    # def view(self, value):
    #     self.value['view'] = value
    #     flag_modified(self, 'value')

    def get_duration(self):
        return self.duration if self.duration != None else (self.modified_on - self.created_on).seconds

    def json(self):
        
        return {
            'id': self.id,
            'name': self.workflow.name,
            'script': self.script,
            'status': self.status,
            'out': self.out,
            'err': self.error,
            'duration': self.get_duration(),
            'created_on': str(self.created_on),
            'modified_on': str(self.modified_on),
            'view': self.view
        }
    
    def to_json_tooltip(self):
        error = ""
        if error:
            error = (self.error[:60] + '...') if len(self.error) > 60 else self.error
        return {
            'id': self.id,
            'name': self.workflow.name,
            'status': self.status,
            'err': error,
            'duration': self.get_duration(),
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
            'err': self.error,
            'duration': self.get_duration(),
            'log': log
        }
        
    def to_json_info(self):
        return {
            'id': self.id,
            'user_id': self.workflow.user_id,
            'name': self.workflow.name,
            'modified': self.modified_on.strftime("%d-%m-%Y %H:%M:%S") if self.modified_on else '',
            'status': self.status
        }

    @staticmethod
    def create(user_id, workflow_id, script, args):
        try:
            runnable = Runnable(workflow_id=workflow_id, user_id=user_id, script=script, status = Status.PENDING)
            RunnableArg.query.filter(RunnableArg.runnable_id==runnable.id).delete()
            db.session.commit()

            if args:
                if isinstance(args, str):
                    args = json.loads(args)
                for p in args:
                    runnable.args.append(RunnableArg(value = p))
        
            db.session.add(runnable)
            db.session.commit()
            return runnable
        except SQLAlchemyError:
            db.session.rollback()
            raise
    
    def get_user(self):
        return User.query.get(self.user_id)
    @property
    def modules(self):
        return self.tasks
    @property
    def name(self):
        return Workflow.query.get(self.workflow_id).name

class Filter(db.Model):
    __tablename__ = 'filters'
    id = db.Column(db.Integer, primary_key=True)
    user_id  = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.Text, nullable = False)
    value = db.Column(JSON, nullable = False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    
    @staticmethod
    def add(**kwargs):
        try:
            if not kwargs['created_on']:
                kwargs['created_on'] = datetime.utcnow()
            filterobj = Filter(**kwargs)
            db.session.add(filterobj)
            db.session.commit()
            return filterobj
        except SQLAlchemyError:
            db.session.rollback()
            raise
        
    @staticmethod
    def remove(filter_id):
        try:
            Filter.query.filter_by(id = filter_id).delete()
            db.session.commit()
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
    def add(**kwargs):
        try:
            if 'created_on' not in kwargs:
                kwargs['created_on'] = datetime.utcnow()

            filterobj = FilterHistory(kwargs)
            db.session.add(FilterHistory(kwargs))
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

class WorkflowAnnotation(db.Model):
    __tablename__ = 'workflow_annotations'
    id = db.Column(db.Integer, primary_key=True)
    workflow_id  = db.Column(db.Integer, db.ForeignKey('workflows.id'), nullable=True)
    tag = db.Column(db.Text, nullable = False)
    
    @staticmethod
    def add(workflow_id, tag):
        try:
            annotation = WorkflowAnnotation.query.filter_by(workflow_id = workflow_id).first()
            if not annotation:            
                annotation = WorkflowAnnotation()
                annotation.workflow_id = workflow_id
                db.session.add(annotation)
            elif annotation.tag == tag:
                return annotation
                
            annotation.tag = tag
            
            db.session.commit()
            return annotation
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
    data_id  = db.Column(db.Integer, db.ForeignKey('data.id'), nullable=True)
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
    extension = db.Column(db.Text, nullable = True)
        
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
        
class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(JSON) #datatype, data, valuetype
    
    properties = db.relationship('DataProperty', backref='datasource_allocation', lazy='dynamic', cascade='all, delete-orphan')
    #properties = db.relationship('Property', backref='data', lazy='dynamic', cascade='all, delete-orphan', foreign_keys='')
    
    @staticmethod
    def get_by_type_value(datatype, value):
        return Data.query.filter(and_(Data.value["valuetype"].astext.cast(db.Integer) == datatype, Data.value["value"].astext.cast(db.Text) == value)).first()
    
    @staticmethod
    def get_by_path(fullpath):
        return Data.query.filter(and_(Data.value["path"] == cast(os.path.dirname(fullpath), JSON), Data.value["name"] == cast(os.path.basename(fullpath), JSON))).first()

    @property
    def name(self):
        if self.value and self.value["name"] != None:
            return self.value["name"]

    def rename(self, name):
        if (self.name == name):
            return self.name
        
        try:
            self.value["name"] = name
            flag_modified(self, "value")
            db.session.add(self)
            db.session.commit()
            return name
        except SQLAlchemyError:
            db.session.rollback()
            raise
    
    @staticmethod
    def get_datasource(ds_id, url):
        return Data.query.filter(and_(Data.value["datasource"] == cast(ds_id, JSON), Data.value["value"] == cast(url, JSON))).first()
    
#     @staticmethod
#     def get_datatype_from_value(value):
#         valuetype = None
#         pythontype = type(value)
#         if pythontype == "<class 'int'>":
#             valuetype = DataType.
    
    @staticmethod
    def add_json(value, data):
        try:
            data.value = value
            db.session.add(data)
            db.session.commit()
            return data
        except SQLAlchemyError:
            db.session.rollback()
            raise

    def allocate_for_user(self, user_id, rights):
        return DataAllocation.add(user_id, self.id, rights)

    @staticmethod
    def add(value, valuetype, **kwargs):
        datavalue = dict(kwargs)
        datavalue.update({"value": value, "type": str(valuetype), "datatype": str(type(value)), "created": str(datetime.utcnow()), "modified": str(datetime.utcnow())})
        return Data.add_json(datavalue, Data())

    @staticmethod
    def add_json_value(value):
        try:
            data = Data()
            data.value = value
            db.session.add(data)
            db.session.commit()
            return data
        except SQLAlchemyError:
            db.session.rollback()
            raise

class DataAllocation(db.Model):
    __tablename__ = 'data_allocations'
    id = db.Column(db.Integer, primary_key=True)
    data_id = db.Column(db.Integer, db.ForeignKey('data.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rights = db.Column(db.Integer, default = 0)
    
    data = db.relationship("Data", foreign_keys=[data_id])
    
    @staticmethod
    def add(user_id, data_id, rights):
        try:
            allocation = DataAllocation.query.filter(and_(DataAllocation.user_id == user_id, DataAllocation.data_id == data_id)).first()
            if not allocation:
                allocation = DataAllocation(user_id = user_id, data_id=data_id, rights=rights)
                db.session.add(allocation)
            elif allocation.rights >= rights:
                return allocation
            else:
                allocation.rights = rights
            db.session.commit()
            return allocation
        
        except SQLAlchemyError:
            db.session.rollback()
            raise
        
    @staticmethod
    def add_datasource(user_id, ds_id, url, rights):
        try:
            data = Data.add_datasource(url, ds_id)
            return DataAllocation.add(user_id, data.id, rights)
        except SQLAlchemyError:
            db.session.rollback()
            raise
    
    @staticmethod
    def add_value(user_id, name, value, valuetype, path, rights, **kwargs):
        try:
            data = Data.add_value(name, value, valuetype, path, **kwargs)
            return DataAllocation.add(user_id, data.id, rights)
        except SQLAlchemyError:
            db.session.rollback()
            raise
    
    @staticmethod
    def add_json_value(user_id, value, rights):
        try:
            data = Data.add_json_value(value)
            return DataAllocation.add(user_id, data.id, rights)
        except SQLAlchemyError:
            db.session.rollback()
            raise
        
    def has_read_access(self):
        return self.has_right(AccessRights.Read)
    
    def has_write_access(self):
        return self.has_right(AccessRights.Write)
    
    def has_owner_access(self):
        return self.has_right(AccessRights.Owner)
    
#     @staticmethod
#     def get(user_id, ds_id, url):
#         data = Data.get_datasource(ds_id, url)
#         if data:
#             return DataAllocation.query.filter(and_(DataAllocation.user_id == user_id, DataAllocation.data_id == data.id)).first()
       
    def has_right(self, checkRight):
        return AccessRights.hasRight(self.rights, checkRight)
    
    @staticmethod
    def has_access_rights(user_id, path, checkRights):
        return True
#        defaultRights = AccessRights.NotSet
        
#         if path == os.sep:
#             defaultRights = AccessRights.Read # we are giving read access to our root folder to all logged in user
# 
#         prefixedDataSources = DataSource.query.filter(or_(DataSource.prefix == path, DataSource.url == path))
#         if prefixedDataSources:
#             defaultRights = AccessRights.Read

#         allocations = DataAllocation.query.join(DataAllocation, DataAllocation.data_id == DataSourceAllocation.id).filter(DataAllocation.user_id == user_id)
#         for allocation in allocations:
#             if path.startswith(allocation.url):
#                 for permission in allocation.permissions:   
#                     if AccessRights.hasRight(permission.rights, checkRights):
#                         return True
#                     
#         return defaultRights >= checkRights

    @staticmethod
    def get_access_rights(user_id, path):
        return AccessRights.Read | AccessRights.Write
    
    @staticmethod
    def check_access_rights(user_id, path, checkRights):
        if not DataAllocation.has_access_rights(user_id, path, checkRights):
            raise DataAccessError(path)
    
    @staticmethod
    def access_rights_to_string(user_id, path):
        return AccessRights.rights_to_string(DataAllocation.get_access_rights(user_id, path))
    
class TaskData(db.Model):
    __tablename__ = 'taskdata'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, ForeignKey('tasks.id'))
    data_id = db.Column(db.Integer, ForeignKey('data.id'))
    
    data = db.relationship("Data", foreign_keys=[data_id])

    @staticmethod
    def add(task_id, data_id):
        try:
            taskdata = TaskData(task_id = task_id, data_id = data_id)
            db.session.add(taskdata)
            db.session.commit()
            return taskdata
        except SQLAlchemyError:
            db.session.rollback()
            raise
    @property
    def value(self):
        v = Data.query.get(self.data_id).value
        return namedtuple("value", v.keys())(*v.values())

class InData(db.Model):
    __tablename__ = 'indata'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, ForeignKey('tasks.id'))
    data_id = db.Column(db.Integer, ForeignKey('data.id'))
    
    @staticmethod
    def add(task_id, data_id):
        try:
            indata = InData(task_id = task_id, data_id = data_id)
            db.session.add(indata)
            db.session.commit()
            return indata
        except SQLAlchemyError:
            db.session.rollback()
            raise
    @property
    def value(self):
        v = Data.query.get(self.data_id).value
        return namedtuple("value", v.keys())(*v.values())
    
    @property
    def type(self):
       return self.value.type 
