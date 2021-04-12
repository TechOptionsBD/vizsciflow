from app.common import AccessRights
import json
from config import Config
from ..models import Service, ServiceAccess
from ..graphutil import ModuleItem, UserItem

class obj(object):
    def __init__(self, dict_):
        self.__dict__.update(dict_)

def dict2obj(d):
    return json.loads(json.dumps(d), object_hook=obj)

class GraphModuleManager():
    @staticmethod
    def get(**kwargs):
        return ModuleItem.get(**kwargs)
    
    @staticmethod
    def add(user_id, value, access, users):
        return ModuleItem.add(user_id, value, access, users)

    @staticmethod
    def get_modules_by_name_package(name, package):
        return ModuleItem.get(name=name, package=package)

    @staticmethod
    def get_all_by_user_access(user_id, access):
        ms = ModuleItem.get(public=True)
        modules = [m.json() for m in ms]
        u = UserItem.first(id=user_id)
        for m in u.modules:
            modules.append(m.json())
        return modules
    
    @staticmethod
    def get(**kwargs):
        return ModuleItem.get(**kwargs)
    
    @staticmethod
    def get_module_by_name_package(name, package):
        return GraphModuleManager.get(name=name, package=package).first()
    
    @staticmethod
    def add_user_access(id, users):
        return ModuleItem.add_user_access(id, users, AccessRights.Write)

    @staticmethod
    def insert_modules(url):
        return ModuleItem.insert_modules(url)

    @staticmethod
    def get_module_by_name_package_for_user_access(user_id, name, package):
        return ModuleItem.get_module_by_name_package_for_user_access(user_id, name, package)

class DBModuleManager():
    @staticmethod
    def get(**kwargs):
        pass

    @staticmethod
    def add(user_id, value, access, users):
        return Service.add(user_id, value, access, users)

    @staticmethod
    def get_module_by_name_package_for_user_access(user_id, name, package):
        return Service.get_module_by_name_package_for_user_access(user_id, name, package)

    @staticmethod
    def get_module_by_name_package(name, package):
        return dict2obj(Service.get_first_service_by_name_package(name, package).value)
        
    @staticmethod
    def get_modules_by_name_package(name, package):
        return Service.get_service_by_name_package(name, package)

    @staticmethod
    def update_access(service_id, access):
        return Service.update_access(service_id, access)

    @staticmethod
    def remove(user_id, module_id):
        return Service.remove(user_id, module_id)

    @staticmethod
    def get_all_by_user_access(user_id, access):
        return Service.get_by_user(user_id, access)

    @staticmethod
    def get_modules(**kwargs):
        return Service.query.filter_by(**kwargs)

    @staticmethod
    def get_access(self, **kwargs):
        return ServiceAccess.get(**kwargs)

    @staticmethod
    def remove_user_access(service_id, user):
        ServiceAccess.remove_user(service_id, user)

    @staticmethod
    def add_user_access(service_id, sharing_with):
        ServiceAccess.add(service_id, sharing_with)
    
    @staticmethod
    def check_access(serviced_id):
        return ServiceAccess.check(serviced_id)

    @staticmethod
    def insert_modules(url):
        return Service.insert_modules(url)

class ModuleManager():
    def __init__(self):
        if Config.DATA_MODE == 0:
            self.persistance = DBModuleManager()
        else:
            self.persistance = GraphModuleManager()
        
    def insert_modules(self, path):
        return self.persistance.insert_modules(path)

    def get_module_by_name_package_for_user_access(self, user_id, name, package = None):
        return self.persistance.get_module_by_name_package_for_user_access(user_id, name, package)

    def get_module_by_name_package(self, name, package = None):
        return self.persistance.get_module_by_name_package(name, package)
        
    def get_modules_by_name_package(self, name, package = None):
        return self.persistance.get_modules_by_name_package(name, package)

    def check_function(self, name, package = None):
        modules = self.get_modules_by_name_package(name, package)
        return modules and modules.count() > 0

    def update_access(self, service_id, access):
        return self.persistance.update_access(service_id, access)

    def remove(self, user_id, module_id):
        return self.persistance.remove(user_id, module_id)
    
    def get_all_by_user_access(self, user_id, access = 2):
        return self.persistance.get_all_by_user_access(user_id, access)
    
    def get_module(self, **kwargs):
        return self.get_modules(**kwargs).first()
    def get_modules(self, **kwargs):
        return self.persistance.get_modules(**kwargs)

    def get_access(self, **kwargs):
        return self.persistance.get_access(**kwargs)
    
    def remove_user_access(self, service_id, user):
        self.persistance.remove_user(service_id, user)

    def add_user_access(self, service_id, sharing_with):
        self.persistance.add_user_access(service_id, sharing_with)

    def check_access(self, service_id):
        self.persistance.check_access(service_id)
    
    def get(self, **kwargs):
        return self.persistance.get(**kwargs)

    def add(self, user_id, value, access, users):
        return self.persistance.add(user_id, value, access, users)

modulemanager = ModuleManager()