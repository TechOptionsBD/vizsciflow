from config import Config

import uuid

from datetime import datetime

from .models import Runnable, Status, Data, Workflow, Task, LogType, DataType
from py2neo import Graph, Node, NodeMatcher
from py2neo.data import Relationship
import neotime

graphgen = Graph(Config.GRAPHDB, username=Config.GRAPHDB_USER, password=Config.GRAPHDB_PASSWORD)
graphgen.schema.create_uniqueness_constraint('Workflow', 'id')

def neotime2StrfTime(date):
    if isinstance(date, neotime.DateTime):
        date = datetime(date.year, date.month, date.day,
                                 date.hour, date.minute, int(date.second),
                                 int(date.second * 1000000 % 1000000),
                                 tzinfo=date.tzinfo)
    return date.strftime("%d-%m-%Y %H:%M:%S")        
# class WorkflowItem(object):
#     def __init__(self, user, name, desc, script, access, users, temp, derived):
#         self.id = uuid.uuid4()
#         self.name = name
#         self.desc = desc
#         self._script = script
#         self.access = access
#         self.users = users
#         self.temp = temp
#         self.derived = derived
#     
#     def json(self):
#         try:
#             msg = {
#                 'event': 'WF-CREATE',
#                 'id': str(self.id),
#                 'name': self.name,
#                 'desc': str(self.desc),
# #                 'memory': (psutil.virtual_memory()[2])*(0.000001),
# #                 'cpu': (psutil.cpu_percent()),
#                 'time': str(neotime.DateTime.utc_now()),
#                 'error': 'success',
#                 'temp': str(self.temp),
#                 'users': self.users,
#                 'derived': self.derived
#                 }
#             
#             return msg    
#         except:
#             pass
        

