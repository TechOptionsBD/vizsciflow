from config import Config
from flask import g

import psutil
from datetime import datetime

from py2neo import NodeMatcher
from py2neo import Graph, Node, Relationship
import neotime

from .models import Status, Workflow, LogType, AccessRights, DataType
from dsl.fileop import FolderItem

def graph():
    if 'graph' not in g:
        g.graph = Graph(Config.GRAPHDB, username=Config.GRAPHDB_USER, password=Config.GRAPHDB_PASSWORD)
        g.graph.schema.create_uniqueness_constraint('Workflow', 'id')
    return g.graph

def load_node(node_id):
    return NodeMatcher(graph()).get(node_id)    
            
bytes_in_gb = 1024 * 1024

def neotime2StrfTime(date):
    if isinstance(date, neotime.DateTime):
        date = datetime(date.year, date.month, date.day,
                                 date.hour, date.minute, int(date.second),
                                 int(date.second * 1000000 % 1000000),
                                 tzinfo=date.tzinfo)
    return date.strftime("%d-%m-%Y %H:%M:%S")

class NodeItem():
    def __init__(self, **kwargs):
        
        self._id = None # this will be set when the item is created or updated from neo4j
        
        self._created_on = neotime.DateTime.utc_now()
        self._modified_on = neotime.DateTime.utc_now()

        # other properties
        self._properties = {}
        for k, v in kwargs.items():
            self._properties[k] = v
    
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, newid):
        self._id = newid
    
    @property
    def modified_on(self):
        return self._modified_on
    @modified_on.setter
    def modified_on(self, modified_on):
        self._modified_on = modified_on
            
    @property
    def created_on(self):
        return self._created_on
    
    @property
    def properties(self):
        return self._properties
    
    @staticmethod
    def OrderBy(self, items, key):
        pass
    
    def json(self):
        
        j = {
            'created_on': self._created_on,
            'modified_on': self._modified_on,
            
        }
        j.update(self._properties)
        return j
    
    def prop_from_node(self, node, *args):
        self._id = node.identity
        self._created_on = node["created_on"]
        self._modified_on = node["modified_on"]
        
        args = list(args)
        args.extend(["id", "created_on", "modified_on"])
        for k, v in node.items():
            if not k in args:
                self._properties[k] = v
        return self
        
    def Node(self):
        if not self.id:
            raise ValueError("Node item is not saved to neo4j yet.")
        return load_node(self.id)
    
class DataItem(NodeItem):
    def __init__(self, value, **kwargs):
        super().__init__(**kwargs)
        
        self._value = value
    
    @property
    def value(self):
        return self._value
    
    def json(self):
        j = NodeItem.json(self)
        j['value'] = self._value
        return j
    
    def prop_from_node(self, node, *args):
        self._value = node["value"]
        
        args = list(args)
        args.append("value")
        return NodeItem.prop_from_node(self, node, *args)
    
#     def __getitem__(self, key):
#         return getattr(self, key)
#     
#     def __setitem__(self, key, item):
#         self.data[key] = item
        
class ValueItem(DataItem):

    def __init__(self, value, valuetype, **kwargs):
        super().__init__(value, **kwargs)
        # type: (Any) -> None

        self.datatype =  type(value) #str(self.__class__.__name__) #val_type#
        self.valuetype = valuetype # if valuetype else str(DataType.Value) #str(type(self.value))
        self.name = 'value'
    
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
    
    def prop_from_node(self, node, *args):
        self.datatype = node["datatype"]
        self.datatype = node["valuetype"]
        self.datatype = node["name"]
        self.datatype = node["path"]
        args = list(args)
        args.extend(["datatype", "valuetype", "name", "path", "memory", "cpu"])
        return DataItem.prop_from_node(self, node, *args)
        
    @staticmethod
    def get_by_type_value(valuetype, value):
        c = graph().run("MATCH(d:Data) WHERE d['valuetype'] = {0} AND d['value'] = '{1}' RETURN d".format(valuetype, value)).data()
        if c:
            return ValueItem.load_from_node(next(iter(c))['d'])

    @staticmethod
    def load_from_node(dataNode):
        valueItem = ValueItem(dataNode["value"], dataNode["valuetype"])
        return valueItem.prop_from_node(dataNode)
    
    @staticmethod
    def load(item_id):
        return ValueItem.load_from_node(load_node(item_id))
    
