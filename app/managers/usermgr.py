import uuid
import hashlib
from datetime import datetime
from py2neo import NodeMatcher
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

from flask import current_app
from config import Config
from ..models import User, Role, Follow, Post, Comment
from ..graphutil import UserItem, RoleItem

class IUser(object):
    def __init__(self, email, username, password, confirmed):
        pass

# class UserItem(object):
#     def __init__(self, email, username, password, confirmed):
#         self.id = uuid.uuid4()
#         self.email = email
#         self.username = username
#     #role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
#         self.password = generate_password_hash(password)
#         self.confirmed = confirmed
#         self.name = ""
#         #self.location = location
#         #about_me = db.Column(db.Text())
#         self.member_since = datetime.utcnow
#         self.last_seen = datetime.utcnow
    
#     def json(self):
#         try:
#             msg = {
#                 'event': 'USER-SAVE',
#                 'id': str(self.id),
#                 'username': self.username,
#                 'password': self.password,
#                 'name': self.name,
#                 'member_since': str(self.member_since),
#                 'last_seen': str(self.last_seen),
#                 'confirmed': str(self.confirmed),
#                 'error': 'success'
#             }
            
#             return msg    
#         except:
#             pass
#     def verify_password(self, password):
#         return check_password_hash(self.password, password)
    
#     def ping(self):
#         self.last_seen = str(datetime.utcnow())
        
#         gfuser = GraphUser.get_by_id(self.id)
#         gfuser['last_seen'] = self.last_seen
#         gfuser.push()

#     def confirmed(self):
#         return self.confirmed
    
#     def generate_confirmation_token(self, expiration=3600):
#         s = Serializer(current_app.config['SECRET_KEY'], expiration)
#         return s.dumps({'confirm': self.id})
    
#     def confirm(self, token):
#         s = Serializer(current_app.config['SECRET_KEY'])
#         try:
#             data = s.loads(token)
#         except:
#             return False
#         if data.get('confirm') != self.id:
#             return False
#         self.confirmed = True
        
#         gfuser = GraphUser.get_by_id(self.id)
#         gfuser['confirmed'] = self.confirmed
#         gfuser.push()
        
#         return True
    
#     def generate_reset_token(self, expiration=3600):
#         s = Serializer(current_app.config['SECRET_KEY'], expiration)
#         return s.dumps({'reset': self.id})

#     def reset_password(self, token, new_password):
#         s = Serializer(current_app.config['SECRET_KEY'])
#         try:
#             data = s.loads(token)
#         except:
#             return False
#         if data.get('reset') != self.id:
#             return False
#         self.password = new_password
        
#         gfuser = GraphUser.get_by_id(self.id)
#         gfuser['password'] = self.password
#         gfuser.push()
        
#         return True
    
#     def change_email(self, token):
#         s = Serializer(current_app.config['SECRET_KEY'])
#         try:
#             data = s.loads(token)
#         except:
#             return False
#         if data.get('change_email') != self.id:
#             return False
#         new_email = data.get('new_email')
#         if new_email is None:
#             return False
#         if self.query.filter_by(email=new_email).first() is not None:
#             return False
#         self.email = new_email
#         self.avatar_hash = hashlib.md5(
#             self.email.encode('utf-8')).hexdigest()
            
#         gfuser = GraphUser.get_by_id(self.id)
#         gfuser['email'] = self.email
#         gfuser.push()
        
#         return True
    
#     def generate_email_change_token(self, new_email, expiration=3600):
#         s = Serializer(current_app.config['SECRET_KEY'], expiration)
#         return s.dumps({'change_email': self.id, 'new_email': new_email})
    
class GraphUser():
    registry = {'user': UserItem, 'role': RoleItem, 'follow': Follow, 'post': Post, 'comment': Comment}
    
    @staticmethod
    def create_user(**kwargs):
        return UserItem.Create(**kwargs)

    @staticmethod
    def get(**kwargs):
         return UserItem.get(**kwargs)
       
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return GraphUser.get_by_id(data['id'])
        
    @staticmethod
    def verify_password(user, password):
        return user.verify_password(password)

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')
        
    @staticmethod
    def ping(self, user):
        gfuser = GraphUser.get_by_id(user.id)
        gfuser['last_seen'] = str(datetime.utcnow())
        gfuser.push()
    
    @staticmethod
    def get_cls(name):
        return GraphUser.registry[name]
    
    @staticmethod
    def insert_roles():
        return RoleItem.insert_roles()
    
    @staticmethod
    def get_other_users_with_entities(id, *args):
        return User.query.filter(id != User.id).with_entities(*args)

        
class DBUser():
    registry = {'user': User, 'role': Role, 'follow': Follow, 'post': Post, 'comment': Comment}

    @staticmethod
    def verify_auth_token(token):
        return User.verify_auth_token(token)
        
    @staticmethod
    def verify_password(user, password):
        return user.verify_password(password)
    
    @staticmethod
    def ping(self, user):
        user.ping()
    
    @staticmethod
    def add(email, username, password, confirmed):
        return User.add(email, username, password, confirmed)
    
    @staticmethod
    def add_self_follows(self):
        return User.add_self_follows()

    @staticmethod
    def insert_roles():
        return Role.insert_roles()
    
    @staticmethod
    def get(**kwargs):
         return User.query.filter_by(**kwargs).first()
        
    @staticmethod
    def get_or_404(id):
        return User.get_or_404(id)
    
    @staticmethod
    def get_other_users_with_entities(id, *args):
        return User.query.filter(id != User.id).with_entities(*args)

    @staticmethod
    def get_role(id):
        return Role.query.get(id)

    @staticmethod
    def create_user(**kwargs):
        return User(**kwargs)
    
    @staticmethod
    def get_cls(name):
        return DBUser.registry[name]

class UserManager():
    def __init__(self):
        if Config.DATA_MODE == 0:
            self.persistance = DBUser()
        else:
            self.persistance = GraphUser()
    
    def get(self, **kwargs):
        return self.persistance.get(**kwargs)
        
    def Save(self, dataitem):
        return self.persistance.Save(dataitem)
    
    def create_user(self, **kwargs):
        return self.persistance.create_user(**kwargs)

    def get_by_email(self, email):
        return self.persistance.get(email=email)
    
    def get_by_username(self, username):
        return self.persistance.get(username=username)
    
    def verify_auth_token(self, email):
        return self.persistance.verify_auth_token(email)

    def verify_password(self, user, password):
        return self.persistance.verify_password(user, password)
    
    def add(self, email, username, password, confirmed):
        return self.persistance.add(email, username, password, confirmed)
    
    def insert_roles(self):
        return self.persistance.insert_roles()
    
    def add_self_follows(self):
        return self.persistance.add_self_follows()
    
    def get_or_404(self, id):
        return self.persistance.get_or_404(id)

    def get_other_users_with_entities(self, id, *args):
        return self.persistance.get_other_users_with_entities(id, *args)
    
    def get_role(self, id):
        return self.persistance.get_role(id)

    def get_cls(self, name):
        return self.persistance.get_cls(name)
    
usermanager = UserManager()