class RunnableItem(object):
    def __init__(self, user_id, workflow_id, script, arguments):
        self.__id = None # this will be set when the item is created or updated from neo4j
        
        self.__user_id = user_id
        self.__workflow_id = workflow_id
        self.__celery_id = 0
        self.__created = neotime.DateTime.utc_now()
        self.__modified = neotime.DateTime.utc_now()
        self.__out = ''
        self.__err = ''
        self.__script = script
        self.__status = Status.RECEIVED
        self.__duration = 0
        self.__arguments = arguments
    
        self.__updateQueue = []
    
    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, id):
        self.__id = id
        
    @property
    def workflow_id(self):
        return self.__workflow_id
    
    @property
    def celery_id(self):
        return self.__celery_id
    @celery_id.setter
    def celery_id(self, celery_id):
        self.__celery_id = celery_id
        self.__updateQueue.append("celery_id")
    
    @property
    def out(self):
        return self.__out
    @out.setter
    def out(self, out):
        self.__out = out
        self.__updateQueue.append("out")
    
    @property
    def err(self):
        return self.__err
    @err.setter
    def err(self, err):
        self.__err = err
        self.__updateQueue.append("err")
        
    @property
    def duration(self):
        return self.__duration
    @duration.setter
    def duration(self, duration):
        self.__duration = duration
        self.__updateQueue.append("duration")
        
    @property
    def status(self):
        return self.__status
    @status.setter
    def status(self, status):
        self.__status = status
        self.__updateQueue.append("status")
    
    @property
    def script(self):
        return self.__script
    @script.setter
    def script(self, script):
        self.__script = script
        self.__updateQueue.append("script")
    
    @property
    def created_on(self):
        return self.__created
        
    @property
    def modified(self):
        return self.__modified
    @modified.setter
    def modified(self, modified):
        self.__modified = modified
        self.__updateQueue.append("modified")
        
    def update(self):
        if not self.__updateQueue:
            return
        
        self.modified = neotime.DateTime.utc_now()
        
        runnableNode = NodeMatcher(graphgen).get(self.id)
        for u in self.__updateQueue:
            if u == 'status':
                runnableNode[u] = self.__status
            elif u == 'out':
                runnableNode[u] = self.__out
            elif u == 'err':
                runnableNode[u] = self.__err
            elif u == 'duration':
                runnableNode[u] = self.__duration
            elif u == 'modified':
                runnableNode[u] = self.__modified
            elif u == 'celery_id':
                runnableNode[u] = self.__celery_id
            else:
                raise NotImplementedError
                
        graphgen.push(runnableNode)
        self.__updateQueue.clear()
        
    @staticmethod
    def load(runnable_id):
        nodeMatcher = NodeMatcher(graphgen)
        runnableNode = nodeMatcher.get(runnable_id)
        runnable = RunnableItem(runnableNode["user_id"], runnableNode["workflow_id"], runnableNode["script"], runnableNode["arguments"])
        runnable.__id = runnableNode.identity
        runnable.__created = runnableNode["created"]
        runnable.__modified = runnableNode["modified"]
        runnable.__out = runnableNode["out"]
        runnable.__err = runnableNode["err"]
        runnable.__script = runnableNode["script"]
        runnable.__status = runnableNode["status"]
        runnable.__duration = runnableNode["duration"]
        runnable.__arguments = runnableNode["arguments"]
        runnable.__celery_id = runnableNode["celery_id"]
        
        return runnable
        
    def completed(self):
        return self.__status == 'SUCCESS' or self.__status == 'FAILURE' or self.__status == 'REVOKED'
    
    def json(self):
        return {
            'event': 'RUN-CREATE',
            #'id': str(self.id),
            'user_id': self.__user_id,
            'workflow_id': self.__workflow_id,
            'celery_id': self.__celery_id,
#                 'memory': (psutil.virtual_memory()[2])*(0.000001),
#                 'cpu': (psutil.cpu_percent()),
            'created': self.__created,
            'modified': self.__modified,
            'output': self.__out,
            'error': self.__err,
            'script': self.__script,
            'status': self.__status,
            'duration': self.__duration,
            'arguments': str(self.__arguments)
            }
        
    @property
    def tasks(self):
        taskItems = []
        c = graphgen.run("MATCH(n)-[:TASK]->(t) WHERE ID(n)={0} return t".format(self.__id)).data()
        for i in c:
            for k, v in i.items():
                taskItems.append(TaskItem.load(v))
        return taskItems
    
    def to_json_tooltip(self):
        name = Workflow.query.get(self.__workflow_id).name
        err = ""
        if err:
            err = (self.__err[:60] + '...') if len(self.__err) > 60 else self.__err
        return {
            'id': self.__id,
            'name': name,
            'status': self.__status,
            'err': err,
            'duration': self.__duration,
            'created_on': neotime2StrfTime(self.__created) if self.__created else '',
            'modified_on': neotime2StrfTime(self.__modified) if self.__modified else ''
        }
        
    def to_json_log(self):
        log = []
        
        tasks = self.tasks
        for task in tasks:
            log.append(task.to_json_log())

        return {
            'id': self.id,
            'script': self.__script,
            'status': self.__status,
            'out': self.__out,
            'err': self.__err,
            'duration': self.__duration,
            'log': log
        }
        
    def to_json_info(self):
        name = Workflow.query.get(self.__workflow_id).name
        return {
            'id': self.__id,
            'user_id': self.__user_id,
            'name': name,
            'modified': neotime2StrfTime(self.modified) if self.modified else '',
            'status': self.status
        }
        
        
