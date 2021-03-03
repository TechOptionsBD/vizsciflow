import os

from config import Config
from dsl.datatype import DataType
from ..graphutil import ValueItem
from ..mocks.datamocks import PersistanceMock
from ..models import DataSourceAllocation, DataSource, Data, DataAllocation
from ..common import AccessRights
from sqlalchemy import and_, or_
from .runmgr import runnablemanager

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
    def is_data_item(value):
        return isinstance(value, ValueItem)
    
    @staticmethod
    def check_access_rights(user_id, path, checkRights):
        ValueItem.check_access_rights(user_id, path, checkRights)
    
    @staticmethod
    def get_access_rights(user_id, path):
        return ValueItem.get_access_rights(user_id, path)
        
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
        
    @staticmethod
    def add_task_data(dataAndType, task):
        return task.add_outputs(dataAndType)
    
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
    def has_access_rights(user_id, path, checkRights):
        return DataSourceAllocation.has_access_rights(user_id, path, checkRights)

    @staticmethod
    def load(user_id, recursive):
        datasets = DataAllocation.query.filter_by(user_id = user_id)
        data_dict = {}
        for dataset in datasets:
            pass
        
        return data_dict
    
    @staticmethod
    def add_task_data(dataAndType, task):
        result = ()        
        for d in dataAndType:
            task.add_output(d[0], str(d[1]))                        
            result += (d[1],)
        return result
    
    @staticmethod
    def is_data_item(value):
        return isinstance(value, Data)
    
    @staticmethod
    def add(user_id, datasource_id, url, rights):
        return DataSourceAllocation.add(user_id, datasource_id, url, rights)

    @staticmethod
    def get_allocation(datasource_id, **kwargs):
        return DataSourceAllocation.query.filter(datasource_id, **kwargs).first()
    
    @staticmethod
    def get_datasources(**kwargs):
        return DataSource.query.filter_by(**kwargs)

    @staticmethod
    def get_allocation_by_url(ds_id, url):
        return DataSourceAllocation.query.filter(and_(DataSourceAllocation.datasource_id == ds_id, DataSourceAllocation.url == url)).first()

class DataManager():
    def __init__(self):
        if Config.DATA_MODE == 0:
            self.persistance = DBPersistance()
        elif Config.DATA_MODE == 1:
            self.persistance = GraphPersistance()
        else:
            self.persistance = PersistanceMock()
    
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
    
    def has_access_rights(self, user_id, path, checkRights):
        return self.persistance.has_access_rights(user_id, path, checkRights)

    def load(self, user_id, recursive):
        self.persistance.load(user_id, recursive)
    
    def add_task_data(self, dataAndType, task):
        return self.persistance.add_task_data(dataAndType, task)
    
    def is_data_item(self, value):
        return self.persistance.is_data_item(value)
    
    def StoreModuleArgs(self, module, params, args):
        if not isinstance(params, list):
            params = [params]
        for i in range(0, len(args)):
            if not datamanager.is_data_item(args[i]):
                paramType = DataType.Value
                if i < len(params):
                    paramType = params[i]["type"]
                    paramType = paramType.lower().split('|')
                    if 'file' in paramType:
                        paramType = DataType.File
                    elif 'folder' in paramType:
                        paramType = DataType.Folder
                
                module.add_arg(paramType, args[i])
               
    def StoreArgumentes(self, user_id, task, params, args):
        if not isinstance(params, list):
            params = [params]
        for i in range(0, len(args)):
            if not self.is_data_item(args[i]):
                paramType = DataType.Value
                if i < len(params):
                    paramType = params[i]["type"]
                    paramType = paramType.lower().split('|')
                    if 'file' in paramType:
                        paramType = DataType.File
                    elif 'folder' in paramType:
                        paramType = DataType.Folder
                
                task.add_input(user_id, paramType, str(args[i]), AccessRights.Read, name = params[i]["name"] if i < len(params) and 'name' in params[i] else "")
                           
    def SaveMetaData(self, user, rights, category, key, value):

        value["user"] = str(user)
        value["rights"] = str(rights)

        val_type = None
        
        item = ValueItem(value, val_type)
        json = item.json()
        json["category"] = category
        json["key"] = key
        return self.persistance.SaveMetadata(user, rights, json)

    def add_allocation(self, user_id, datasource_id, url, rights):
        return self.persistance.add(user_id, datasource_id, url, rights)
    def get_allocation(self, datasource_id, **kwargs):
        return self.persistance.get(datasource_id, **kwargs)
    def get_datasource(self, **kwargs):
        return self.get_datasources(**kwargs).first()
    def get_datasources(self, **kwargs):
        return self.persistance.get_datasources(**kwargs)
    def get_allocation_by_url(self, ds_id, url):
        return self.persistance.get_allocation_by_url(ds_id, url)

        
datamanager = DataManager()