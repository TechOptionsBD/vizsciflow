from app.managers.mgrutil import ManagerUtility

class UserManager():
    def __init__(self):
        self.persistance = ManagerUtility.Manage('user')
    
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