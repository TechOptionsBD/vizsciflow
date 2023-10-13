import os
import logging
import requests

from app.managers.mgrutil import ManagerUtility
from app.objectmodel.models.loader import Loader

class ModuleManager():
    def __init__(self):
        self.persistance = ManagerUtility.Manage('module')

    def get_by_id(self, id):
        return self.persistance.get(id = id)

    def first(self, **kwargs):
        return self.persistance.first(**kwargs)
    
    def get(self, **kwargs):
        return self.persistance.get(**kwargs)

    def insert_modules(self, activity, path, user_id = None, with_users = False, install_pypi = False):
        from urllib.parse import urljoin

        activity.add_log(log=f"Integrating services ...")

        external = path.startswith("http://") or path.startswith("https://")
        funclist = requests.get(urljoin(path, 'api/services')).json()["services"] if external else Loader.load_funcs_recursive_flat(path, with_users)

        from app.objectmodel.common import pip_activity, pip_req_activity, LogType
        modules = []
        for func in funclist:
            pkgfuncname = f"{func['package']}{'.' if func['package'] else ''}{func['name']}"
            try:
                if external:
                    func.update({'module': path})
                if install_pypi and "pipvenv" in func and func["pipvenv"]:
                    if "pippkgs" in func and func["pippkgs"]:
                        pippkgs = func["pippkgs"].split(",")
                        for pkg in pippkgs:
                            try:
                                pip_activity(activity, func["pipvenv"], pkg)
                            except Exception as e:
                                logging.error(f'Error installing package {pkg}: {str(e)}')

                    if "reqfile" in func and func["reqfile"]:
                        from app import app
                        reqfile = func["reqfile"] if os.path.isabs(func["reqfile"]) else os.path.join(app.config['ROOT_DIR'], func["reqfile"])
                        pip_req_activity(activity, func["pipvenv"], reqfile)
                
                module = self.persistance.add(user_id, value = dict(func), access=func['access'] if 'access' in func else 0, users=func['sharedusers'] if 'sharedusers' in func else [])
                if module:
                    activity.add_log(log=f"Integration of {pkgfuncname} service is successful.")
                    modules.append(module)
                else:
                    activity.add_log(log=f"Integration of {pkgfuncname} service is not successful.")
            except Exception as e:
                msg = f"Error in integrating service {pkgfuncname}: {str(e)}"
                logging.error(msg)
                activity.add_log(log=msg, type=LogType.ERROR)

        return modules

    def delete_modules(self, activity, path, user_id = None, with_users = False):
        from urllib.parse import urljoin

        activity.add_log(log=f"Deleting services ...")

        external = path.startswith("http://") or path.startswith("https://")
        if external:
            response = requests.get(urljoin(path, 'functions')).json()
        else:
            funclist = Loader.load_funcs_recursive_flat(path, with_users)

        from app.objectmodel.common import LogType
        modules = []
        for func in funclist:
            pkgfuncname = f"{func['package']}{'.' if func['package'] else ''}{func['name']}"
            try:
                module = self.persistance.get_module_by_name_package(func['name'], func['package'])
                if module:
                    module.remove()
                    activity.add_log(log=f"Deletion of {pkgfuncname} service is successful.")
            except Exception as e:
                msg = f"Error in deleting service {pkgfuncname}: {str(e)}"
                logging.error(msg)
                activity.add_log(log=msg, type=LogType.ERROR)

        return modules

    def get_module_by_name_package_for_user_access(self, user_id, name, package = None):
        return self.persistance.get_module_by_name_package_for_user_access(user_id, name, package)

    def get_module_by_name_package(self, name, package = None):
        return self.persistance.get_module_by_name_package(name, package)
    
    def get_module_by_name_package_json(self, name, package = None):
        return self.persistance.get_module_by_name_package_json(name, package)
    
    def get_modules_by_name_package(self, name, package = None):
        return self.persistance.get_modules_by_name_package(name, package)

    def check_function(self, name, package = None):
        modules = self.get_modules_by_name_package(name, package)
        return modules and modules.count() > 0

    def update_access(self, service_id, access):
        return self.persistance.update_access(service_id, access)

    def remove(self, user_id, module_id):
        return self.persistance.remove(user_id, module_id)
    
    def toggle_publish(self, user_id, module_id):
        return self.persistance.toggle_publish(user_id, module_id)
    
    def get_all_by_user_access(self, user_id, access = 2):
        return self.persistance.get_all_by_user_access(user_id, access)
    
    def get_access(self, **kwargs):
        return self.persistance.get_access(**kwargs)
    
    def remove_user_access(self, service_id, user):
        self.persistance.remove_user(service_id, user)

    def add_user_access(self, service_id, sharing_with):
        self.persistance.add_user_access(service_id, sharing_with)

    def check_access(self, service_id):
        self.persistance.check_access(service_id)
    
    def get_by_value_key(self, **kwargs):
        return self.persistance.get_by_value_key(**kwargs)

    def add(self, user_id, value, access, users):
        return self.persistance.add(user_id, value, access, users)

modulemanager = ModuleManager()