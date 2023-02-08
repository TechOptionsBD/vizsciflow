import logging
from dsl.datatype import DataType
from app.managers.mgrutil import ManagerUtility
from app.objectmodel.common import AccessRights, known_types, str_or_empty
from pathlib import Path

class DataManager():
    def __init__(self):
        self.persistance = ManagerUtility.Manage('data')

    def get_by_id(self, id):
        return self.persistance.first(id = id)

    def get_by_value(self, value):
        return self.persistance.get(value = value)

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
                    if 'file[]' in paramType:
                        paramType = DataType.FileList
                    elif 'folder[]' in paramType:
                        paramType = DataType.FolderList
                
                module.add_arg(paramType, args[i])
               
    def StoreArgumentes(self, user_id, task, params, args):
        if not isinstance(params, list):
            params = [params]
        for i in range(0, len(args)):
            if not self.is_data_item(args[i]):
                paramType = DataType.Value
                if i < len(params):
                    paramType = params[i].type if hasattr(params[i], 'type') else 'any'
                    paramType = paramType.lower().split('|')
                    if 'file' in paramType:
                        paramType = DataType.File
                    elif 'folder' in paramType:
                        paramType = DataType.Folder
                    elif 'folder' in paramType:
                        paramType = DataType.Folder
                    elif 'file[]' in paramType:
                        paramType = DataType.FileList
                    elif 'folder[]' in paramType:
                        paramType = DataType.FolderList
                    elif 'any' in paramType:
                        paramType = DataType.Unknown
                    elif any(item in known_types.keys() for item in paramType):
                        paramType = DataType.Value
                    else:
                        paramType = DataType.Unknown
                        logging.error(f"Store Arguments: param type {paramType} doesn't exist.")
                        #raise ValueError("Store Arguments: param type {0} doesn't exist.".format(paramType))
                
                task.add_input(user_id, paramType, str_or_empty(args[i]), AccessRights.Read, name = params[i].name if i < len(params) and params[i].name else "")
                           
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
    
    def get_mimetype(self, file):
        if file:
            path = Path(file)
            if path.suffix:
                mime = self.persistance.get_mimetype(path.suffix[1:])
                if mime:
                    return mime.name
    
    def load_listview_datasets(self, user_id, page, no_of_item):
        return self.persistance.load_listview_datasets(user_id, page, no_of_item)
    
    def load_dataset_data_for_plugin(self, user_id, dataset_id, data_id, page_num):
        return self.persistance.load_dataset_data_for_plugin(user_id, dataset_id, data_id, page_num)
    
    def get_task_data_value(self, data_id):
        return self.persistance.get_task_data_value(data_id)
    
datamanager = DataManager()