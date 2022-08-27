from .runmocks import RunnableMock

class ValueMock:
    @staticmethod
    def check_access_rights(user_id, path, checkRights):
        pass
        
    @staticmethod
    def get_access_rights(user_id, path):
        pass

class PersistanceMock(): 
    @staticmethod
    def is_data_item(value):
        return isinstance(value, ValueMock)
    
    @staticmethod
    def check_access_rights(user_id, path, checkRights):
        ValueMock.check_access_rights(user_id, path, checkRights)
    
    @staticmethod
    def get_access_rights(user_id, path):
        return ValueMock.get_access_rights(user_id, path)
                
    @staticmethod
    def add_task_data(dataAndType, task):
        return task.add_outputs(dataAndType)