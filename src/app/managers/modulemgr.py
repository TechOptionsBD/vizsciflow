import logging
from app.managers.mgrutil import ManagerUtility
from app.objectmodel.models.loader import Loader

class ModuleManager():
    def __init__(self):
        self.persistance = ManagerUtility.Manage('module')

    def get_by_id(self, id):
        return self.persistance.get(id = id)

    def get(self, **kwargs):
        return self.persistance.get(**kwargs)

    def insert_modules(self, path, user_id = None, with_users = False, install_pypi = False):
        funclist = Loader.load_funcs_recursive_flat(path, with_users)

        from app.objectmodel.common import pip_install, pipinstall_req_file
        modules = []
        for func in funclist:
            try:
                if install_pypi and "pipenv" in func and func["pipenv"]:
                    if "pippkgs" in func and func["pippkgs"]:
                        pippkgs = func["pippkgs"].split(",")
                        for pkg in pippkgs:
                            try:
                                pip_install(func["pipenv"], pkg)
                            except Exception as e:
                                logging.error(f'Error installing package {pkg}: {str(e)}')

                    if "reqfile" in func and func["reqfile"]:
                        pipinstall_req_file(func["pipenv"], func["reqfile"])
                
                module = self.persistance.insert_modules(funclist, user_id)
                if module:
                    modules.extend(module)
            except Exception as e:
                logging.error(f"Error in inserting module {func['package']}{'.' if func['package'] else ''}{func['name']}: {str(e)}")

            return modules

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
    
    def get_by_value_key(self, **kwargs):
        return self.persistance.get_by_value_key(**kwargs)

    def add(self, user_id, value, access, users):
        return self.persistance.add(user_id, value, access, users)

modulemanager = ModuleManager()