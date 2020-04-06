import os
import uuid
import psutil

from py2neo import NodeMatcher

from config import Config
from .models import Data, AccessRights, DataAllocation, DataProperty, TaskData
from .runmgr import runnableManager
from py2neo import Graph, Node, Relationship
import neotime
from dsl.datatype import DataType
from dsl.fileop import FolderItem

graphgen = Graph(Config.GRAPHDB, username=Config.GRAPHDB_USER, password=Config.GRAPHDB_PASSWORD)
graphgen.schema.create_uniqueness_constraint('Workflow', 'id')

class DataItem(object):
    def __init__(self):
        self.id = None
        self.value = None
    
#     def __getitem__(self, key):
#         return getattr(self, key)
#     
#     def __setitem__(self, key, item):
#         self.data[key] = item
        
class ValueItem(DataItem):

    def __init__(self, val, valuetype, path = ""):
        # type: (Any) -> None

        self.id = None
        self.value = val
        self.datatype =  type(val) #str(self.__class__.__name__) #val_type#
        self.valuetype = valuetype # if valuetype else str(DataType.Value) #str(type(self.value))
        self.path = path
        self.time = neotime.DateTime.utc_now()
    
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
        return {
            'event': 'VAL-SAVE',
            'datatype': str(self.datatype),
            'valuetype': self.valuetype,
            'value': str(self.value),
#                 'memory': (psutil.virtual_memory()[2])*(0.000001),
#                 'cpu': (psutil.cpu_percent()),
            'time': self.time,
            'name': 'value',
            'path': self.path
        }
    
    @staticmethod
    def get_by_type_value(datatype, value):
        c = graphgen.run("MATCH(d:Data) WHERE d['valuetype'] = {0} AND d['value'] = '{1}' RETURN d".format(datatype, value)).data()
        if c:
            return ValueItem.load(next(iter(c))['d'])

    @staticmethod
    def load(dataNode):
        valueItem = ValueItem(dataNode["value"], dataNode["valuetype"], dataNode["path"])
        valueItem.id = dataNode.identity
        valueItem.time = dataNode["time"]
        valueItem.datatype = dataNode["datatype"]
        return valueItem
    
    def Node(self):
        if not self.id:
            raise ValueError("Data Allocation Item is not saved to neo4j yet.")
        return NodeMatcher(graphgen).get(self.id)
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

class DataAllocationItem(object):

    def __init__(self, user_id, access):
        self.id = None
        self.user_id = user_id
        self.__access = access
        self.time = neotime.DateTime.utc_now()

    @staticmethod
    def add(user_id, access):
        dataAllocation = DataAllocationItem(user_id, access)
        dataAllocationNode =  Node('Allocation', **dataAllocation.json())
        graphgen.create(dataAllocationNode)
        dataAllocation.id = dataAllocationNode.identity
        return dataAllocation
                
    def json(self):
        return {
            'event': 'DATA-ALLOC',
            'user_id': self.user_id,
            'access': self.__access,
#                 'memory': (psutil.virtual_memory()[2])*(0.000001),
#                 'cpu': (psutil.cpu_percent()),
            'time': self.time
        }
    
    @staticmethod
    def load_by_data_user(data_id, user_id):
        c = graphgen.run("MATCH(n:Data)-[:ALLOCATION]->(a:Allocation) WHERE ID(n) = {0} AND a['user_id'] = {1} RETURN a".format(data_id, user_id)).data()
        if c:
            return DataAllocationItem.load(next(iter(c))['a'])
        
    @staticmethod
    def load(allocNodeItem):
        allocItem = DataAllocationItem(allocNodeItem["user_id"], allocNodeItem["access"])
        allocItem.id = allocNodeItem.identity
        allocItem.time = allocNodeItem["time"]
        return allocItem
    
    @property
    def access(self):
        return self.__access

    @access.setter    
    def access(self, access):        
        self.__access = access           
        self.time = neotime.DateTime.utc_now()
        allocNode = self.Node()
        allocNode["access"] = self.__access
        allocNode["time"] = self.time
        graphgen.push(allocNode)
    
    def Node(self):
        if not self.id:
            raise ValueError("Data Allocation Item is not saved to neo4j yet.")
        return NodeMatcher(graphgen).get(self.id)
        
