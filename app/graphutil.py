import sys

from config import Config
from flask import g

import psutil
from datetime import datetime

from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom
from py2neo import NodeMatcher
from py2neo import Graph
import neotime

from .models import Status, Workflow, LogType, AccessRights, DataType
from dsl.fileop import FolderItem

def graph():
    if 'graph' not in g:
        g.graph = Graph(Config.GRAPHDB, username=Config.GRAPHDB_USER, password=Config.GRAPHDB_PASSWORD)
        g.graph.schema.create_uniqueness_constraint('Workflow', 'id')
    return g.graph

bytes_in_gb = 1024 * 1024

def neotime2StrfTime(date):
    if isinstance(date, neotime.DateTime):
        date = datetime(date.year, date.month, date.day,
                                 date.hour, date.minute, int(date.second),
                                 int(date.second * 1000000 % 1000000),
                                 tzinfo=date.tzinfo)
    return date.strftime("%d-%m-%Y %H:%M:%S")

class NodeItem(GraphObject):
#     __primarykey__ = "id"
    created_on = Property("created_on", neotime.DateTime.utc_now())
    modified_on = Property("modified_on", neotime.DateTime.utc_now())
    properties = {}
    
    def __init__(self, **kwargs):
        #self._id = None # this will be set when the item is created or updated from neo4j
         
        # other properties
        if not self.properties:
            for k, v in kwargs. items():
                #self.add_new_prooperty(k, v)
                self.properties[k] = Property(k, v)
                
    def add_new_property(self, name, value):
        self.__class__ = type(
            type(self).__name__, (self.__class__,), {name: Property()}
        )
        setattr(self, name, value)
    
    @property
    def label(self):
        return self.__primarylabel__

    @label.setter
    def label(self, l):
        self.__primarylabel__ = l
            
    @property
    def id(self):
        return self.__primaryvalue__
    
    @staticmethod
    def OrderBy(self, items, key):
        pass

    @staticmethod
    def push(node):
        graph().push(node)
            
    def json(self):
        
        j = {
            'created_on': self.created_on,
            'modified_on': self.modified_on,
            
        }
        j.update(self.properties)
        return j

class UserItem(NodeItem):
    user_id = Property("user_id")
    name = Property("username")
    runs = RelatedTo("RunnableItem", "USERRUN")
    workflows = RelatedTo("WorkflowItem", "WORKFLOW")
    datasets = RelatedTo("ValueItem", "ACCESS")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    @staticmethod
    def load(user_id):
        if user_id:
            return UserItem.match(graph()).where("_.user_id = {0}".format(user_id)).first()
        else: # this will be very resource-intensive. never call it.
            return UserItem.match(graph()).limit(sys.maxsize)

    @property
    def Runs(self):
        return list(self.runs)
    
    @property
    def Workflows(self):
        return list(self.workflows)
            
class WorkflowItem(NodeItem):
    workflow_id = Property("workflow_id")
    name = Property("name")
    user = RelatedFrom("UserItem", "WORKFLOW")
    runs = RelatedTo("RunnableItem", "WORKFLOWRUN")
    symbols = RelatedTo("ValueItem", "SYMBOL")
    
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        if not self.name:
            self.name = name
    
    @staticmethod
    def Create(name):
        workflow = WorkflowItem(name)
        graph().push(workflow)
        return workflow
        
    @staticmethod
    def load(workflow_id):
        if workflow_id:
            return WorkflowItem.match(graph()).where("_.workflow_id = {0}".format(workflow_id)).first()
        else: # this will be very resource-intensive. never call it.
            return WorkflowItem.match(graph()).limit(sys.maxsize)
    
    @property
    def Runs(self):
        return list(self.runs)
    
class DataItem(NodeItem):
    value = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)   
   
    @staticmethod
    def create(value, **kwargs):
        item = DataItem(*kwargs)
        item.value = value
        return item
    
    def json(self):
        j = NodeItem.json(self)
        j['value'] = self.value
        return j
       
