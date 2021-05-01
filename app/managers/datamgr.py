import os

from config import Config
from dsl.datatype import DataType
from ..graphutil import ValueItem, DataSourceItem
from ..mocks.datamocks import PersistanceMock
from ..models import DataSourceAllocation, DataSource, Data, DataAllocation
from ..common import AccessRights
from sqlalchemy import and_, or_
from .runmgr import runnablemanager
from ..elasticutil import ElasticDataSource, ElasticValue

class ElasticPersistance():
    @staticmethod
    def insert_datasources():
        return ElasticDataSource.insert_datasources()

    @staticmethod
    def get_datasources(**kwargs):
        return ElasticDataSource.get(**kwargs)

    @staticmethod
    def is_data_item(value):
        return isinstance(value, ElasticValue)

    @staticmethod
    def add_task_data(dataAndType, task):
        return task.add_outputs(dataAndType)
        
class GraphPersistance():
    
    @staticmethod
    def is_data_item(value):
        return isinstance(value, ValueItem)
    
    @staticmethod
    def check_access_rights(user_id, path, checkRights):
        ValueItem.check_access_rights(user_id, path, checkRights)
    
    @staticmethod
    def get_access_rights(user_id, path):
        return ValueItem.get_access_rights(user_id, path)
        
    @staticmethod
    def add_task_data(dataAndType, task):
        return task.add_outputs(dataAndType)

    @staticmethod
    def insert_datasources():
        return DataSourceItem.insert_datasources()
    
    @staticmethod
    def get_datasources(**kwargs):
        return DataSourceItem.get(**kwargs)
    
    @staticmethod
    def add(user_id, datasource_id, url, rights):
        return DataSourceItem.add(user_id, datasource_id, url, rights)
    
    @staticmethod
    def has_access_rights(user_id, path, checkRights):
        return DataSourceItem.has_access_rights(user_id, path, checkRights)

class DBPersistance():
        
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

    @staticmethod
    def insert_datasources():
        return DataSource.insert_datasources()

class DataManager():
    def __init__(self):

        if Config.DATA_MODE == 0:
            self.persistance = DBPersistance()
        elif Config.DATA_MODE == 1:
            self.persistance = GraphPersistance()
        elif Config.DATA_MODE == 3:
            self.persistance = ElasticPersistance()
        else:
            self.persistance = PersistanceMock()

        # self.persistance.insert_datasources()
        # from ..graphutil import RoleItem
        # RoleItem.insert_roles()
    
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
        '''
            It will return a tuple.
        '''
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
                    paramType = params[i].type
                    paramType = paramType.lower().split('|')
                    if 'file' in paramType:
                        paramType = DataType.File
                    elif 'folder' in paramType:
                        paramType = DataType.Folder
                
                task.add_input(user_id, paramType, str(args[i]), AccessRights.Read, name = params[i].name if i < len(params) and params[i].name else "")
                           
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

    def insert_datasources(self):
        return self.persistance.insert_datasources()

        
datamanager = DataManager()