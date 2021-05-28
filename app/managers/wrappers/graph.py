from app.managers.wrappers.graphutil import *

class UserManager():
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
        gfuser = UserManager.get_by_id(user.id)
        gfuser['last_seen'] = str(datetime.utcnow())
        gfuser.push()
    
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
        
class DataManager():
    
    @staticmethod
    def is_data_item(value):
        return isinstance(value, ValueItem)
    
    @staticmethod
    def check_access_rights(user_id, path, checkRights):
        ValueItem.check_access_rights(user_id, path, checkRights)
    
    @staticmethod
    def get_access_rights(user_id, path):
        return ValueItem.get_access_rights(user_id, path)
        
    @staticmethod
    def add_task_data(dataAndType, task):
        return task.add_output(dataAndType)

    @staticmethod
    def insert_datasources():
        return DataSourceItem.insert_datasources()
    
    @staticmethod
    def get_datasources(**kwargs):
        return DataSourceItem.get(**kwargs)
    
    @staticmethod
    def add(user_id, datasource_id, url, rights):
        return DataSourceItem.add(user_id, datasource_id, url, rights)
    
    @staticmethod
    def has_access_rights(user_id, path, checkRights):
        return DataSourceItem.has_access_rights(user_id, path, checkRights)

class ModuleManager():
    @staticmethod
    def get(**kwargs):
        return ModuleItem.get(**kwargs)
    
    @staticmethod
    def add(user_id, value, access, users):
        return ModuleItem.add(user_id, value, access, users)

    @staticmethod
    def get_modules_by_name_package(name, package):
        params = {'name': name}
        if package:
            params['package'] = package
        return ModuleItem.get(**params)

    @staticmethod
    def get_all_by_user_access(user_id, access):
        ms = ModuleItem.get(public=True)
        modules = [m.json() for m in ms]
        u = UserItem.first(id=user_id)
        for m in u.modules:
            modules.append(m.json())
        return modules
    
    @staticmethod
    def get_module_by_name_package(name, package):
        return ModuleManager.get_modules_by_name_package(name, package).first()
    
    @staticmethod
    def add_user_access(id, users):
        return ModuleItem.add_user_access(id, users, AccessRights.Write)

    @staticmethod
    def insert_modules(funclist):
        return ModuleItem.insert_modules(funclist)

    @staticmethod
    def get_module_by_name_package_for_user_access(user_id, name, package):
        return ModuleItem.get_module_by_name_package_for_user_access(user_id, name, package)

class WorkflowManager():

    @staticmethod
    def first(**kwargs):
        return WorkflowItem.first(**kwargs)

    @staticmethod
    def get(**kwargs):
        return WorkflowItem.get(**kwargs)

    @staticmethod
    def get_workflows_as_list(access, user_id, *args):
        return WorkflowItem.get_workflows_as_list(access, user_id, *args)
    
    @staticmethod
    def create(**kwargs):
        return WorkflowItem.Create(**kwargs)

    @staticmethod
    def get_or_404(id):
        return WorkflowItem.first(id=id)

    @staticmethod
    def insert_workflows(path):
        return WorkflowItem.insert_workflows(path)

class RunnableManager():
    @staticmethod
    def get(**kwargs):
        return RunnableItem.get(**kwargs)
    
    @staticmethod
    def first(**kwargs):
        return RunnableItem.get(**kwargs).first()

    @staticmethod
    def create_runnable(user, workflow, script, provenance, args):
        return RunnableItem.create(user, workflow, script, provenance, args)
    
    @staticmethod
    def add_module(workflow_id, package, function):
        workflowItem = WorkflowItem.load(workflow_id)
        return workflowItem.add_module(package, function)
    
    @staticmethod
    def invoke_module(runnable_id, function_name, package):
        runnableItem = RunnableItem.get(id=runnable_id).first()
        return runnableItem.invoke_module(function_name, package)
    
    @staticmethod
    def get_runnables(**kwargs):
        return RunnableItem.get(**kwargs)
    
    @staticmethod
    def runnables_of_user(user_id):
        return RunnableItem.load_for_users(user_id)

class FilterManager():
    @staticmethod
    def first(**kwargs):
         return Filter.query.filter_by(**kwargs).first()

    @staticmethod
    def get(**kwargs):
         return Filter.query.filter_by(**kwargs)
       
    @staticmethod
    def remove(id):
        Filter.remove(id)

    @staticmethod
    def add(**kwargs):
        return Filter.add(**kwargs)
    
    @staticmethod
    def add_history(**kwargs):
        return FilterHistory.add(**kwargs)
    
    def get_history(self, **kwargs):
        return FilterHistory.get(**kwargs)