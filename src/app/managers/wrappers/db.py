from app.objectmodel.models.rdb import *
from app.objectmodel.common import dict2obj
from dsl.fileop import FolderItem
from app.objectmodel.common import isiterable
from sqlalchemy import text

class UserManager():
    @staticmethod
    def first(**kwargs):
         return User.query.filter_by(**kwargs).first()

    @staticmethod
    def get(**kwargs):
         return User.query.filter_by(**kwargs)

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
    def get_or_404(id):
        return User.get_or_404(id)
    
    @staticmethod
    def get_other_users_with_entities(id, *args):
        import json
        args = [getattr(User, r) for r in args]
        result = User.query.filter(id != User.id).with_entities(*args)
        return [json.dumps([x for x in r], cls=AlchemyEncoder) for r in result]

    @staticmethod
    def get_role(id):
        return Role.query.get(id)

    @staticmethod
    def create_user(**kwargs):
        return User(**kwargs)

class DataManager():

    @staticmethod
    def first(**kwargs):
         return DataSourceAllocation.query.filter_by(**kwargs).first()

    @staticmethod
    def get(**kwargs):
         return DataSourceAllocation.query.filter_by(**kwargs)
        
    @staticmethod
    def check_access_rights(user_id, path, checkRights):
        DataSourceAllocation.check_access_rights(user_id, path, checkRights)
    
    @staticmethod
    def get_access_rights(user_id, path):
        DataSourceAllocation.get_access_rights(user_id, path)
    
    @staticmethod
    def has_access_rights(user_id, path, checkRights):
        return DataSourceAllocation.has_access_rights(user_id, path, checkRights)

    @staticmethod
    def load(user_id, recursive):
        datasets = DataAllocation.query.filter_by(user_id = user_id)
        data_dict = {}
        for dataset in datasets:
            pass
        
        return data_dict
    
    @staticmethod
    def add_task_data(triplet, task):
        if isinstance(triplet[1], FolderItem) and isiterable(triplet[1].path):
            for it in triplet[1].path:
                task.add_output(triplet[0], str(it))
        elif (triplet[0] == DataType.File or triplet[0] == DataType.Folder) and isiterable(triplet[1]):
            for it in triplet[1].path:
                task.add_output(triplet[0], str(it))
        else:
            task.add_output(triplet[0], str(triplet[1]))
    
    @staticmethod
    def is_data_item(value):
        return isinstance(value, Data)
    
    @staticmethod
    def add(user_id, datasource_id, url, rights):
        return DataSourceAllocation.add(user_id, datasource_id, url, rights)

    @staticmethod
    def get_allocation(datasource_id, **kwargs):
        return DataSourceAllocation.query.filter(datasource_id, **kwargs).first()
    
    @staticmethod
    def get_datasources(**kwargs):
        return DataSource.query.filter_by(**kwargs)

    @staticmethod
    def get_allocation_by_url(ds_id, url):
        return DataSourceAllocation.query.filter(and_(DataSourceAllocation.datasource_id == ds_id, DataSourceAllocation.url == url)).first()

    @staticmethod
    def insert_datasources():
        return DataSource.insert_datasources()

    @staticmethod
    def get_mimetype(extension):
        return MimeType.query.filter_by(extension = extension).first()

    @staticmethod
    def load_listview_datasets(user_id, page, no_of_item):
        return DataSource.load_listview_datasets(user_id, page, no_of_item)

    @staticmethod
    def load_dataset_data_for_plugin(dataset_id, data_id, page_num):
        return DataSource.load_dataset_data_for_plugin(dataset_id, data_id, page_num)
    