class ValueItem(DataItem):
    datatype =  Property("datatype")
    valuetype = Property("valuetype")
    name = Property('name', 'value')
    value = Property('value')
    
    #allocations = RelatedTo("DataAllocationItem", "ALLOCATION")
    users = RelatedFrom(UserItem, 'ACCESS')
    
    def __init__(self, value, valuetype, **kwargs):
        super().__init__(**kwargs)

        if not self.value:
            self.value = value
        if not self.datatype:
            self.datatype =  str(type(value)) #str(self.__class__.__name__) #val_type#
        if not self.valuetype:
            self.valuetype = valuetype # if valuetype else str(DataType.Value) #str(type(self.value))
        if not self.name:
            self.name = 'value'
    
    @staticmethod
    def create(value, valuetype, **kwargs):
        item = ValueItem(value, valuetype, **kwargs)        
        item.name = "value"
        graph().push(item)
        return item
    
    def get_allocation_for_user(self, user_id):
        return next((a for a in self.allocations if a.user_id == user_id), None)

    def allocate_for_user(self, user_id, rights):
        for a in self.users:
            if a.user_id == user_id:
                if rights > a.datasets.get(self, "rights"):
                    a.datasets.remove(self)
                    a.datasets.add(self, rights=rights)
                    graph().push(a)
                return self
            
        user = UserItem.match(graph()).where("_.user_id = {0}".format(user_id)).first()
        user.datasets.add(self, rights=rights)
        graph().push(user)
        return self

    def __add__(self, other):
        if self.valuetype == "value":
            return self.value + other.value
        elif self.valuetype == DataType.File or self.valuetype == DataType.Folder:
            FolderItem(self.value) + other.value
        else:
            raise NotImplementedError
    
    def __sub__(self, other):
        if self.valuetype == "value":
            return self.value - other.value
        elif self.valuetype == DataType.File or self.valuetype == DataType.Folder:
            FolderItem(self.value) - other.value
        else:
            raise NotImplementedError
    
    def __mul__(self, other):
        if self.valuetype == "value":
            return self.value * other.value
        else:
            raise NotImplementedError
    
    def __truediv__(self, other):
        if self.valuetype == "value":
            return self.value / other.value
        else:
            raise NotImplementedError
                    
    def json(self):
        j = DataItem.json(self)
        j.update({
            'event': 'VAL-SAVE',
            'datatype': str(self.datatype),
            'valuetype': self.valuetype,
            'memory': (psutil.virtual_memory()[2])/bytes_in_gb,
            'cpu': (psutil.cpu_percent()),
            'name': self.name
        })
        return j
            
    @staticmethod
    def get_by_type_value(valuetype, value):
        return ValueItem.match(graph()).where("_.valuetype={0} AND _.value='{1}'".format(valuetype, value)).first()
    
    @staticmethod
    def load(item_id):
        return ValueItem.match(graph(), item_id).first()
    
    @staticmethod
    def check_access_rights(user_id, path, checkRights):
        matcher = NodeMatcher(graphgen.graph)
        return matcher.match(id=user_id)
    
    @staticmethod
    def get_access_rights(user_id, path):
        defaultRights = AccessRights.NotSet
        
        if path == os.sep:
            defaultRights = AccessRights.Read # we are giving read access to our root folder to all logged in user

        matcher = NodeMatcher(graphgen.graph)
       
class DataPropertyItem(NodeItem):
    name = Property("name")
    value = Property("value")
    datatype = Property("datatype")
    data = RelatedFrom(ValueItem, "ALLOCATION")
    
    def __init__(self, name, value, **kwargs):
        super().__init__(**kwargs)
        
        if not self.name:
            self.name = str(name)
        if not self.value:
            self.value = value
        if not self.datatype:
            self.datatype = str(type(value))
    
    def json(self):
        j = NodeItem.json(self)
        j.update({
            'event': 'PROP-SAVE',
            'name': self.name,
            'value': str(self.value),
            'datatype': str(self.datatype),
            'memory': (psutil.virtual_memory()[2])/bytes_in_gb,
            'cpu': (psutil.cpu_percent()),
        })
        return j
    
    @staticmethod
    def load(item_id):
        return DataPropertyItem.match(graph(), item_id).first()
    
