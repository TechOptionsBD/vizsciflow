import os
import uuid
import psutil
from datetime import datetime

from py2neo.data import Relationship
from py2neo import NodeMatcher

from config import Config
from dsl.fileop import FolderItem
from .models import Data, DataSourceAllocation, AccessRights, DataProperty, DataType #DataAllocation, DataType, Property,
from .util import Utility
from .runmgr import runnableManager
from py2neo import Graph

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

    def __init__(self, val, valuetype):
        # type: (Any) -> None

        self.id = uuid.uuid4()
        self.value = val
        self.datatype =   str(self.__class__.__name__) #val_type#
        self.valuetype = valuetype if valuetype else str(DataType.Value) #str(type(self.value))
        
    def json(self):
        try:
            msg = {
                'event': 'VAL-SAVE',
                'id': str(self.id),
                'datatype': self.datatype,
                'valuetype': self.valuetype,
                'value': str(self.value),
                'memory': (psutil.virtual_memory()[2])*(0.000001),
                'cpu': (psutil.cpu_percent()),
                'time': str(datetime.utcnow()),
                'name': 'value',
                'error': 'success'
            }
            
            return msg    
        except:
            pass
    
class FileItem(ValueItem):

    def __init__(self, f, ds_id = None):
        self.ds_id = ds_id
        super().__init__(f, DataType.File)
        
        if not self.ds_id:
            ds = Utility.ds_by_prefix(f)
            if ds:
                self.ds_id = ds.id
        
    def json(self):
        v = super().json()
        v["ds"] = str(self.ds_id) 
        v["name"] = "file"
        return v
    
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

class GraphPermission(object):

    def __init__(self, rights):
        self.id = uuid.uuid4()
        self.label = "Permission"
        self.rights = rights
        
    def json(self):
        try:
            msg = {
                'event': 'PERM-SAVE',
                'id': str(self.id),
                'rights': str(self.rights),
                'time': str(datetime.utcnow()),
                'label': self.label,
                'error': 'success'
            }
            
            return msg    
        except:
            pass
        
class ModuleItem(ValueItem):

    def __init__(self, f):
        super().__init__(f, DataType.Module)
        
    def json(self):
        v = super().json()
        v["name"] = "folder"
        return v
    
    def startLogMsg(self, user):
        msg = {
            'event': 'MOD-STRT',
            'id': str(self.id),
            'user': user
        }
        #deb.debug(jsonify(msg))
        return msg

    def endLogMsg(self):
        msg = {
            'event': 'MOD-END',
            'id': str(self.id),
            'user': str(self.user)
        }

        #deb.debug(jsonify(msg))
        return msg
        

    def body(self):
        """
        :param interfaceParam:
        :return:
        """

    def run(self, *args):

        start_time = datetime.utcnow()

        self.P = args

        try:
            param_ids = []

            for i in args:

                if isinstance(i, Object) or isinstance(i, File) or isinstance(i, Document):
                    param_ids.append(str(i.id))

                else:
                    param_ids.append(str(i))



            msg = {
                'p@': param_ids,
                'event': 'MOD-CRTN',
                'id': str(self.id),
                'name': str(self.__class__.__name__),
                'user': str(USER.id),
                'memory_init': (psutil.virtual_memory()[2])*(.000001),
                'cpu_init': (psutil.cpu_percent()),
                'duration_init': str(datetime.utcnow()-start_time),
                'time': str(datetime.utcnow()),
                'cpu_run': 0,
                'memory_run': 0,
                'duration_run': "00:00:00.000000",
                'label': 'module',
                'error': 'success'
            }

            deb.debug(jsonify(msg))

            elasticmodule(msg['id'], msg['time'], msg['name'], msg['user'], msg['memory_run'], msg['memory_init'], msg['cpu_run'], msg['cpu_init'], msg['duration_run'], msg['duration_init'], msg['error'])

            ''' GDB part '''
            props = ['NAME:\"' + msg['name'] + '\"', 'id:\"' + msg['id'] + '\"',
                     'user:\"' + msg['user'] + '\"', 'error:\"null\"', 'time:\"' + str(msg['time']) + '\"', 'memory_init:\"' + str(msg['memory_init']) + '\"',
                     'cpu_init:\"' + str(msg['cpu_init']) + '\"', 'duration_init:\"' + str(msg['duration_init']) + '\"',
                     'duration_run:\"' + str(msg['duration_run']) + '\"', 'memory_run:\"' + str(msg['memory_run']) + '\"', 'cpu_run:\"' + str(msg['cpu_run']) + '\"',
                     'label:\"' + str(msg['label']) + '\"']
            propsQuery = ','.join(props)
            #print propsQuery
            query = 'create (n:Module{' + propsQuery + '})'
            graph.run(query)


            ''' relationships '''
            for uninqid in param_ids:
                # match (n:Object{id:uniqid}), (m:Module{id:id})
                # create (n)-[:IN]-> (m)

                query = ' match (n),(m) where n.id = \"' + uninqid + '\" and m.id = \"' + msg['id'] + '\" create (n)-[:IN]-> (m)'
                #print query
                graph.run(query)
        except:
            pass
    
class GraphPersistance():
    @staticmethod
    def Save(dataitem):
        return graphgen.graph.run(
            statement="CREATE (x) SET x = {dict_param}",
            parameters={'dict_param': dataitem})
        
        matcher = NodeMatcher(graphgen.graph)
        return matcher.match(id=dataitem['id']).first()
    
    @staticmethod
    def SavePermission(user, rights, dataitem):
        matcher = NodeMatcher(graphgen.graph)
        node = matcher.match(id=dataitem['id']).first()
        
        if not node:
            node = GraphPersistance.Save(dataitem)
    
        usernode = matcher.match(id=user).first()
        if not usernode:
            raise ValueError("User doesn't exist")
        
        rel = Relationship(usernode, "ACCESS", node)
        rel.properties["rights"] = str(rights)
        
        return rel
  
    @staticmethod
    def SaveMetadata(data, metadata):
        
        metadatanode = GraphPersistance.Save(metadata)
        return Relationship(data, "METADATA", metadatanode)
       
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
        
class DBPersistance():
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
            if isinstance(d[1], FolderItem):
                ds = Utility.ds_by_prefix_or_default(str(d[1]))
                data_alloc = DataSourceAllocation.get(user_id, ds.id, str(d[1]))
                if not data_alloc:
                    data_alloc = DataSourceAllocation.add(user_id, ds.id, str(d[1]), AccessRights.Owner)
                
    
                workflow_id = runnableManager.get_runnable(task.runnable_id).workflow_id
                DataProperty.add(data_alloc.id, "execution {0}".format(task.id), { 'workflow': { 'task_id': task.id, 'job_id': task.runnable_id, 'workflow_id': workflow_id, 'inout': 'out'} })
            result += (d[1],)
        return result
    
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