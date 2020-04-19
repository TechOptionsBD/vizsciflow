from config import Config

from .models import Runnable, Workflow, Task
from .graphutil import RunnableItem

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
    def create_runnable(user_id, workflow_id, script, args):
        return RunnableItem.create(user_id, workflow_id, script, args)
    
#     @staticmethod
#     def update_runnable(properties):
#         try:
#             runnable = RunnableItem(properties['workflow_id'], properties['script'], properties['arguments'])
#             workflow = properties['workflow_id']
#             result = runnable.update_json(properties)            
#             print(result)
#             run = graphgen.graph.run("MATCH (x) WHERE x.workflow_id = {dict_param} SET x = {dict_param2}",{'dict_param': workflow, 'dict_param2': result}).data()
#             return run
#         except Exception as e:
#             return e
    
    @staticmethod
    def create_task(runnable_id, function_name):
        runnableItem = RunnableItem.load(runnable_id)
        return runnableItem.add_module(function_name)
    
    @staticmethod
    def get_workflow(workflow_id):
        return Workflow.query.get(workflow_id)    
    
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
    def create_workflow(user_id, name, desc, script, access, users, temp, derived = 0):
        return Workflow.create(user_id, name, desc if desc else '', script, 2 if not access else int(access), users, temp, derived)

    @staticmethod
    def get_runnable(runnable_id):
        return RunnableItem.load(runnable_id)
    
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
    def get_workflow(workflow_id):
        return Workflow.query.get(workflow_id)
    
    @staticmethod
    def create_workflow(user_id, name, desc, script, access, users, temp, derived = 0):
        return Workflow.create(user_id, name, desc if desc else '', script, 2 if not access else int(access), users, temp, derived)
    
    @staticmethod
    def create_runnable(user_id, workflow_id, script, args):
        return Runnable.create(user_id, workflow_id, script, args)
    
    @staticmethod
    def get_runnable(runnable_id):
        return Runnable.query.get(int(runnable_id))
    
    @staticmethod
    def create_task(runnable_id, function_name):
        return Task.create_task(runnable_id, function_name)
    
    @staticmethod
    def runnables_of_user(user_id):
        return Runnable.query.join(Workflow).filter(Workflow.user_id == user_id)
    
class RunnableManager:
    def __init__(self):
        self.manager = GraphModuleManager() if Config.DATA_GRAPH else DBModuleManager()
        self.dbmanager = DBModuleManager() if Config.DATA_GRAPH else self.manager # we need this line as long as we have pre-provenance data in the rdbms

    def create_runnable(self, user_id, workflow_id, script, args):
        return self.manager.create_runnable(user_id, workflow_id, script, args)
    
    def create_task(self, runnable_id, function_name):
        return self.manager.create_task(runnable_id, function_name)
    
    def update_runnable(self, properties):
        return self.manager.update_runnable(properties)
    
    def get_workflow(self, workflow_id):
        return self.manager.get_workflow(workflow_id)
    
    def create_workflow(self, user_id, name, desc, script, access, users, temp, derived = 0):
        raise NotImplementedError
        if script and name:
            users = users.split(";") if users else []
            return self.manager.create_workflow(user_id, name, desc if desc else '', script, 2 if not access else int(access), users, temp, derived)
    
    def get_runnable(self, runnable_id):
        return self.manager.get_runnable(runnable_id)
    
    def runnables_of_user(self, user_id):
        #Runnable.query.join(Workflow).filter(Workflow.user_id == user_id).order_by(Runnable.id.desc())
        return self.manager.runnables_of_user(user_id)
    
runnableManager = RunnableManager()