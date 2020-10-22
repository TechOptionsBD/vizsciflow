import sys

from config import Config
from flask import g

import psutil
from datetime import datetime

from .ogmex import Model, Property, RelatedTo, RelatedFrom
from py2neo import NodeMatcher
from py2neo import Graph
import neotime

from .models import Status, Workflow, LogType, AccessRights, DataType, User
from dsl.fileop import FolderItem

def graph():
    if 'graph' not in g:
        g.graph = Graph(Config.GRAPHDB, username=Config.GRAPHDB_USER, password=Config.GRAPHDB_PASSWORD)
#        g.graph.schema.create_uniqueness_constraint('Workflow', 'workflow_id')
    return g.graph
 
bytes_in_gb = 1024 * 1024
def neotime_duration_to_ms(duration):
    return duration[0] * 2629800000 + duration[1] * 86400000 + duration[2] * 1000 + duration[3]/1000000

def neotime_duration_to_s(duration):
    return neotime_duration_to_ms(duration)/1000

def neotime2StrfTime(date):
    if isinstance(date, neotime.DateTime):
        date = datetime(date.year, date.month, date.day,
                                 date.hour, date.minute, int(date.second),
                                 int(date.second * 1000000 % 1000000),
                                 tzinfo=date.tzinfo)
    return date.strftime("%d-%m-%Y %H:%M:%S")

class NodeItem(Model):
#     __primarykey__ = "id"
    _created_on = Property("created_on")
    _modified_on = Property("modified_on")
    properties = {}
    
    def __init__(self, **kwargs):
        if not self._created_on:
            self._created_on = neotime.DateTime.utc_now()
        if not self._modified_on:
            self._modified_on = neotime.DateTime.utc_now()
         
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
    
    @property
    def created_on(self):
        return self._created_on.to_native()
    @created_on.setter
    def created_on(self, value):
        self._created_on = neotime.DateTime(value.year, value.month, value.day, value.hour, value.minute, value.second, value.tzinfo)
#     
    @property
    def modified_on(self):
        return self._modified_on.to_native()
    @modified_on.setter
    def modified_on(self, value):        
        self._modified_on = neotime.DateTime(value.year, value.month, value.day, value.hour, value.minute, value.second, value.tzinfo)
        
    def json(self):
        
        j = {
            'created_on': str(self.created_on),
            'modified_on': str(self.modified_on),
        }
        j.update(self.properties)
        return j
    
    @staticmethod
    def load(id):
        registry = {'UserItem':UserItem, 'WorkflowItem':WorkflowItem, 'ModuleItem':ModuleItem, 'ValueItem':ValueItem, 'RunnableItem': RunnableItem}
        
        cypher = "MATCH(n) WHERE ID(n)={0} RETURN n".format(id)
        c = graph().run(cypher)
        node = next(iter(c))['n']
        label = list(node.labels)[0]
        if  label in registry:
            return registry[label].wrap(node)

    @staticmethod
    def matchItems(cypher, **parameters):
        registry = {'UserItem':UserItem, 'WorkflowItem':WorkflowItem, 'ModuleItem':ModuleItem, 'ValueItem':ValueItem, 'RunnableItem': RunnableItem}
        
        c = graph().run(cypher, parameters)
        for node in iter(c):
            graphnode = node['n']
            label = list(graphnode.labels)[0]
            if  label in registry:
                yield registry[label].wrap(graphnode)
        
class UserItem(NodeItem):
    user_id = Property("user_id")
    name = Property("username")
    runs = RelatedTo("RunnableItem", "USERRUN")
    workflows = RelatedTo("WorkflowItem", "WORKFLOW")
    datasets = RelatedTo("ValueItem", "ACCESS")
    
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        if not self.name:
            self.name = name
    
    @staticmethod
    def load(user_id):
        if user_id:
            return UserItem.match(graph()).where("_.user_id = {0}".format(user_id)).first()
        else: # this will be very resource-intensive. never call it.
            return list(UserItem.match(graph()).limit(sys.maxsize))

    @staticmethod
    def Create(user_id):
        user = UserItem(User.query.get(user_id).username)
        user.user_id = user_id
        return user
            
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
    modules = RelatedTo("ModuleItem", "MODULE")
    
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        if not self.name:
            self.name = name
    
    def add_module(self, function, package):
        item = ModuleItem(function, package)
        self.modules.add(item)
        graph().push(self)
        return item
            
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
            return list(WorkflowItem.match(graph()).limit(sys.maxsize))
    
    @property
    def Runs(self):
        return list(self.runs)
    
    
