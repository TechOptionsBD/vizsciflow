from config import Config

from ..models import Runnable, Task, Service
from ..graphutil import RunnableItem, WorkflowItem
from ..mocks.runmocks import ModuleManagerMock
from .workflowmgr import workflowmanager
from ..elasticutil import ElasticRunnable

class ElasticRunnableManager():
    
    @staticmethod
    def create_runnable(user, workflow, script, provenance, args):
        return ElasticRunnable.create(user, workflow, script, provenance, args)
       
    @staticmethod
    def add_module(workflow_id, package, function):
        workflowItem = WorkflowItem.load(workflow_id)
        return workflowItem.add_module(package, function)
    
    @staticmethod
    def invoke_module(runnable_id, function_name, package):
        runnableItem = ElasticRunnable.get(id=runnable_id).first()
        return runnableItem.invoke_module(function_name, package)
    
    @staticmethod
    def get_runnables(**kwargs):
        return ElasticRunnable.get(**kwargs)
    
    @staticmethod
    def runnables_of_user(user_id):
        return ElasticRunnable.load_for_users(user_id)

class GraphRunnableManager():
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

class DBRunnableManager():
    
       
    @staticmethod
    def create_runnable(user, workflow, script, provenance, args):
        return Runnable.create(user.id, workflow.id, script, args)
    
    @staticmethod
    def get_runnables(**kwargs):
        return Runnable.query.filter_by(**kwargs)
    
    @staticmethod
    def invoke_module(runnable_id, function_name, package):
        service = Service.get_first_service_by_name_package(function_name, package)
        if service:
            return Task.create_task(runnable_id, service.id)
    
    @staticmethod
    def runnables_of_user(user_id):
        from ..models import Workflow
        return Runnable.query.join(Workflow).filter(Workflow.user_id == user_id).order_by(Runnable.created_on.desc())
    
class RunnableManager:
    def __init__(self):
        if Config.DATA_MODE == 0:
            self.manager = DBRunnableManager()
        elif Config.DATA_MODE == 1:
            self.manager = GraphRunnableManager()
        elif Config.DATA_MODE == 3:
            self.manager = ElasticRunnableManager()
            
        #self.dbmanager = DBModuleManager() if Config.DATA_MODE != 0 else self.manager # we need this line as long as we have pre-provenance data in the rdbms

    def add_module(self, workflow_id, package, function_name):
        return self.manager.add_module(workflow_id, package, function_name)
    
    def create_runnable(self, user, workflow, script, provenance, args):
        return self.manager.create_runnable(user, workflow, script, provenance, args)
    
    def invoke_module(self, runnable_id, function_name, package):
        return self.manager.invoke_module(runnable_id, function_name, package)
    
    def update_runnable(self, properties):
        return self.manager.update_runnable(properties)
        
    def get_runnables(self, **kwargs):
        return self.manager.get_runnables(**kwargs)
    
    def get_runnable(self, **kwargs):
        return self.get_runnables(**kwargs).first()

    def runnables_of_user(self, user_id):
        return self.manager.runnables_of_user(user_id)
    
runnablemanager = RunnableManager()