class DataPropertyItem(object):

    def __init__(self, key, value):
        self.id = None
        self.key = key
        self.value = value
        self.datatype = type(value)
        self.time = neotime.DateTime.utc_now()

    def json(self):
        return {
            'event': 'PROP-SAVE',
            'key': self.key,
            'value': str(self.value),
            'datatype': str(self.datatype),
#                 'memory': (psutil.virtual_memory()[2])*(0.000001),
#                 'cpu': (psutil.cpu_percent()),
            'time': self.time
        }    
    
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
    
class GraphPersistance():
#     @staticmethod
#     def Save(dataitem):
#         return graphgen.graph.run(
#             statement="CREATE (x) SET x = {dict_param}",
#             parameters={'dict_param': dataitem})
#         
#         matcher = NodeMatcher(graphgen.graph)
#         return matcher.match(id=dataitem['id']).first()
#     
#     @staticmethod
#     def SavePermission(user, rights, dataitem):
#         matcher = NodeMatcher(graphgen.graph)
#         node = matcher.match(id=dataitem['id']).first()
#         
#         if not node:
#             node = GraphPersistance.Save(dataitem)
#     
#         usernode = matcher.match(id=user).first()
#         if not usernode:
#             raise ValueError("User doesn't exist")
#         
#         rel = Relationship(usernode, "ACCESS", node)
#         rel.properties["rights"] = str(rights)
#         
#         return rel
#   
#     @staticmethod
#     def SaveMetadata(data, metadata):
#         
#         metadatanode = GraphPersistance.Save(metadata)
#         return Relationship(data, "METADATA", metadatanode)
       
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
        
        #fileitems = matcher.match("FileItem", value=path)

#         prefixedDataSources = DataSource.query.filter(or_(DataSource.prefix == path, DataSource.url == path))
#         if prefixedDataSources:
#             defaultRights = AccessRights.Read
#         
#         matcher = NodeMatcher(graphgen.graph)
#         return matcher.match(id=user_id)
#     
#         allocations = DataSourceAllocation.query.join(DataPermission, DataPermission.data_id == DataSourceAllocation.id).filter(DataPermission.user_id == user_id)
#         for allocation in allocations:
#             if path.startswith(allocation.url):
#                 for permission in allocation.permissions:
#                     return permission.rights 
        
        return defaultRights
        
    @staticmethod
    def add_task_data(dataAndType, user_id, task):
        runnable_id = task.runnable_id
        
        workflow_id = runnableManager.get_runnable(runnable_id).workflow_id
            
        result = ()        
        for d in dataAndType:
            dataNodeCreated = False
            data = None
            if not GraphPersistance.is_data_item(d[1]):
                data = ValueItem.get_by_type_value(d[0], d[1])
                if not data:
                    data = ValueItem(str(d[1]), d[0], "")
                    dataNode = Node("Data", **data.json())
                    dataNodeCreated = True
            task2DataRel = Relationship(task.Node(), "OUTPUT", dataNode)

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
            data2dataAllocationRel = Relationship(dataNode, "ALLOCATION", dataAllocationNode)
            
            dataProperty = DataPropertyItem(str(task.id), { 'task_id': task.id, 'job_id': runnable_id, 'workflow_id': workflow_id, 'inout': 'out'})
            dataPropertyNode =  Node("Property", **dataProperty.json())
            data2dataPropertyRel = Relationship(dataNode, "PROPERTY", dataPropertyNode)
            
            
            tx = graphgen.begin()
            if dataNodeCreated:
                tx.create(dataNode)
            if dataAllocationNodeCreated:
                tx.create(dataAllocationNode)
            tx.create(dataPropertyNode)
            
            tx.create(task2DataRel)
            tx.create(data2dataAllocationRel)
            tx.create(data2dataPropertyRel)
            tx.commit()

            result += (d[1],)
        return result
    
    @staticmethod
    def is_data_item(value):
        return isinstance(value, ValueItem)
    
    @staticmethod
    def add_data_with_rights(user_id, datatype, value, rights):
        data = ValueItem.get_by_type_value(datatype, value)
        if not data:
            data = ValueItem(value, datatype, "")
            dataNode = Node("Data", **data.json())
            graphgen.create(dataNode)
            data.id = dataNode.identity
        dataAllocation = DataAllocationItem.load_by_data_user(data.id, user_id)
        if dataAllocation:
            dataAllocation.access = rights
        else:
            dataAllocation = DataAllocationItem.add(user_id, rights)
            data2dataAllocationRel = Relationship(data.Node(), "ALLOCATION", dataAllocation.Node())
            graphgen.create(data2dataAllocationRel)
        return data
    