class DataItem(NodeItem):
    _value = Property("value", "")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)   
   
    @staticmethod
    def create(value, **kwargs):
        item = DataItem(*kwargs)
        item._value = value
        return item
    
    def json(self):
        j = NodeItem.json(self)
        j['value'] = self._value
        return j
       
class ValueItem(DataItem):
    datatype =  Property("datatype")
    valuetype = Property("valuetype")
    _name = Property('name', 'value')
    
    _inputs = RelatedTo("ModuleItem", "INPUT")
    _outputs = RelatedFrom("ModuleItem", "OUTPUT")
    
    #allocations = RelatedTo("DataAllocationItem", "ALLOCATION")
    users = RelatedFrom(UserItem, 'ACCESS')
    
    def __init__(self, value, valuetype, **kwargs):
        super().__init__(**kwargs)

        self._value = ValueItem.to_primitive(value)
        self.datatype =  str(type(value)) #str(self.__class__.__name__) #val_type#
        self.valuetype = valuetype # if valuetype else str(DataType.Value) #str(type(self.value))
        self._name = 'value'
    
    def name(self):
        return self._name
    
    def set_name(self, value):
        self._name = value
        
    def value(self):
        return self._value
    
    @staticmethod
    def to_primitive(value):
        return value if isinstance(value, (int, float, bool, str)) else str(value)

    @staticmethod
    def create(value, valuetype, **kwargs):
        item = ValueItem(value, valuetype, **kwargs)        
        item._name = "value"
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
            return self._value + other._value
        elif self.valuetype == DataType.File or self.valuetype == DataType.Folder:
            FolderItem(self._value) + other._value
        else:
            raise NotImplementedError
    
    def __sub__(self, other):
        if self.valuetype == "value":
            return self._value - other._value
        elif self.valuetype == DataType.File or self.valuetype == DataType.Folder:
            FolderItem(self._value) - other._value
        else:
            raise NotImplementedError
    
    def __mul__(self, other):
        if self.valuetype == "value":
            return self._value * other._value
        else:
            raise NotImplementedError
    
    def __truediv__(self, other):
        if self.valuetype == "value":
            return self._value / other._value
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
            'name': self._name
        })
        return j
            
    @staticmethod
    def get_by_type_value(valuetype, value):
        return ValueItem.match(graph()).where("_.valuetype={0} AND _.value='{1}'".format(valuetype, value)).first()
    
    @staticmethod
    def load(id = None, path = None):
        if id:
            return ValueItem.match(graph(), id).first()
        else:
            return ValueItem.match(graph()).where("_.value='{0}'".format(path)).first()
    
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
    _name = Property("name")
    
    out = Property("out", "")
    error = Property("error", "")
    view = Property("view", "")
    
    script = Property("script", "")
    status = Property("status", Status.RECEIVED)
    _duration = Property("duration", neotime.Duration())
    arguments = Property("arguments", "")
    provenance = Property("provenance", False)
    
    _modules = RelatedTo("ModuleItem", "MODULE", "id(b)")
    users = RelatedFrom(UserItem, "USERRUN")
    workflows = RelatedFrom(WorkflowItem, "WORKFLOWRUN")
    
    cpu_init = Property("cpu_init", psutil.cpu_percent())
    memory_init = Property("memory_init", (psutil.virtual_memory()[2])/bytes_in_gb)
    
    cpu_run = Property("cpu_run", 0.0)
    memory_run = Property("memory_run", 0.0)
    
    _started_on = Property("started_on", neotime.DateTime.min)
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self._name = name
                    
    @property
    def user_id(self):
        return list(self.users)[0].user_id
    
    @property
    def workflow_id(self):
        return list(self.workflows)[0].workflow_id
    
    @property
    def duration(self):
        if self.status == Status.STARTED:
            self._duration = neotime.DateTime.utc_now() - self._started_on
            #graph().push(self)
            
        return self._duration    
    
    def name(self):
        return self._name
        
    def update(self):
        graph().push(self)
    
    def modules(self):
        return self._modules
        
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
            return list(RunnableItem.match(graph()).limit(sys.maxsize))
    
