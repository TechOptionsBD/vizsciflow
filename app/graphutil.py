import sys

from config import Config
from flask import g

import psutil
from datetime import datetime

from .ogmex import GraphObject, Property, RelatedTo, RelatedFrom, OGM, RelatedObjects, Related, OUTGOING, GraphObjectMatcher, GraphObjectMatch, Repository, GraphObjectType
from py2neo import NodeMatcher
from py2neo import Graph
from py2neo.data import PropertyDict, Node 
from py2neo.compat import metaclass
import neotime

from .models import Status, Workflow, LogType, AccessRights, DataType, User
from dsl.fileop import FolderItem

def graph():
    if 'graph' not in g:
        g.graph = Graph(Config.GRAPHDB, username=Config.GRAPHDB_USER, password=Config.GRAPHDB_PASSWORD)
#        g.graph.schema.create_uniqueness_constraint('Workflow', 'workflow_id')
    return g.graph


# class OGMEx(OGM):
# 
#     def __init__(self, node):
#         super().__init__(node)
# 
#     def relatedex(self, direction, relationship_type, related_class, order_by):
#         """ Return :class:`.RelatedObjects` for given criteria.
#         """
#         key = (direction, relationship_type)
#         if key not in self._related:
#             self._related[key] = RelatedObjectsEx(self.node, direction, relationship_type, related_class, order_by)
#         return self._related[key]
# 
# class RelatedObjectsEx(RelatedObjects):
#     """ A set of similarly-typed and similarly-related objects,
#     relative to a central node.
#     """
# 
#     def __init__(self, node, direction, relationship_type, related_class, order_by):
#         super().__init__(node, direction, relationship_type, related_class)
#         self.order_by = order_by
#         
# 
# #     def add(self, obj, properties=None, **kwproperties):
# #         """ Add a related object.
# # 
# #         :param obj: the :py:class:`.GraphObject` to relate
# #         :param properties: dictionary of properties to attach to the relationship (optional)
# #         :param kwproperties: additional keyword properties (optional)
# #         """
# #         related_objects = self._related_objects
# #         properties = PropertyDict(properties or {}, **kwproperties)
# #         added = False
# #         for i, (related_object, _) in enumerate(related_objects):
# #             if related_object == obj:
# #                 related_objects[i] = (obj, properties)
# #                 added = True
# #         if not added:
# #             related_objects.append((obj, properties))
# 
# #     def update(self, obj, properties=None, **kwproperties):
# #         """ Add or update a related object.
# # 
# #         :param obj: the :py:class:`.GraphObject` to relate
# #         :param properties: dictionary of properties to attach to the relationship (optional)
# #         :param kwproperties: additional keyword properties (optional)
# #         """
# #         related_objects = self._related_objects
# #         properties = dict(properties or {}, **kwproperties)
# #         added = False
# #         for i, (related_object, p) in enumerate(related_objects):
# #             if related_object == obj:
# #                 related_objects[i] = (obj, PropertyDict(p, **properties))
# #                 added = True
# #         if not added:
# #             related_objects.append((obj, properties))
# 
#     def __db_pull__(self, tx):
#         related_objects = {}
#         matcher = tx.graph.match(**self._RelatedObjects__match_args)
#         if self.order_by:
#             matcher = matcher.order_by(self.order_by)
#         for r in matcher:
#             nodes = []
#             n = self.node
#             a = r.start_node
#             b = r.end_node
#             if a == b:
#                 nodes.append(a)
#             else:
#                 if self.__start_node and a != n:
#                     nodes.append(r.start_node)
#                 if self.__end_node and b != n:
#                     nodes.append(r.end_node)
#             for node in nodes:
#                 related_object = self.related_class.wrap(node)
#                 related_objects[node] = (related_object, PropertyDict(r))
#         self._related_objects[:] = related_objects.values()
# 
# class RelatedEx(Related):
#     """ Descriptor for a set of related objects in a :class:`.GraphObject`.
# 
#     Attributes:
#         related_class: The class of object to which these relationships
#                        connect. This class is used to coerce nodes to and
#                        from :class:`GraphObject` instances.
#         relationship_type: The underlying relationship type for these
#                            relationships. Note that the relationship
#                            type should be unique for each class of related
#                            object as the `related_class` is only used for
#                            object coercion and not as part of the underlying
#                            database query.
#     """
# 
#     def __init__(self, related_class, relationship_type=None, order_by=None):
#         """ Initialise a property definition.
# 
#         Args:
#             related_class: The class of object to which these relationships
#                            connect.
#             relationship_type: The underlying relationship type for these
#                                relationships.
#         """
#         self.related_class = related_class
#         self.relationship_type = relationship_type
#         self.order_by=order_by
# 
#     def __get__(self, instance, owner):
#         return instance.__ogm__.relatedex(self.direction, self.relationship_type,
#                                         self._resolve_class(self.related_class, instance), self.order_by)
#     
#     @classmethod
#     def _resolve_class(cls, ogm_class, instance):
#         if isinstance(ogm_class, type):
#             return ogm_class
#         module_name, _, class_name = ogm_class.rpartition(".")
#         if not module_name:
#             module_name = instance.__class__.__module__
#         module = __import__(module_name, fromlist=".")
#         return getattr(module, class_name)
#     
# class RelatedToEx(RelatedEx):
#     direction = OUTGOING
# 
# 
# class GraphObjectMatcherEx(GraphObjectMatcher):
# 
#     _match_class = GraphObjectMatch
# 
#     def __init__(self, object_class, repository):
#         super().__init__(object_class, repository)
# 
#     def match(self, primary_value=None):
#         cls = self._object_class
#         properties = {}
#         if primary_value is not None:
#             return NodeMatcher.match(self, cls.__primarylabel__).where("id(_) = %d" % primary_value)
#         return NodeMatcher.match(self, cls.__primarylabel__, **properties)
# 
# @metaclass(GraphObjectType)    
# class GraphObjectEx(GraphObject):
#     
#     @property
#     def __ogm__(self):
#         if self._GraphObject__ogm is None:
#             self._GraphObject__ogm = OGMEx(Node(self.__primarylabel__))
#         node = self._GraphObject__ogm.node
#         if not hasattr(node, "__primarylabel__"):
#             setattr(node, "__primarylabel__", self.__primarylabel__)
#         if not hasattr(node, "__primarykey__"):
#             setattr(node, "__primarykey__", self.__primarykey__)
#         return self.__ogm
# 
#     @classmethod
#     def wrap(cls, node):
#         """ Convert a :class:`.Node` into a :class:`.GraphObject`.
# 
#         :param node:
#         :return:
#         """
#         if node is None:
#             return None
#         inst = GraphObjectEx()
#         inst.__ogm = OGMEx(node)
#         inst.__class__ = cls
#         return inst
# 
#     @classmethod
#     def match(cls, repository, primary_value=None):
#         """ Select one or more nodes from the database, wrapped as instances of this class.
# 
#         :param repository: the :class:`.Repository` in which to match
#         :param primary_value: value of the primary property (optional)
#         :rtype: :class:`.GraphObjectMatch`
#         """
#         return GraphObjectMatcherEx(cls, repository).match(primary_value)
    
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
    
    def add_module(self, package, function):
        if package:
            function = package + '.' + function
        
        item = ModuleItem(function)
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
    celery_id = Property("celery_id")
    name = Property("name")
    
    out = Property("out")
    error = Property("error")
    
    script = Property("script")
    status = Property("status")
    duration = Property("duration")
    arguments = Property("arguments")
    
    modules = RelatedTo("ModuleItem", "MODULE", "id(b)")
    users = RelatedFrom(UserItem, "USERRUN")
    workflows = RelatedFrom(WorkflowItem, "WORKFLOWRUN")
    
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        if not self.celery_id:
            self.celery_id = 0
        
        if not self.out:
            self.out = ""
        
        if not self.error:
            self.error = ""
        
        if not self.script:
            self.script = ""
        
        if not self.status:
            self.status = Status.RECEIVED
            
        if not self.duration:
            self.duration = 0
        
        if not self.arguments:
            self.arguments = ""
            
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
            return list(RunnableItem.match(graph()).limit(sys.maxsize))
    
    @staticmethod
    def load_for_users(user_id):
        user = UserItem.match(graph()).where("_.user_id = {0}".format(user_id)).first()
        return list(user.runs) if user else []
    
    def add_module(self, function_name):
        item = ModuleItem(function_name)
        self.modules.add(item)
        from py2neo.data import Node
        n = Node(self.__primarylabel__)
        
        graph().push(self)
        graph().pull(self)
        return item
    
    @staticmethod
    def create(user_id, workflow_id, script, args):
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
            'name': self.name,
            'status': self.status,
            'err': error,
            'duration': self.duration,
            'created_on': str(self.created_on) if self.created_on else '',
            'modified_on': str(self.modified_on) if self.modified_on else ''
        }
        
    def to_json_log(self):
        log = []
        
        for module in self.modules:
            log.append(module.to_json_log())

        return {
            'id': self.id,
            'script': self.script,
            'status': self.status,
            'out': self.out,
            'err': self.error,
            'duration': self.duration,
            'log': log
        }
        
    def to_json_info(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'modified_on': str(self.modified_on) if self.modified_on else '',
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
        self.created_on = datetime.utcnow()
        self.add_log(Status.STARTED, LogType.INFO)
        graph().push(self)
    
    def succeeded(self):
        self.status = Status.SUCCESS
        self.add_log(Status.SUCCESS, LogType.INFO)
        self.modified_on = datetime.utcnow()
        graph().push(self)
    
    def failed(self, log = "Task Failed."):
        self.status = Status.FAILURE
        self.add_log(log, LogType.INFO)
        self.modified_on = datetime.utcnow()
        graph().push(self)
                    
    def add_log(self, log, logtype =  LogType.ERROR):
        item = TaskLogItem(log, logtype)
        self.logs.add(item)
        return item
    
    def graph(self):
        pass
    
    def add_arg(self, datatype, value):
        if isinstance(value, ValueItem):
            self.inputs.add(value)
        else:
            for data in self.inputs:
                if data.datatype == datatype and data.value == value:
                    value = data
                    break
            if not value:    
                value = ValueItem.get_by_type_value(datatype, value)
                if not value:
                    data = ValueItem(value, datatype)
                    graph().push(data)
                self.inputs.add(data)

        graph().push(self)
        
        return value
    
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
        self.modified_on = datetime.utcnow()
        graph().push(self)