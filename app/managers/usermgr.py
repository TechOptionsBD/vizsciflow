from datetime import datetime

from flask import current_app
from config import Config
from ..models import User, Role, Follow, Post, Comment
from ..graphutil import UserItem, RoleItem
from ..elasticutil import ElasticRole, ElasticUser

class IUser(object):
    def __init__(self, email, username, password, confirmed):
        pass

class ElasticUserManager():
    registry = {'user': UserItem, 'role': RoleItem, 'follow': Follow, 'post': Post, 'comment': Comment}
    
    @staticmethod
    def create_user(**kwargs):
        return ElasticUser.Create(**kwargs)

    @staticmethod
    def first(**kwargs):
         return ElasticUser.first(**kwargs)
    
    @staticmethod
    def insert_roles():
        return ElasticRole.insert_roles()

class GraphUser():
    registry = {'user': UserItem, 'role': RoleItem, 'follow': Follow, 'post': Post, 'comment': Comment}
    
    @staticmethod
    def create_user(**kwargs):
        return UserItem.Create(**kwargs)

    @staticmethod
    def first(**kwargs):
         return UserItem.first(**kwargs)

    @staticmethod
    def get(**kwargs):
         return UserItem.get(**kwargs)
      
        
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
        id_list = [i for i, value in enumerate(args) if value.lower() == 'id']
        args = [i for j, i in enumerate(args) if j not in id_list]

        properties = ["u.{0}".format(arg) for arg in args]
        for id in id_list:
            properties.insert(id, "ID(u)")
        properties = ",".join(properties)
                    
        returns = properties if properties else "u"
        users = UserItem.run("MATCH (u:UserItem) WHERE ID(u) <> {0} RETURN {1}".format(id, returns))
        rows = []
        for node in iter(users):
            row = [r[1] for r in node.items()]
            rows.append(row)
        return rows
        
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
    def first(**kwargs):
         return User.query.filter_by(**kwargs).first()

    @staticmethod
    def get(**kwargs):
         return User.query.filter_by(**kwargs).first()
        
    @staticmethod
    def get_or_404(id):
        return User.get_or_404(id)
    
    @staticmethod
    def get_other_users_with_entities(id, *args):
        import json
        from app.models import AlchemyEncoder
        result = User.query.filter(id != User.id).with_entities(*args)
        return json.dumps([r for r in result], cls=AlchemyEncoder)

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
        elif Config.DATA_MODE == 3:
            self.persistance = ElasticUserManager()
        else:
            self.persistance = GraphUser()
    
    def first(self, **kwargs):
        return self.persistance.first(**kwargs)

    def get(self, **kwargs):
        return self.persistance.get(**kwargs)
        
    def Save(self, dataitem):
        return self.persistance.Save(dataitem)
    
    def create_user(self, **kwargs):
        return self.persistance.create_user(**kwargs)

    def get_by_email(self, email):
        return self.first(email=email)
    
    def get_by_username(self, username):
        return self.first(username=username)
    
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