#     @property
#     def properties(self):
#         c = graph().run("MATCH(d:Data)-[:PROPERTY]->(p) WHERE ID(d) = {0} RETURN p".format(self.id)).data()
#         if c:
#             for _,v in c:
#                 yield DataPropertyItem.load_from_node(v['p'])
    
# class FileItem(ValueItem):
# 
#     def __init__(self, f, ds_id = None):
#         self.ds_id = ds_id
#         super().__init__(f, DataType.File)
#         
#         if not self.ds_id:
#             ds = Utility.ds_by_prefix(f)
#             if ds:
#                 self.ds_id = ds.id
#         
#     def json(self):
#         v = super().json()
#         v["ds"] = str(self.ds_id) 
#         v["name"] = "file"
#         return v

class DataAllocationItem(NodeItem):

    def __init__(self, user_id, access):
        super().__init__()
        self.user_id = user_id
        self._access = access

    @staticmethod
    def add(user_id, access):
        dataAllocation = DataAllocationItem(user_id, access)
        dataAllocationNode =  Node('Allocation', **dataAllocation.json())
        graph().create(dataAllocationNode)
        dataAllocation.id = dataAllocationNode.identity
        return dataAllocation
                
    def json(self):
        j = NodeItem.json(self)
        j.update({
            'event': 'DATA-ALLOC',
            'user_id': self.user_id,
            'access': self._access,
            'memory': (psutil.virtual_memory()[2])/bytes_in_gb,
            'cpu': (psutil.cpu_percent())
        })
        return j
    
    def prop_from_node(self, node):
        NodeItem.prop_from_node(self, node, "user_id", "access")
        self.user_id = node["user_id"]
        self._access = node["access"]
        return self
    
    @staticmethod
    def load_by_data_user(data_id, user_id):
        c = graph().run("MATCH(n:Data)-[:ALLOCATION]->(a:Allocation) WHERE ID(n) = {0} AND a['user_id'] = {1} RETURN a".format(data_id, user_id)).data()
        if c:
            return DataAllocationItem.load_from_node(next(iter(c))['a'])
        
    @staticmethod
    def load_from_node(allocNodeItem):
        allocItem = DataAllocationItem(allocNodeItem["user_id"], allocNodeItem["access"])
        return allocItem.prop_from_node(allocNodeItem)
    
    @property
    def access(self):
        return self._access

    @access.setter    
    def access(self, access):        
        self._access = access           
        self._modified_on = neotime.DateTime.utc_now()
        allocNode = self.Node()
        allocNode["access"] = self._access
        allocNode["modified_on"] = self._modified_on
        graph().push(allocNode)
        
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

    def __init__(self, name, value, **kwargs):
        super().__init__(**kwargs)
        self._name = str(name)
        self._value = value
        self._datatype = type(value)
    
    @property
    def name(self):
        return self._name
    
    def json(self):
        j = NodeItem.json(self)
        j.update({
            'event': 'PROP-SAVE',
            'name': self._name,
            'value': str(self._value),
            'datatype': str(self._datatype),
            'memory': (psutil.virtual_memory()[2])/bytes_in_gb,
            'cpu': (psutil.cpu_percent()),
        })
        return j
    
    def prop_from_node(self, node):
        NodeItem.prop_from_node(self, node, "datatype")
        self._datatype = node["datatype"]
        return self
    
    @staticmethod
    def load_from_node(propertyNode):
        prop = DataPropertyItem(propertyNode["name"], propertyNode["value"])
        return prop.prop_from_node(propertyNode)
    
    @staticmethod
    def load(item_id):
        return DataPropertyItem.load_from_node(load_node(item_id))
    
