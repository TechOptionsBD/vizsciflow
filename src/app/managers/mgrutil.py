from config import Config

if Config.DATA_MODE == 0:
    from app.managers.wrappers.db import *
elif Config.DATA_MODE == 1 or Config.DATA_MODE == 2:
    from app.managers.wrappers.graph import *
elif Config.DATA_MODE == 3:
    from app.managers.wrappers.elastic import *

class ManagerUtility():
    @staticmethod
    def Manage(name):
        registry = {'workflow': WorkflowManager, 'manager': Manager, 'user': UserManager, 'module': ModuleManager, 'runnable': RunnableManager, 'data': DataManager, 'filter': FilterManager, 'activity': ActivityManager}
        return registry[name]()