class RunnableItem(NodeItem): #number1
    celery_id = Property("celery_id", 0)
    name = Property("name")
    
    out = Property("out", "")
    error = Property("error", "")
    
    script = Property("script")
    status = Property("status", Status.RECEIVED)
    duration = Property("duration", 0)
    arguments = Property("arguments")
    
    modules = RelatedTo("ModuleItem", "MODULE")
    users = RelatedFrom(UserItem, "USERRUN")
    workflows = RelatedFrom(WorkflowItem, "WORKFLOWRUN")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    @property
    def user_id(self):
        return list(self.users)[0].user_id
    
    @property
    def workflow_id(self):
        return list(self.workflows)[0].workflow_id
    
    def update(self):
        graph().push(self)
        
    @staticmethod
    def load_runnables_from_cypher(cypher):
        
        runs = []
        c = graph().run(cypher).data()
        for i in c:
            for _,v in i.items():
                runs.append(RunnableItem.load(v.identity))
        return runs
                
    @staticmethod
    def load(run_id = None, workflow_id = None):
        if run_id:
            return RunnableItem.match(graph(), run_id).first()
        elif workflow_id:
            return RunnableItem.match(graph()).where("_.workflow_id = {0}".format(workflow_id)).limit(sys.maxsize)
        else: # this will be very resource-intensive. never call it.
            return RunnableItem.match(graph()).limit(sys.maxsize)
    
    @staticmethod
    def load_for_users(user_id):
        user = UserItem.match(graph()).where("_.user_id = {0}".format(user_id)).first()
        return list(user.runs)
    
    def add_module(self, function_name):
        item = ModuleItem(function_name)
        self.modules.add(item)
        graph().push(self)
        return item
    
    @staticmethod
    def create(user_id, workflow_id, script, args):
        user = UserItem.match(graph()).where("_.user_id = {0}".format(user_id)).first()
        if not user:
            user = UserItem()
            user.user_id = user_id
        
        dbWorkflow = Workflow.query.get(workflow_id)  
        workflow = WorkflowItem.match(graph()).where("_.workflow_id = {0}".format(workflow_id)).first()
        if not workflow:
            workflow = WorkflowItem(dbWorkflow.name)
            workflow.workflow_id = workflow_id
            user.workflows.add(workflow)
            
        item = RunnableItem()
        item.script = script
        item.name = workflow.name
        item.args = args
        
        user.runs.add(item)
        workflow.runs.add(item)
        
        graph().push(user)
        graph().push(workflow)
        
        graph().push(item)
        return item
        
    @staticmethod
    def load_if(condition = None):
        pass
    
    def completed(self):
        return self.status == 'SUCCESS' or self.status == 'FAILURE' or self.status == 'REVOKED'
    
    def json(self):
        j = NodeItem.json(self)
        j.update({
            'user_id': self.user_id,
            'workflow_id': self.workflow_id,
            'celery_id': self.celery_id,
            'memory': (psutil.virtual_memory()[2])/bytes_in_gb,
            'cpu': (psutil.cpu_percent()),
            'out': self.out,
            'error': self.error,
            'script': self.script,
            'status': self.status,
            'duration': self.duration,
            'arguments': str(self.arguments),
            'name': self.name
            })
        return j
       
    def nodes_by_property(self, key = None, value = None, order_by = None):
        moduleItems = []
        cypher = ''
        if not key:
            if not value:
                cypher = "MATCH(n) WHERE ID(n)={0} AND t.name = {1} return t".format(self._id, key) if key else "MATCH(n)-[:MODULE]->(t) WHERE ID(n)={0} return t".format(self._id)
        c = graph().run(cypher)
        for i in c:
            for _, v in i.items():
                moduleItems.append(ModuleItem.load_from_node(v))
        return moduleItems
    
    def to_json_tooltip(self):
        error = ""
        if error:
            error = (self._error[:60] + '...') if len(self.error) > 60 else self.error
        return {
            'id': self.id,
            'name': self._name,
            'status': self.status,
            'error': error,
            'duration': self.duration,
            'created_on': neotime2StrfTime(self.created_on) if self.created_on else '',
            'modified_on': neotime2StrfTime(self.modified_on) if self.modified_on else ''
        }
        
    def to_json_log(self):
        log = []
        
        modules = self.modules
        for module in modules:
            log.append(module.to_json_log())

        return {
            'id': self.id,
            'script': self.script,
            'status': self.status,
            'out': self.out,
            'error': self.error,
            'duration': self.duration,
            'log': log
        }
        
    def to_json_info(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'modified_on': neotime2StrfTime(self.modified_on) if self.modified_on else '',
            'status': self.status
        }
        