# class FolderItem(FileItem):
# 
#     def __init__(self, f, ds_id = None):
#         super().__init__(f, ds_id)
#         self.valuetype = DataType.Folder
#         
#     def json(self):
#         v = super().json()
#         v["name"] = "folder"
#         return v

# class GraphPermission(object):
# 
#     def __init__(self, rights):
#         self.id = uuid.uuid4()
#         self.label = "Permission"
#         self.rights = rights
#         
#     def json(self):
#         try:
#             msg = {
#                 'event': 'PERM-SAVE',
#                 'id': str(self.id),
#                 'rights': str(self.rights),
#                 'time': str(neotime.DateTime.utc_now()),
#                 'error': 'success'
#             }
#             
#             return msg    
#         except:
#             pass
#         
# class ModuleItem(ValueItem):
# 
#     def __init__(self, f):
#         super().__init__(f, DataType.Module)
#         
#     def json(self):
#         v = super().json()
#         v["name"] = "folder"
#         return v
#     
#     def startLogMsg(self, user):
#         msg = {
#             'event': 'MOD-STRT',
#             'id': str(self.id),
#             'user': user
#         }
#         #deb.debug(jsonify(msg))
#         return msg
# 
#     def endLogMsg(self):
#         msg = {
#             'event': 'MOD-END',
#             'id': str(self.id),
#             'user': str(self.user)
#         }
# 
#         #deb.debug(jsonify(msg))
#         return msg
#         
# 
#     def body(self):
#         """
#         :param interfaceParam:
#         :return:
#         """
# 
#     def run(self, *args):
# 
#         start_time = neotime.DateTime.utc_now()
# 
#         self.P = args
# 
#         try:
#             param_ids = []
# 
#             for i in args:
# 
#                 if isinstance(i, Object) or isinstance(i, File) or isinstance(i, Document):
#                     param_ids.append(str(i.id))
# 
#                 else:
#                     param_ids.append(str(i))
# 
# 
# 
#             msg = {
#                 'p@': param_ids,
#                 'event': 'MOD-CRTN',
#                 'id': str(self.id),
#                 'name': str(self.__class__.__name__),
#                 'user': str(USER.id),
#                 'memory_init': (psutil.virtual_memory()[2])*(.000001),
#                 'cpu_init': (psutil.cpu_percent()),
#                 'duration_init': str(neotime.DateTime.utc_now()-start_time),
#                 'time': str(neotime.DateTime.utc_now()),
#                 'cpu_run': 0,
#                 'memory_run': 0,
#                 'duration_run': "00:00:00.000000",
#                 'error': 'success'
#             }
# 
#             deb.debug(jsonify(msg))
# 
#             elasticmodule(msg['id'], msg['time'], msg['name'], msg['user'], msg['memory_run'], msg['memory_init'], msg['cpu_run'], msg['cpu_init'], msg['duration_run'], msg['duration_init'], msg['error'])
# 
#             ''' GDB part '''
#             props = ['NAME:\"' + msg['name'] + '\"', 'id:\"' + msg['id'] + '\"',
#                      'user:\"' + msg['user'] + '\"', 'error:\"null\"', 'time:\"' + str(msg['time']) + '\"', 'memory_init:\"' + str(msg['memory_init']) + '\"',
#                      'cpu_init:\"' + str(msg['cpu_init']) + '\"', 'duration_init:\"' + str(msg['duration_init']) + '\"',
#                      'duration_run:\"' + str(msg['duration_run']) + '\"', 'memory_run:\"' + str(msg['memory_run']) + '\"', 'cpu_run:\"' + str(msg['cpu_run']) + '\"',
#                      'label:\"' + str(msg['label']) + '\"']
#             propsQuery = ','.join(props)
#             #print propsQuery
#             query = 'create (n:Module{' + propsQuery + '})'
#             graph.run(query)
# 
# 
#             ''' relationships '''
#             for uninqid in param_ids:
#                 # match (n:Object{id:uniqid}), (m:Module{id:id})
#                 # create (n)-[:IN]-> (m)
# 
#                 query = ' match (n),(m) where n.id = \"' + uninqid + '\" and m.id = \"' + msg['id'] + '\" create (n)-[:IN]-> (m)'
#                 #print query
#                 graph.run(query)
#         except:
#             pass
    
        
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
     