#     @staticmethod
#     def load_for_users(user_id):
#         user = UserItem.match(graph()).where("_.user_id = {0}".format(user_id)).first()
#         if not user:
#             return []
#         return [r for r in user.runs if not r.provenance]
    
    @staticmethod
    def load_for_users(user_id):        
        cypher = "MATCH (n:RunnableItem)<-[:USERRUN]-(u:UserItem) WHERE u.user_id = $id AND n.provenance = FALSE RETURN n"
        return NodeItem.matchItems(cypher, id=user_id)
        
    def add_module(self, function_name, package):
        item = ModuleItem(function_name, package)
        self._modules.add(item)
        graph().push(self)
        graph().pull(self)
        return item
    
    @staticmethod
    def create(user_id, workflow_id, script, provenance, args):
        user = UserItem.match(graph()).where("_.user_id = {0}".format(user_id)).first()
        if not user:
            user = UserItem.Create(user_id)
        
        dbWorkflow = Workflow.query.get(workflow_id)  
        workflow = WorkflowItem.match(graph()).where("_.workflow_id = {0}".format(workflow_id)).first()
        if not workflow:
            workflow = WorkflowItem(dbWorkflow.name)
            workflow.workflow_id = workflow_id
            user.workflows.add(workflow)
            
        item = RunnableItem(workflow.name)
        item.script = script
        item.args = args
        item.provenance = provenance
        
        user.runs.add(item)
        workflow.runs.add(item)
        
        graph().push(user)
        graph().push(workflow)
        
        graph().push(item)
        return item
        
    @staticmethod
    def load_if(condition = None):
        pass
    
    def update_cpu_memory(self):
        self.cpu_run = psutil.cpu_percent()
        self.memory_run = (psutil.virtual_memory()[2])/bytes_in_gb
        
    def set_status(self, value, update = True):
        self.status = value
        
        if value == Status.STARTED:
            self._started_on = neotime.DateTime.utc_now()
            self.update_cpu_memory()
    
        if value == Status.SUCCESS or value == Status.FAILURE or value == Status.REVOKED:
            self._duration = neotime.DateTime.utc_now() - self._started_on
            self.update_cpu_memory()
        
        if update:
            self.update()
        
    @property        
    def completed(self):
        return self.status == Status.SUCCESS or self.status == Status.FAILURE or self.status == Status.REVOKED
    
    def json(self):
        j = NodeItem.json(self)
        j.update({
            'user_id': self.user_id,
            'workflow_id': self.workflow_id,
            'celery_id': self.celery_id,
            'memory': self.memory_run,
            'cpu': self.cpu_run,
            'out': self.out,
            'error': self.error,
            'view': self.view,
#            'script': self.script,
            'status': self.status,
            'duration': "{0:.3f}".format(neotime_duration_to_s(self.duration)),
            'arguments': str(self.arguments),
            'name': self._name
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
            'err': error,
            'duration': "{0:.3f}".format(neotime_duration_to_s(self.duration)),
            'created_on': neotime2StrfTime(self.created_on),
            'modified_on': neotime2StrfTime(self.modified_on)
        }
        
    def to_json_log(self):
        log = []
        
        for module in self._modules:
            log.append(module.to_json_log())

        return {
            'id': self.id,
            'script': self.script,
            'status': self.status,
            'out': self.out,
            'err': self.error,
            'duration': "{0:.3f}".format(neotime_duration_to_s(self.duration)),
            'log': log
        }
        
    def to_json_info(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self._name,
            'modified_on': neotime2StrfTime(self.modified_on),
            'status': self.status
        }
        
class ModuleItem(NodeItem):
    runs = RelatedFrom(RunnableItem, "MODULE")
    _inputs = RelatedFrom(ValueItem, "INPUT")
    _outputs = RelatedTo("ValueItem", "OUTPUT")
    logs = RelatedTo("TaskLogItem", "LOG", "id(b)")
    
    _name = Property("name", "")
    package = Property("package", "")
    status = Property("status", Status.RECEIVED)
    
    cpu_init = Property("cpu_init", psutil.cpu_percent())
    memory_init = Property("memory_init", (psutil.virtual_memory()[2])/bytes_in_gb)
    
    cpu_run = Property("cpu_run", 0)
    memory_run = Property("memory_run", 0)
    
    _started_on = Property("started_on", neotime.DateTime.min)
    _duration = Property("duration", neotime.Duration())
    
    def __init__(self, name, package = None, **kwargs):
        super().__init__(**kwargs)
        self._name = name
        self.package = package
    
    def json(self):
        j = NodeItem.json(self)
        j.update({
            'event': 'RUN-CREATE',
            'name':self._name,
            'memory': str(self.memory_run),
            'cpu': str(self.cpu_run),
            'status': self.status           
        })
        
        return j 

    def name(self):
        return self._name
        
    def inputs(self):
        return self._inputs
    
    def outputs(self):
        return self._outputs
    
    def prop_from_node(self, node):
        NodeItem.prop_from_node(self, node, "name", "status")
        self.status = node["status"]
        return self
    
    @property
    def run_id(self):
        return list(self.runs)[0].id
           
    @property
    def duration(self):
        if self.status == Status.STARTED:
            self._duration = neotime.DateTime.utc_now() - self._started_on
            #graph().push(self)
            
        return self._duration  
    
    @duration.setter
    def duration(self, value):
        self._duration = value
        
    @staticmethod
    def load(module_id, name = None, package = None):
        if module_id:
            return ModuleItem.match(graph(), module_id).first()
        elif name:
            if not package:
                pkg_func = name.split(".")
                if len(pkg_func) > 1:
                    name = pkg_func[-1]
                    package = ".".join(pkg_func[0:-1])
                else:
                    return ModuleItem.match(graph()).where("_.name='{0}'".format(name)).first()
            
            return ModuleItem.match(graph()).where("_.name='{0}' AND _.package='{1}'".format(name, package)).first()
        
    def start(self):
        self.status = Status.STARTED
        self._started_on = neotime.DateTime.utc_now()
        
        self._duration = neotime.Duration()
        self.memory_run = (psutil.virtual_memory()[2])/bytes_in_gb
        self.cpu_run = psutil.cpu_percent()
                    
        self.add_log(Status.STARTED, LogType.INFO)
        graph().push(self)
    
    def succeeded(self):
        self.status = Status.SUCCESS
        self.add_log(Status.SUCCESS, LogType.INFO)
        self.modified_on = neotime.DateTime.utc_now()
        self._duration = neotime.DateTime.utc_now() - self._started_on
        
        graph().push(self)
    
    def failed(self, log = "Task Failed."):
        self.status = Status.FAILURE
        self.add_log(log, LogType.INFO)
        self.modified_on = datetime.utcnow()
        self._duration = neotime.DateTime.utc_now() - self._started_on
        
        graph().push(self)
                    
    def add_log(self, log, logtype =  LogType.ERROR):
        item = TaskLogItem(log, logtype)
        self.logs.add(item)
        return item
    
    def graph(self):
        pass
    
    def add_arg(self, datatype, value):
        if isinstance(value, ValueItem):
            self._inputs.add(value)
        else:
            for data in self._inputs:
                if data.datatype == datatype and data.value == value:
                    value = data
                    break
            if not value:    
                value = ValueItem.get_by_type_value(datatype, value)
                if not value:
                    data = ValueItem(value, datatype)
                    graph().push(data)
                self._inputs.add(data)

        graph().push(self)
        
        return value
    
    def add_input(self, user_id, datatype, value, rights, **kwargs):
        for data in self._inputs:
            if data.datatype == datatype and data.value == value:
                return data.allocate_for_user(user_id, rights)
                            
        data = ValueItem.get_by_type_value(datatype, value)
        if not data:
            data = ValueItem(value, datatype) #  data = ValueItem(str(value), datatype)
            if "name" in kwargs:
                data.set_name(kwargs['name'])
            graph().push(data)
        
        data.allocate_for_user(user_id, rights)
        
        self._inputs.add(data)
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
                    if len(d) > 2:
                        data.set_name(d[2])
                    data.allocate_for_user(runitem.user_id, AccessRights.Owner)                    
                    graph().push(data)
                else:
                    data.allocate_for_user(runitem.user_id, AccessRights.Write)
                
            self._outputs.add(data)
            result += (d[1],)
        
        graph().push(self)
        
        return result
    
    def to_json_log(self):
        
        data = [{ "datatype": data.valuetype, "data": data._value} for data in self._outputs]
            
        return { 
            'name': self._name if self._name else "", 
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
            'type': self.logtype,
            'log': self.logtext
            })
        
        return j
    
    @staticmethod
    def load(task_id):
        return TaskLogItem.match(graph(), task_id).first()
    
    def updateTime(self):
        self.modified_on = datetime.utcnow()
        graph().push(self)