class ModuleItem(NodeItem):
    runs = RelatedFrom(RunnableItem, "MODULE")
    inputs = RelatedFrom(ValueItem, "INPUT")
    outputs = RelatedTo("ValueItem", "OUTPUT")
    logs = RelatedTo("TaskLogItem", "LOG")
    
    name = Property("name")
    status = Property("status")
        
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        if not self.name:
            self.name = name
        if not self.status:
            self.status = Status.RECEIVED
    
    def json(self):
        j = NodeItem.json(self)
        j.update({
            'event': 'RUN-CREATE',
            'name':self.name,
            'memory': (psutil.virtual_memory()[2])/bytes_in_gb,
            'cpu': (psutil.cpu_percent()),
            'status': self.status           
        })
        
        return j 
    
    def prop_from_node(self, node):
        NodeItem.prop_from_node(self, node, "name", "status")
        self.status = node["status"]
        return self
    
    @property
    def run_id(self):
        return list(self.runs)[0].id

    @staticmethod
    def load(module_id):
        return ModuleItem.match(graph(), module_id).first()
        
    def start(self):
        self.status = Status.STARTED
        self.created_on = neotime.DateTime.utc_now()
        self.add_log(Status.STARTED, LogType.INFO)
        graph().push(self)
    
    def succeeded(self):
        self.status = Status.SUCCESS
        self.add_log(Status.SUCCESS, LogType.INFO)
        self.modified_on = neotime.DateTime.utc_now()
        graph().push(self)
    
    def failed(self, log = "Task Failed."):
        self.status = Status.FAILURE
        self.add_log(log, LogType.INFO)
        self.modified_on = neotime.DateTime.utc_now()
        graph().push(self)
                    
    def add_log(self, log, logtype =  LogType.ERROR):
        item = TaskLogItem(log, logtype)
        self.logs.add(item)
        return item
    
    def graph(self):
        pass
    
    def add_input(self, user_id, datatype, value, rights):
        for data in self.inputs:
            if data.datatype == datatype and data.value == value:
                return data.allocate_for_user(user_id, rights)
                            
        data = ValueItem.get_by_type_value(datatype, value)
        if not data:
            data = ValueItem(value, datatype)
            graph().push(data)
        
        data.allocate_for_user(user_id, rights)
        
        self.inputs.add(data)
        graph().push(self)
        
        return data
    
    def add_outputs(self, dataAndType):
        runitem = list(self.runs)[0]
        
        result = ()        
        for d in dataAndType:
            data = None
            if not isinstance(d[1], ValueItem):
                data = ValueItem.get_by_type_value(d[0], d[1])
                if not data:
                    data = ValueItem(str(d[1]), d[0], task_id = self.id, job_id = runitem.id, workflow_id = runitem.workflow_id)
                    data.allocate_for_user(runitem.user_id, AccessRights.Owner)                    
                    graph().push(data)
                else:
                    data.allocate_for_user(runitem.user_id, AccessRights.Write)
                
            self.outputs.add(data)
            result += (d[1],)
        
        graph().push(self)
        
        return result
    
    def to_json_log(self):
        
        data = [{ "datatype": data.valuetype, "data": data.value} for data in self.outputs]
            
        return { 
            'name': self.name if self.name else "", 
            'status': self.status,
            'data': data
        }
        
class TaskLogItem(NodeItem):
    logtype = Property("type")
    logtext = Property("logtext")
    
    log = RelatedFrom(ModuleItem)
    
    def __init__(self, log, logtype):
        super().__init__()
        
        if not self.logtype:
            self.logtype = logtype
        
        if not self.logtext:
            self.logtext = log
       
    def json(self):
        j = NodeItem.json(self)
        j.update({
            'event': 'LOG-CREATE',
            'memory': (psutil.virtual_memory()[2])/bytes_in_gb,
            'cpu': (psutil.cpu_percent()),
            'type': self.logtype,
            'log': self.logtext
            })
        
        return j
    
    @staticmethod
    def load(task_id):
        return TaskLogItem.match(graph(), task_id).first()
    
    def updateTime(self):
        self.modified_on = neotime.DateTime.utc_now()
        graph().push(self)