class RunnableItem(NodeItem):
    def __init__(self, user_id, workflow_id, script, arguments, **kwargs):
        super().__init__(**kwargs)
        
        # RDBMS info
        self._user_id = user_id
        self.__workflow_id = workflow_id
        self.__celery_id = 0
        self._name = Workflow.query.get(self.__workflow_id).name
        
        self._out = ''
        self._error = ''
        
        self._script = script
        self._status = Status.RECEIVED
        self.__duration = 0
        self.__arguments = arguments
    
        self._updateQueue = []

    @property
    def modified_on(self):
        return NodeItem.modified_on
    @modified_on.setter
    def modified_on(self, modified_on):
        self._modified_on = modified_on
        self.updateQueue.append("modified_on")

    @property
    def arguments(self):
        return self.__arguments
    @arguments.setter
    def arguments(self, arguments):
        self.__arguments = arguments
        self._updateQueue.append("arguments")
    
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name
        self._updateQueue.append("name")
            
    @property
    def user_id(self):
        return self._user_id
    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id
        self._updateQueue.append("user_id")
                        
    @property
    def workflow_id(self):
        return self.__workflow_id
    
    @property
    def celery_id(self):
        return self.__celery_id
    @celery_id.setter
    def celery_id(self, celery_id):
        self.__celery_id = celery_id
        self._updateQueue.append("celery_id")
    
    @property
    def out(self):
        return self._out
    @out.setter
    def out(self, out):
        self._out = out
        self._updateQueue.append("out")
    
    @property
    def err(self):
        return self._error
    @err.setter
    def err(self, error):
        self._error = error
        self._updateQueue.append("error")
        
    @property
    def duration(self):
        return self.__duration
    @duration.setter
    def duration(self, duration):
        self.__duration = duration
        self._updateQueue.append("duration")
        
    @property
    def status(self):
        return self._status
    @status.setter
    def status(self, status):
        self._status = status
        self._updateQueue.append("status")
    
    @property
    def script(self):
        return self._script
    @script.setter
    def script(self, script):
        self._script = script
        self._updateQueue.append("script")
    
    @property
    def updateQueue(self):
        return self._updateQueue
    @updateQueue.setter
    def updateQueue(self, updateQueue):
        self._updateQueue = updateQueue
        self._updateQueue.append("updateQueue")
            
    def update(self):
        if not self.updateQueue:
            return
        
        self._modified_on = neotime.DateTime.utc_now()
        
        runnableNode = load_node(self.id)
        for u in self.updateQueue:
            if u == 'status':
                runnableNode[u] = self._status
            elif u == 'out':
                runnableNode[u] = self._out
            elif u == 'error':
                runnableNode[u] = self._error
            elif u == 'duration':
                runnableNode[u] = self.__duration
            elif u == 'modified_on':
                runnableNode[u] = self._modified_on
            elif u == 'celery_id':
                runnableNode[u] = self.__celery_id
            else:
                raise NotImplementedError
                
        graph().push(runnableNode)
        self._updateQueue.clear()
    
    def prop_from_node(self, node):
        NodeItem.prop_from_node(self, node, "user_id", "workflow_id", "out", "error", "script", "status", "duration", "celery_id", "name", "arguments")
        self._out = node["out"]
        self._error = node["error"]
        self._status = node["status"]
        self._duration = node["duration"]
        self._arguments = node["arguments"]
        self._celery_id = node["celery_id"]
        self._name = node["name"]
        return self
    
    @staticmethod
    def load_from_node(runnableNode):
        runnable = RunnableItem(runnableNode["user_id"], runnableNode["workflow_id"], runnableNode["script"], runnableNode["arguments"])
        return runnable.prop_from_node(runnableNode)
    
    @staticmethod
    def load_runnables_from_cypher(cypher):
        runs = []
        c = graph().run(cypher).data()
        for i in c:
            for _,v in i.items():
                runs.append(RunnableItem.load_from_node(v))
        return runs
                
    @staticmethod
    def load(run_id = None, workflow_id = None):
        if run_id:
            return RunnableItem.load_from_node(load_node(run_id))
        elif workflow_id:
            return RunnableItem.load_runnables_from_cypher("MATCH(n:Run) WHERE n.workflow_id = {0} RETURN n".format(int(workflow_id)))
        else:
            return RunnableItem.load_runnables_from_cypher("MATCH(n:Run) RETURN n")
    
    @staticmethod
    def load_for_users(user_id):
        runnableItems = []
        c = graph().run("MATCH(n:Run) WHERE n['user_id'] = {0} RETURN n".format(user_id)).data()
        for i in c:
            for _, v in i.items():
                runnableItems.append(RunnableItem.load_from_node(v))
        return runnableItems
    
    def add_module(self, function_name):
        item = ModuleItem(function_name)
        moduleNode = Node("Module", **item.json())
              
        runnableTask = Relationship(self.Node(), "MODULE", moduleNode)
        
        tx = graph().begin()
        tx.create(moduleNode)
        tx.create(runnableTask)
        tx.commit()
        item.id = moduleNode.identity
        return item
    
    @staticmethod
    def create(user_id, workflow_id, script, args):
        item = RunnableItem(user_id, workflow_id, script, args)
        runnableNode = Node("Run", **item.json())
        
        tx = graph().begin()
        tx.create(runnableNode)
        tx.commit()
        item.id = runnableNode.identity
        return item
    
    @staticmethod
    def load_if(condition = None):
        pass
    
    def completed(self):
        return self._status == 'SUCCESS' or self._status == 'FAILURE' or self._status == 'REVOKED'
    
    def json(self):
        j = NodeItem.json(self)
        j.update({
            'user_id': self.user_id,
            'workflow_id': self.workflow_id,
            'celery_id': self.celery_id,
            'memory': (psutil.virtual_memory()[2])/bytes_in_gb,
            'cpu': (psutil.cpu_percent()),
            'out': self.out,
            'error': self._error,
            'script': self.script,
            'status': self.status,
            'duration': self.duration,
            'arguments': str(self.arguments),
            'name': self.name
            })
        return j
        
    @property
    def modules(self):
        moduleItems = []
        c = graph().run("MATCH(n:Run)-[:MODULE]->(t) WHERE ID(n)={0} return t".format(self._id)).data()
        for i in c:
            for _, v in i.items():
                moduleItems.append(ModuleItem.load_from_node(v))
        return moduleItems
    
    def modules_by_name(self, name):
        moduleItems = []
        cypher = "MATCH(n:Run)-[:MODULE]->(t) WHERE ID(n)={0} AND t.name = {1} return t".format(self._id, name) if name else "MATCH(n)-[:MODULE]->(t) WHERE ID(n)={0} return t".format(self._id)
        c = graph().run(cypher)
        for i in c:
            for _, v in i.items():
                moduleItems.append(ModuleItem.load_from_node(v))
        return moduleItems
    
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
            error = (self._error[:60] + '...') if len(self._error) > 60 else self._error
        return {
            'id': self._id,
            'name': self._name,
            'status': self._status,
            'error': error,
            'duration': self.__duration,
            'created_on': neotime2StrfTime(self._created_on) if self._created_on else '',
            'modified_on': neotime2StrfTime(self._modified_on) if self._modified_on else ''
        }
        
    def to_json_log(self):
        log = []
        
        modules = self.modules
        for module in modules:
            log.append(module.to_json_log())

        return {
            'id': self.id,
            'script': self._script,
            'status': self._status,
            'out': self._out,
            'error': self._error,
            'duration': self.__duration,
            'log': log
        }
        
    def to_json_info(self):
        return {
            'id': self._id,
            'user_id': self._user_id,
            'name': self._name,
            'modified_on': neotime2StrfTime(self._modified_on) if self._modified_on else '',
            'status': self._status
        }
    def graph(self):
        pass    
        
