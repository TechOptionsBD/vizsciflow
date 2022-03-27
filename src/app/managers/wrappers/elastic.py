from app.objectmodel.models.elasticutil import *

class UserManager():    
    @staticmethod
    def create_user(**kwargs):
        return ElasticUser.Create(**kwargs)

    @staticmethod
    def first(**kwargs):
         return ElasticUser.first(**kwargs)
    
    @staticmethod
    def insert_roles():
        return ElasticRole.insert_roles()
    
    @staticmethod
    def get_other_users_with_entities(id, *args):
        return ElasticUser.get_other_users_with_entities(id, *args)

class ModuleManager():
    @staticmethod
    def get(**kwargs):
        return ElasticModule.get(**kwargs)
    
    @staticmethod
    def add(user_id, value, access, users):
        return ElasticModule.add(user_id, value, access, users)

    @staticmethod
    def get_modules_by_name_package(name, package):
        return ElasticModule.get(name=name, package=package)

    @staticmethod
    def get_all_by_user_access(user_id, access):
        ms = ElasticModule.get(public=True)
        modules = [m.json() for m in ms]
        u = ElasticUser.first(id=user_id)
        for m in u.modules:
            modules.append(m.json())
        return modules
    
    @staticmethod
    def get(**kwargs):
        return ElasticModule.get(**kwargs)
    
    @staticmethod
    def get_module_by_name_package(name, package):
        return ModuleManager.get(name=name, package=package).first()
    
    @staticmethod
    def add_user_access(id, users):
        return ElasticModule.add_user_access(id, users, AccessRights.Write)

    @staticmethod
    def insert_modules(funclist):
        return ElasticModule.insert_modules(funclist)

    @staticmethod
    def get_module_by_name_package_for_user_access(user_id, name, package):
        return ElasticModule.get_module_by_name_package_for_user_access(user_id, name, package)

class DataManager():
    @staticmethod
    def insert_datasources():
        return ElasticDataSource.insert_datasources()

    @staticmethod
    def get_datasources(**kwargs):
        return ElasticDataSource.get(**kwargs)

    @staticmethod
    def is_data_item(value):
        return isinstance(value, ElasticValue)

    @staticmethod
    def add_task_data(dataAndType, task):
        return task.add_outputs(dataAndType)


class WorkflowManager():

    @staticmethod
    def first(**kwargs):
        return ElasticWorkflow.first(**kwargs)

    @staticmethod
    def get(**kwargs):
        return ElasticWorkflow.get(**kwargs)

    @staticmethod
    def get_workflows_as_list(access, user_id, *args):
        return ElasticWorkflow.get_workflows_as_list(access, user_id, *args)
    
    @staticmethod
    def create(**kwargs):
        return ElasticWorkflow.Create(**kwargs)

    @staticmethod
    def get_or_404(id):
        return ElasticWorkflow.first(id=id)

    @staticmethod
    def insert_workflows(path):
        return ElasticWorkflow.insert_workflows(path)

class RunnableManager():
    
    @staticmethod
    def get(**kwargs):
        return ElasticRunnable.get(**kwargs)
    
    @staticmethod
    def first(**kwargs):
        return ElasticRunnable.get(**kwargs).first()

    @staticmethod
    def create_runnable(user, workflow, script, provenance, args):
        return ElasticRunnable.create(user, workflow, script, provenance, args)
       
    # @staticmethod
    # def add_module(workflow_id, package, function):
    #     workflowItem = WorkflowItem.load(workflow_id)
    #     return workflowItem.add_module(package, function)
    
    @staticmethod
    def invoke_module(runnable_id, function_name, package):
        runnableItem = ElasticRunnable.get(id=runnable_id).first()
        return runnableItem.invoke_module(function_name, package)
    
    @staticmethod
    def runnables_of_user(user_id):
        return ElasticRunnable.load_for_users(user_id)

class Manager():
    
    @staticmethod
    def close():
        pass

    @staticmethod
    def create():
        pass
        
    @staticmethod
    def clear():
        final_indices = session().indices.get_alias().keys()
        
        for _index in final_indices:
            try:
                if "." not in _index: # avoid deleting indexes like `.kibana`
                    # if _index == 'datasets':# delete index as needed
                    # SessionManager.session().delete_by_query(index=_index, body={"query": {"match_all": {}}})
                    session().indices.delete(index=_index)
            except Exception as error:
                print ('indices.delete error:', error, 'for index:', _index)