class TaskItem(object):
    def __init__(self, name):
        self.id = None
        self.name = name
        self.started_on = neotime.DateTime.utc_now()
        self.ended_on = neotime.DateTime.utc_now()
        self._status = Status.RECEIVED
    
    def json(self):
        msg = {
            'event': 'RUN-CREATE',
            'name':self.name,
            #'id': str(self.id),
#                 'memory': (psutil.virtual_memory()[2])*(0.000001),
#                 'cpu': (psutil.cpu_percent()),
            'started_on': self.started_on,
            'ended_on': self.ended_on,
            'status': self._status           
        }
        
        return msg 
    
    @property
    def runnable_id(self):
        c = graphgen.run("MATCH(n)-[:TASK]->(t) WHERE ID(t)={0} return ID(n)".format(self.id))
        c.forward()
        return c.current[0]

    @staticmethod
    def load(taskNode):
        taskItem = TaskItem(taskNode["name"])
        taskItem.id = taskNode.identity
        taskItem.started_on = taskNode["started_on"]
        taskItem.ended_on = taskNode["ended_on"]
        taskItem._status = taskNode["status"]
        return taskItem
    
    def start(self):
        self._status = Status.STARTED
        self.started_on = neotime.DateTime.utc_now()
        
        nodeMatcher = NodeMatcher(graphgen)
        taskNode = nodeMatcher.get(self.id)

        taskNode["status"] = self._status
        taskNode["started_on"] = self.started_on
        graphgen.push(taskNode)
        
        self.add_log(Status.STARTED, LogType.INFO)
    
    def succeeded(self):
        self._status = Status.SUCCESS
        self.add_log(Status.SUCCESS, LogType.INFO)
        self.ended_on = neotime.DateTime.utc_now()
        
        nodeMatcher = NodeMatcher(graphgen)
        taskNode = nodeMatcher.get(self.id)
        
        taskNode["status"] = self._status
        taskNode["ended_on"] = self.ended_on
        graphgen.push(taskNode)
    
    def failed(self, log = "Task Failed."):
        self._status = Status.FAILURE
        self.add_log(log, LogType.INFO)
        self.ended_on = neotime.DateTime.utc_now()
        
        taskNode = self.Node()
        
        taskNode["status"] = self._status
        taskNode["ended_on"] = self.ended_on
        graphgen.push(taskNode)
                    
    def add_log(self, log, logtype =  LogType.ERROR):
        item = TaskLogItem(log, logtype)
        taskLogNode = Node("TaskLog", **item.json())
        
        taskTaskLogRel = Relationship(self.Node(), "LOG", taskLogNode)
        
        tx = graphgen.begin()
        tx.create(taskLogNode)
        tx.create(taskTaskLogRel)
        tx.commit()
        
        item.id = taskLogNode.identity
        return item
    
    @property
    def outputs(self):
        from .datamgr import ValueItem
        dataItems = []
        c = graphgen.run("MATCH(n:Task)-[:OUTPUT]->(t) WHERE ID(n)={0} return t".format(self.id)).data()
        for i in c:
            for k, v in i.items():
                dataItems.append(ValueItem.load(v))
        return dataItems
        
    def to_json_log(self):
        
        data = [{ "datatype": data.valuetype, "data": data.value} for data in self.outputs]
            
        return { 
            'name': self.name if self.name else "", 
            'status': self._status,
            'data': data
        }
    
    def Node(self):
        if not self.id:
            raise ValueError("Task item is not saved to neo4j yet.")
        return NodeMatcher(graphgen).get(self.id)
    
class TaskLogItem(object):
    def __init__(self, log, logtype):
        self.id = None
        self.time = neotime.DateTime.utc_now()
        self.type = logtype
        self.log = log
    
    def json(self):
        msg = {
            'event': 'RUN-CREATE',
            #'id': str(self.id),
#                 'memory': (psutil.virtual_memory()[2])*(0.000001),
#                 'cpu': (psutil.cpu_percent()),
            'time': self.time,
            'type': self.type,
            'log': self.log
            }
        
        return msg 
    
    def updateTime(self):
        self.time = neotime.DateTime.utc_now()
        logNode = self.Node()
        logNode['time'] = self.time
        graphgen.push(logNode)
        
    def Node(self):
        if not self.id:
            raise ValueError("Task log item is not saved to neo4j yet.")
        return NodeMatcher(graphgen).get(self.id)
    
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
        item = RunnableItem(user_id, workflow_id, script, args)
        runnableNode = Node("Runnable", **item.json())
        
        tx = graphgen.begin()
        tx.create(runnableNode)
        tx.commit()
        item.id = runnableNode.identity
        return item
    
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
        item = TaskItem(function_name)
        taskNode = Node("Task", **item.json())
        
        nodes_matcher = NodeMatcher(graphgen)
        runnableNode = nodes_matcher.get(runnable_id)
        
        runnableTask = Relationship(runnableNode, "TASK", taskNode)
        
        tx = graphgen.begin()
        tx.create(taskNode)
        tx.create(runnableTask)
        tx.commit()
        item.id = taskNode.identity
        return item
    
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
        runnableItems = []
        c = graphgen.run("MATCH(n:Runnable) WHERE n['user_id'] = {0} RETURN ID(n)".format(user_id)).data()
        for i in c:
            for k, v in i.items():
                runnableItems.append(RunnableItem.load(v))
        return runnableItems

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