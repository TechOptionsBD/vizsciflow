from config import Config

from ..models import Runnable, Task, Service
from ..graphutil import RunnableItem, WorkflowItem
from ..mocks.runmocks import ModuleManagerMock
from .workflowmgr import workflowmanager

class GraphModuleManager():
#     @staticmethod
#     def Create(workflow_id, script, args):
#         return Runnable.create(workflow_id, script, args)
#     
#     @staticmethod
#     def Save(dataitem):
#         return graphgen.graph.run(
#             statement="CREATE (x) SET x = {dict_param}",
#             parameters={'dict_param': dataitem})
#         
#         matcher = NodeMatcher(graphgen.graph)
#         return matcher.get(dataitem['id'])
#     
#     @staticmethod
#     def SavePermission(user, rights, dataitem):
#         dataitem["user"] = str(user)
#         dataitem["rights"] = str(rights)
#         
#         return GraphPersistance.Save(dataitem)       
#   
#     @staticmethod
#     def SaveMetadata(data, metadata):
#         
#         metadatanode = GraphPersistance.Save(metadata)
#         return Relationship(data, "METADATA", metadatanode)
    
    @staticmethod
    def create_runnable(user, workflow, script, provenance, args):
        return RunnableItem.create(user, workflow, script, provenance, args)
    
#     @staticmethod
#     def update_runnable(properties):
#         try:
#             runnable = RunnableItem(properties['workflow_id'], properties['script'], properties['args'])
#             workflow = properties['workflow_id']
#             result = runnable.update_json(properties)            
#             print(result)
#             run = graphgen.graph.run("MATCH (x) WHERE x.workflow_id = {dict_param} SET x = {dict_param2}",{'dict_param': workflow, 'dict_param2': result}).data()
#             return run
#         except Exception as e:
#             return e
    
    @staticmethod
    def add_module(workflow_id, package, function):
        workflowItem = WorkflowItem.load(workflow_id)
        return workflowItem.add_module(package, function)
    
    @staticmethod
    def invoke_module(runnable_id, function_name, package):
        runnableItem = RunnableItem.get(id=runnable_id).first()
        return runnableItem.invoke_module(function_name, package)
    
    
#    @staticmethod
#     def create_workflow(user_id, name, desc, script, access, users, temp, derived = 0):
#         workflow = WorkflowItem(name, desc if desc else '', script, 2 if not access else int(access), users, temp, derived)
#         workflow = graphgen.graph.run(
#             statement="CREATE (x) SET x = {dict_param}",
#             parameters={'dict_param': workflow.json()})
#         
#         matcher = NodeMatcher(graphgen.graph)
#         user = matcher.match(id=user_id).first()
#         Relationship(user, "WORKFLOW", workflow)
#         
#         return workflow
    
    @staticmethod
    def get_runnables(**kwargs):
        return RunnableItem.get(**kwargs)
    
    @staticmethod
    def runnables_of_user(user_id):
        return RunnableItem.load_for_users(user_id)

class DBModuleManager():
    
#     @staticmethod
#     def Save(dataitem):
#         return Data.add(dataitem.json())
#     
#     @staticmethod
#     def SavePermission(user, rights, dataitem):
#         data = DBPersistance.Save(dataitem)
#         return DataAllocation.add(user, data.id, rights)
#     
#     @staticmethod
#     def SaveMetadata(data, user, rights, json):
#         metadata = Data.add(json)
#         DataAllocation.add(user, metadata.id, rights)
#         return Property.add(data.id, metadata.id)
       
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
    
    @staticmethod
    def runnables_of_user(user_id):
        return ElasticRunnable.load_for_users(user_id)

class RunnableManager:
    def __init__(self):
        if Config.DATA_MODE == 0:
            self.manager = DBModuleManager()
        elif Config.DATA_MODE == 1:
            self.manager = GraphModuleManager()
        else:
            self.manager = ModuleManagerMock()
            
        self.dbmanager = DBModuleManager() if Config.DATA_MODE != 0 else self.manager # we need this line as long as we have pre-provenance data in the rdbms
#        self.elasticManager = ElasticModuleManager() if Config.ELASTIC else None #It's may not the convinent way, kindly review

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