class ModuleManager():
    @staticmethod
    def first(**kwargs):
         return Service.query.filter_by(**kwargs).first()

    @staticmethod
    def get(**kwargs):
         return Service.query.filter_by(**kwargs)

    @staticmethod
    def get_by_value_key(**kwargs):
        if not kwargs:
            return ModuleManager.get(**kwargs)
            
        results = None
        for k,v in kwargs.items():
            if results:
                results = results.filter(func.lower(Service.value[f"{k}"].astext).cast(Unicode) == v.lower())
            else:
                results = Service.query.filter(func.lower(Service.value[f"{k}"].astext).cast(Unicode) == v.lower())
        return results

    @staticmethod
    def add(user_id, value, access, users, pipenv, pippkgs, reqfile):
        return Service.add(user_id, value, access, users, pipenv, pippkgs, reqfile)

    @staticmethod
    def get_module_by_name_package_for_user_access(user_id, name, package):
        return Service.get_module_by_name_package_for_user_access_json(user_id, name, package)

    @staticmethod
    def get_module_by_name_package(name, package):
        return dict2obj(Service.get_first_service_by_name_package_json(name, package))
        
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
        return Service.get_full_by_user_json(user_id, access)

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
    def insert_modules(funclist):
        return Service.insert_modules(funclist)
    
    @staticmethod
    def insert_module(func):
        return Service.insert_module(func)

class WorkflowManager():
    @staticmethod
    def first(**kwargs):
        return Workflow.query.filter_by(**kwargs).first()

    @staticmethod
    def get(**kwargs):
        return Workflow.query.filter_by(**kwargs)
    
    @staticmethod
    def get_or_404(id):
        return Workflow.query.get(id)

    @staticmethod
    def create(**kwargs):
        return Workflow.create(**kwargs)

    @staticmethod
    def remove(user_id, workflow_id):
        Workflow.remove(user_id, workflow_id)

    @staticmethod
    def update(id, **kwargs):
        return WorkflowManager.first(id=id).update(**kwargs)
    
    @staticmethod
    def get_workflows_as_list(access, user_id, *args):
        terms = ["tag='{0}'".format(v) for v in args]
        if access == 0 or access == 3:
            return Workflow.query.filter(Workflow.public == True).filter(or_(*terms))
        if access == 1 or access == 3:
            return Workflow.query.filter(Workflow.public != True).filter(Workflow.accesses.any(and_(WorkflowAccess.user_id == user_id, Workflow.user_id != user_id))).filter(or_(*terms)) # TODO: Do we need or_ operator here? 
        if access == 2 or access == 3:
            return Workflow.query.filter(and_(Workflow.public != True, Workflow.user_id == user_id)).filter(or_(*terms))

    @staticmethod
    def insert_workflows(path):
        return Workflow.insert_workflows(path)

    @staticmethod
    def get_returns_json(workflow_id):
        return dict2obj(Workflow.get_returns_json(workflow_id))

class RunnableManager():
    @staticmethod
    def first(**kwargs):
         return Runnable.query.filter_by(**kwargs).first()

    @staticmethod
    def get(**kwargs):
         return Runnable.query.filter_by(**kwargs)

    @staticmethod
    def create_runnable(user_id, workflow, script, provenance, args):
        return Runnable.create(user_id, workflow.id, script, args)
    
    @staticmethod
    def invoke_module(runnable_id, function_name, package):
        service = Service.get_first_service_by_name_package(function_name, package)
        if service:
            return Task.create_task(runnable_id, service.id)
    
    @staticmethod
    def runnables_of_user(user_id):
        return Runnable.query.join(Workflow).filter(Workflow.user_id == user_id).order_by(Runnable.created_on.desc())

    @staticmethod
    def get_task_logs(task_id):
        return Task.get_logs(task_id)
    
    @staticmethod
    def add_return(runnable_id, triplet):
        if isinstance(triplet[1], FolderItem) and isiterable(triplet[1].path):
            for it in triplet[1].path:
                Runnable.add_return(runnable_id, triplet[0], str(it))
        elif (triplet[0] == DataType.File or triplet[0] == DataType.Folder) and isiterable(triplet[1]):
            for it in triplet[1].path:
                Runnable.add_return(runnable_id, triplet[0], str(it))
        else:
            Runnable.add_return(runnable_id, triplet[0], str(triplet[1]))

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
        return FilterHistory.query.filter_by(**kwargs)

class Manager():
    @staticmethod
    def clear():
        try:
            db.drop_all()
            db.session.commit()
        except:
            db.session.rollback()
            raise
    
    @staticmethod
    def create():
        try:
            db.create_all()
            db.session.commit()
        except:
            db.session.rollback()
            raise

    @staticmethod
    def close():
        pass
