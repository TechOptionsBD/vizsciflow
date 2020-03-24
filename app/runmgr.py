from config import Config

import uuid

from datetime import datetime

from .models import Runnable, Status, Data, Workflow, Task, LogType, DataType
from py2neo import Graph
from py2neo.data import Relationship
from py2neo import NodeMatcher

graphgen = Graph(Config.GRAPHDB, username=Config.GRAPHDB_USER, password=Config.GRAPHDB_PASSWORD)
graphgen.schema.create_uniqueness_constraint('Workflow', 'id')
        
class WorkflowItem(object):
    def __init__(self, user, name, desc, script, access, users, temp, derived):
        self.id = uuid.uuid4()
        self.name = name
        self.desc = desc
        self.script = script
        self.access = access
        self.users = users
        self.temp = temp
        self.derived = derived
    
    def json(self):
        try:
            msg = {
                'event': 'WF-CREATE',
                'id': str(self.id),
                'name': self.name,
                'desc': str(self.desc),
#                 'memory': (psutil.virtual_memory()[2])*(0.000001),
#                 'cpu': (psutil.cpu_percent()),
                'time': str(datetime.utcnow()),
                'error': 'success',
                'temp': str(self.temp),
                'users': self.users,
                'derived': self.derived,
                'label': 'Workflow'
                }
            
            return msg    
        except:
            pass
        

class RunnableItem(object):
    def __init__(self, workflow_id, script, arguments):
        self.id = uuid.uuid4()
        self.workflow_id = workflow_id
        self.celery = 0
        self.created = datetime.utcnow()
        self.modified = datetime.utcnow()
        self.out = ''
        self.err = ''
        self.script = script
        self.status = Status.RECEIVED
        self.duration = 0
        self.arguments = arguments
        
    def get_script(self):
        return self.script
    
    def update(self):
        pass    # update the node
    
    def completed(self):
        return self.status == 'SUCCESS' or self.status == 'FAILURE' or self.status == 'REVOKED'
    
    def json(self):
        try:
            msg = {
                'event': 'RUN-CREATE',
                'id': str(self.id),
                'workflow_id': str(self.workflow_id),
                'celery': str(self.celery),
#                 'memory': (psutil.virtual_memory()[2])*(0.000001),
#                 'cpu': (psutil.cpu_percent()),
                'created': str(self.created),
                'modified': str(self.modified),
                'output': self.out,
                'error': self.err,
                'script': self.script,
                'status': str(self.status),
                'duration': str(self.duration),
                'arguments': str(self.arguments),
                'label': 'Runnable'
                }
            
            return msg    
        except:
            pass  
    
    def update_status(self, status):
        self.status = status
        pass # update the node
    
    def to_json_log(self):
        log = []

        for task in self.tasks:
            log.append(task.to_json_log())

        return {
            'id': self.id,
            'script': self.script,
            'status': self.status,
            'out': self.out,
            'err': self.err,
            'duration': self.duration,
            'log': log
        }
        
    def update_json(self, properties):
        try:
            msg = {
                'event': 'RUN-CREATE',
                'id': str(self.id),
                'workflow_id': str(self.workflow_id),
                'celery': str(self.celery),
#                 'memory': (psutil.virtual_memory()[2])*(0.000001),
#                 'cpu': (psutil.cpu_percent()),
                'created': str(self.created),
                'modified': str(properties['modified']),
                'output': properties['out'],
                'error': self.err,
                'script': self.script,
                'status': str(properties['update_status'],),
                'duration': str(properties['duration']),
                'arguments': str(self.arguments),
                'label': 'Runnable'
                }
            
            return msg    
        except:
            pass 
#         
#         self.modified = properties['modified'],
#         self.output = properties['out'],
#         self.status = properties['update_status'],
#         self.duration = properties['duration']
 

class TaskItem(object):
    def __init__(self, runnable_id, name = None):
        self.id = uuid.uuid4()
        self.name = name
        self.runnable_id = runnable_id
        self.started_on = datetime.utcnow()
        self.ended_on = datetime.utcnow()
        self.status = Status.RECEIVED
        self.data = ''
        
    def update(self):
        pass    # update the node
    
    def start(self):
        self.status = Status.STARTED
        self.started_on = datetime.utcnow()
        self.add_log(Status.STARTED, LogType.INFO)
        self.update()
    
    def succeeded(self, datatype, result):
        self.status = Status.SUCCESS
        self.add_log(Status.SUCCESS, LogType.INFO)
        self.ended_on = datetime.utcnow()
        self.data = result
        self.datatype = datatype
    
    def failed(self, log = "Task Failed."):
        self.status = Status.FAILURE
        self.datatype = DataType.Unknown
        self.add_log(log, LogType.ERROR)
        self.add_log(Status.FAILURE, LogType.INFO)        
        self.ended_on = datetime.utcnow()
                    
    def add_log(self, log, logtype =  LogType.ERROR):
        tasklog = TaskLogItem(self.id, logtype, log)
        tasklog.save()
        
    def to_json_log(self):
        data = self.data
        if data and data.startswith('[') and data.endswith(']'):
            data = data[1:]
            data = data[:-1]
            
        log = { 
            'name': self.name if self.name else "", 
            'datatype': self.datatype, 
            'status': self.status,
            'data': data
        }
        if self.status == Status.SUCCESS and (self.datatype & DataType.FileList) > 0:
            log['data'] = log['data'].strip('}{').split(',')
        return log
    