class ModuleItem(NodeItem):
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self._name = name
        self._status = Status.RECEIVED
    
    @property
    def name(self):
        return self._name
    
    @property
    def status(self):
        return self._status
    
    def json(self):
        j = NodeItem.json(self)
        j.update({
            'event': 'RUN-CREATE',
            'name':self._name,
            'memory': (psutil.virtual_memory()[2])/bytes_in_gb,
            'cpu': (psutil.cpu_percent()),
            'status': self._status           
        })
        
        return j 
    
    def prop_from_node(self, node):
        NodeItem.prop_from_node(self, node, "name", "status")
        self._status = node["status"]
        return self
    
    @property
    def run_id(self):
        c = graph().run("MATCH(n)-[:MODULE]->(t) WHERE ID(t)={0} return ID(n)".format(self.id))
        c.forward()
        return c.current[0]

    @staticmethod
    def load(module_id):
        return ModuleItem.load_from_node(load_node(module_id))
    
    @staticmethod
    def load_from_node(moduleNode):
        moduleItem = ModuleItem(moduleNode["name"])
        return moduleItem.prop_from_node(moduleNode)
    
    def start(self):
        self._status = Status.STARTED
        self._created_on = neotime.DateTime.utc_now()
        
        moduleNode = load_node(self.id)

        moduleNode["status"] = self._status
        moduleNode["created_on"] = self._created_on
        graph().push(moduleNode)
        
        self.add_log(Status.STARTED, LogType.INFO)
    
    def succeeded(self):
        self._status = Status.SUCCESS
        self.add_log(Status.SUCCESS, LogType.INFO)
        self._modified_on = neotime.DateTime.utc_now()
        
        moduleNode = load_node(self.id)
        
        moduleNode["status"] = self._status
        moduleNode["modified_on"] = self._modified_on
        graph().push(moduleNode)
    
    def failed(self, log = "Task Failed."):
        self._status = Status.FAILURE
        self.add_log(log, LogType.INFO)
        self._modified_on = neotime.DateTime.utc_now()
        
        moduleNode = self.Node()
        
        moduleNode["status"] = self._status
        moduleNode["modified_on"] = self._modified_on
        graph().push(moduleNode)
                    
    def add_log(self, log, logtype =  LogType.ERROR):
        item = TaskLogItem(log, logtype)
        taskLogNode = Node("TaskLog", **item.json())
        
        taskTaskLogRel = Relationship(self.Node(), "LOG", taskLogNode)
        
        tx = graph().begin()
        tx.create(taskLogNode)
        tx.create(taskTaskLogRel)
        tx.commit()
        
        item.id = taskLogNode.identity
        return item
    
    def graph(self):
        pass
    
    def add_input(self, user_id, datatype, value, rights):
        data = ValueItem.get_by_type_value(datatype, value)
        if not data:
            data = ValueItem(value, datatype)
            dataNode = Node("Data", **data.json())
            graph().create(dataNode)
            data.id = dataNode.identity
            
        dataAllocation = DataAllocationItem.load_by_data_user(data.id, user_id)
        if dataAllocation:
            dataAllocation.access = rights
        else:
            dataAllocation = DataAllocationItem.add(user_id, rights)
            data2dataAllocationRel = Relationship(data.Node(), "ALLOCATION", dataAllocation.Node())
            graph().create(data2dataAllocationRel)
            
        
        task2DataRel = Relationship(data.Node(), "INPUT", self.Node())
        graph().create(task2DataRel)

        return data
    
    def add_outputs(self, dataAndType, user_id):
        workflow_id = RunnableItem.load(self.run_id).workflow_id
        run_id = self.run_id
        
        result = ()        
        for d in dataAndType:
            dataNodeCreated = False
            data = None
            if not isinstance(d[1], ValueItem):
                data = ValueItem.get_by_type_value(d[0], d[1])
                if not data:
                    data = ValueItem(str(d[1]), d[0], task_id = self.id, job_id = run_id, workflow_id = workflow_id)
                    dataNode = Node("Data", **data.json())
                    dataNodeCreated = True
                else:
                    dataNode = data.Node()
            task2DataRel = Relationship(self.Node(), "OUTPUT", dataNode)

            #DataAllocationItem.add(user_id, dataNode)
            dataAllocationNodeCreated = False
            dataAllocation = None
            if not dataNodeCreated:
                dataAllocation = DataAllocationItem.load_by_data_user(data.id, user_id)
                if dataAllocation:
                    dataAllocation.access = AccessRights.Owner
            if not dataAllocation:
                dataAllocation = DataAllocationItem(user_id, AccessRights.Owner)
                dataAllocationNode =  Node('Allocation', **dataAllocation.json())
                dataAllocationNodeCreated = True
            else:
                dataAllocationNode = dataAllocation.Node()
            data2dataAllocationRel = Relationship(dataNode, "ALLOCATION", dataAllocationNode)
            
