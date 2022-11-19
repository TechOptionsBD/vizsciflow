from app.managers.mgrutil import ManagerUtility

class RunnableManager:
    def __init__(self):
        self.persistance = ManagerUtility.Manage('runnable')

    def get(self, **kwargs):
        return self.persistance.get(**kwargs)
    
    def first(self, **kwargs):
        return self.persistance.first(**kwargs)

    def add_module(self, workflow_id, package, function_name):
        return self.persistance.add_module(workflow_id, package, function_name)
    
    def create_runnable(self, user_id, workflow, script, provenance, args):
        return self.persistance.create_runnable(user_id, workflow, script, provenance, args)

    def add_return(self, runnable_id, retval):
        return self.persistance.add_return(runnable_id, retval)
    
    def invoke_module(self, runnable_id, function_name, package):
        return self.persistance.invoke_module(runnable_id, function_name, package)
    
    def update_runnable(self, properties):
        return self.persistance.update_runnable(properties)

    def runnables_of_user(self, user_id):
        return self.persistance.runnables_of_user(user_id)
    
runnablemanager = RunnableManager()