class TaskLogItem(object):
    def __init__(self, task_id, logtype, log):
        self.id = uuid.uuid4()
        self.task_id = task_id
        self.time = datetime.utcnow()
        self.type = logtype
        self.log = log
    
    def update(self):
        pass
    def updateTime(self):
        self.time = datetime.utcnow()
    
class GraphModuleManager():
    @staticmethod
    def Create(workflow_id, script, args):
        return Runnable.create(workflow_id, script, args)
    
    @staticmethod
    def Save(dataitem):
        return graphgen.graph.run(
            statement="CREATE (x) SET x = {dict_param}",
            parameters={'dict_param': dataitem})
        
        matcher = NodeMatcher(graphgen.graph)
        return matcher.match(id=dataitem['id']).first()
    
    @staticmethod
    def SavePermission(user, rights, dataitem):
        dataitem["user"] = str(user)
        dataitem["rights"] = str(rights)
        
        return GraphPersistance.Save(dataitem)       
  
    @staticmethod
    def SaveMetadata(data, metadata):
        
        metadatanode = GraphPersistance.Save(metadata)
        return Relationship(data, "METADATA", metadatanode)
    
    @staticmethod
    def create_runnable(user_id, workflow_id, script, args):
        runnable = RunnableItem(workflow_id, script, args)
        run = graphgen.graph.run("CREATE (x) SET x = {dict_param}",{'dict_param': runnable.json()})
#         runnable = graphgen.graph.run(
#             statement="CREATE (x) SET x = {dict_param}",
#             parameters={'dict_param': runnable.json()})

        #a = graphgen.graph.run("MATCH (x) WHERE x.script = {dict_param} RETURN ID(x)",{'dict_param': runnable.get_script()})
        result = graphgen.graph.run("MATCH (x) WHERE x.script = {dict_param} RETURN ID(x), properties(x)",{'dict_param': runnable.get_script()}).data()
        
        # check here that result is a list with a single item
        # if not raise ValueError("Expected one runnable, but getting more")
#         node_id = a.identity
        matcher = NodeMatcher(graphgen.graph)
        
        return result[0]
    
#     @staticmethod
#     def get_workflow(workflow_id):
#         matcher = NodeMatcher(graphgen.graph)
#         return matcher.match(id=workflow_id).first()




    @staticmethod
    def update_runnable(properties):
        try:
            runnable = RunnableItem(properties['workflow_id'], properties['script'], properties['arguments'])
            workflow = properties['workflow_id']
            result = runnable.update_json(properties)            
            print(result)
            run = graphgen.graph.run("MATCH (x) WHERE x.workflow_id = {dict_param} SET x = {dict_param2}",{'dict_param': workflow, 'dict_param2': result}).data()
            return run
        except Exception as e:
            return e
    
#     @staticmethod
#     def create_task(runnable, function_name):
#         try:
#             pass
#         except Exception as e:
#             return e
    
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

    
    def get_runnable(self, runnable_id):
        return self.manager.get_runnable(runnable_id)

class DBModuleManager():
    
    @staticmethod
    def Save(dataitem):
        return Data.add(dataitem.json())
    
    @staticmethod
    def SavePermission(user, rights, dataitem):
        data = DBPersistance.Save(dataitem)
        return DataAllocation.add(user, data.id, rights)
    
    @staticmethod
    def SaveMetadata(data, user, rights, json):
        metadata = Data.add(json)
        DataAllocation.add(user, metadata.id, rights)
        return Property.add(data.id, metadata.id)
    
    @staticmethod
    def get_workflow(workflow_id):
        return Workflow.query.get(workflow_id)
    
    @staticmethod
    def create_workflow(user_id, name, desc, script, access, users, temp, derived = 0):
        return Workflow.create(user_id, name, desc if desc else '', script, 2 if not access else int(access), users, temp, derived)
    
    @staticmethod
    def create_runnable(user_id, workflow_id, script, args):
        return Runnable.create(workflow_id, script, args)
    
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