class DBPersistance():
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
    def check_access_rights(user_id, path, checkRights):
        DataSourceAllocation.check_access_rights(user_id, path, checkRights)
    
    @staticmethod
    def get_access_rights(user_id, path):
        DataSourceAllocation.get_access_rights(user_id, path)
    
    @staticmethod
    def load(user_id, recursive):
        datasets = DataAllocation.query.filter_by(user_id = user_id)
        data_dict = {}
        for dataset in datasets:
            pass
        
        return data_dict
    
    @staticmethod
    def add_task_data(dataAndType, user_id, task):
        result = ()        
        for d in dataAndType:
            #ds = Utility.ds_by_prefix_or_default(str(d[1])) if isinstance(d[1], FolderItem) else d[1]
            data = Data.get_by_type_value(datatype, value)
            if not data:
                data = Data.add(str(d[1]), d[0], "")
            
            TaskData.add(task.id, data.id)
            DataAllocation.add(user_id, data.id, AccessRights.Owner)
            workflow_id = runnableManager.get_runnable(task.runnable_id).workflow_id
            DataProperty.add(data.id, "execution {0}".format(task.id), { 'workflow': { 'task_id': task.id, 'job_id': task.runnable_id, 'workflow_id': workflow_id, 'inout': 'out'} })
            
            result += (d[1],)
        return result
    
    @staticmethod
    def is_data_item(value):
        return isinstance(value, Data)
    
    @staticmethod
    def add_data_with_rights(user_id, datatype, value, rights):
        data = Data.get_by_type_value(datatype, value)
        if not data:
            data = Data.add(value, datatype, "")
        DataAllocation.add(user_id, data.id, rights)
        return data
        
class DataManager():
    def __init__(self):
        self.persistance = GraphPersistance() if Config.DATA_GRAPH else DBPersistance() 
    
    def Save(self, dataitem):
        return self.persistance.Save(dataitem)
    
    def SavePermission(self, user, rights, dataitem):
        return self.persistance.SavePermission(user, rights, dataitem)
    
    def check_access_rights(self, user_id, path, checkRights):
        self.persistance.check_access_rights(user_id, path, checkRights)

    def get_access_rights(self, user_id, path):
        self.persistance.get_access_rights(user_id, path)
    
    def access_rights_to_string(self, user_id, path):
        return AccessRights.rights_to_string(self.get_access_rights(user_id, path))
    
    def load(self, user_id, recursive):
        self.persistance.load(user_id, recursive)
    
    def add_task_data(self, dataAndType, user_id, task):
        return self.persistance.add_task_data(dataAndType, user_id, task)
    
    def is_data_item(self, value):
        return self.persistance.is_data_item(value)
    
    def add_data_with_rights(self, user_id, datatype, value, rights):
        return self.persistance.add_data_with_rights(user_id, datatype, value, rights)
    
    def StoreArgumentes(self, user_id, task, params, args):
        if not isinstance(params, list):
            params = [params]
        for i in range(0, len(args)):
            if not dataManager.is_data_item(args[i]):
                paramType = DataType.Value
                if i < len(params):
                    paramType = params[i]["type"]
                    paramType = paramType.lower().split('|')
                    if 'file' in paramType:
                        paramType = DataType.File
                    elif 'folder' in paramType:
                        paramType = DataType.Folder
                    
                data = dataManager.add_data_with_rights(user_id, paramType, args[i], AccessRights.Read)
                
                task2DataRel = Relationship(data.Node(), "INPUT", task.Node())
                graphgen.create(task2DataRel)
                           
    def SaveMetaData(self, user, rights, category, key, value):

        value["user"] = str(user)
        value["rights"] = str(rights)

        val_type = None
        
        item = ValueItem(value, val_type)
        json = item.json()
        json["category"] = category
        json["key"] = key
        return self.persistance.SaveMetadata(user, rights, json)
        
dataManager = DataManager()