#             dataProperty = DataPropertyItem(str(self.id), { 'task_id': self.id, 'job_id': self.run_id, 'workflow_id': workflow_id, 'inout': 'out'})
#             dataPropertyNode =  Node("Property", **dataProperty.json())
#             data2dataPropertyRel = Relationship(dataNode, "PROPERTY", dataPropertyNode)
            
            
            tx = graph().begin()
            if dataNodeCreated:
                tx.create(dataNode)
            if dataAllocationNodeCreated:
                tx.create(dataAllocationNode)
#            tx.create(dataPropertyNode)
            
            tx.create(task2DataRel)
            tx.create(data2dataAllocationRel)
            #tx.create(data2dataPropertyRel)
            tx.commit()

            result += (d[1],)
        return result

    @property
    def outputs(self):
        dataItems = []
        c = graph().run("MATCH(n:Module)-[:OUTPUT]->(t) WHERE ID(n)={0} return t".format(self.id)).data()
        for i in c:
            for _, v in i.items():
                dataItems.append(ValueItem.load_from_node(v))
        return dataItems
    
    @property
    def inputs(self):
        dataItems = []
        c = graph().run("MATCH(n:Data)-[:INPUT]->(t) WHERE ID(t)={0} return n".format(self.id)).data()
        for i in c:
            for _, v in i.items():
                dataItems.append(ValueItem.load_from_node(v))
        return dataItems
    
    @property
    def logs(self):
        dataItems = []
        c = graph().run("MATCH(m:Module)-[:LOG]->(l) WHERE ID(n)={0} return l".format(self.id)).data()
        for i in c:
            for _, v in i.items():
                dataItems.append(TaskLogItem.load_from_node(v['l']))
        return dataItems
    
    def to_json_log(self):
        
        data = [{ "datatype": data.valuetype, "data": data.value} for data in self.outputs]
            
        return { 
            'name': self._name if self._name else "", 
            'status': self._status,
            'data': data
        }
        
class TaskLogItem(NodeItem):
    def __init__(self, log, logtype):
        super().__init__()
        self._type = logtype
        self._log = log
    
    @property
    def log(self):
        return self._log
    
    @property
    def type(self):
        return self._type
    
    def json(self):
        j = NodeItem.json(self)
        j.update({
            'event': 'LOG-CREATE',
            'memory': (psutil.virtual_memory()[2])/bytes_in_gb,
            'cpu': (psutil.cpu_percent()),
            'type': self._type,
            'log': self._log
            })
        
        return j
    
    def prop_from_node(self, node):
        return NodeItem.prop_from_node(self, node, "type", "log")
    
    @staticmethod
    def load(task_id):
        return ModuleItem.load_from_node(load_node(task_id))
    
    @staticmethod
    def load_from_node(taskNode):
        taskItem = TaskLogItem(taskNode["log"], taskNode["type"])
        return taskItem.prop_from_node(taskNode)
    
    def updateTime(self):
        self._modified_on = neotime.DateTime.utc_now()
        logNode = self.Node()
        logNode['modified_on'] = self._modified_on
        graph().push(logNode)