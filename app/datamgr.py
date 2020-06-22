import os

from config import Config
from .models import Data, AccessRights, DataAllocation, DataProperty, TaskData
from dsl.datatype import DataType
from .graphutil import ValueItem

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
    
    @staticmethod
    def is_data_item(value):
        return isinstance(value, ValueItem)
    
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
    def add_task_data(dataAndType, task):
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
    
    def add_task_data(self, dataAndType, task):
        return self.persistance.add_task_data(dataAndType, task)
    
    def is_data_item(self, value):
        return self.persistance.is_data_item(value)
    
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
                
                task.add_input(user_id, paramType, args[i], AccessRights.Read)
                           
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