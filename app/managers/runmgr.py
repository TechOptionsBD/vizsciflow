from app.managers.mgrutil import ManagerUtility

class RunnableManager:
    def __init__(self):
        self.persistance = ManagerUtility.Manage('runnable')

    def add_module(self, workflow_id, package, function_name):
        return self.persistance.add_module(workflow_id, package, function_name)
    
    def create_runnable(self, user, workflow, script, provenance, args):
        return self.persistance.create_runnable(user, workflow, script, provenance, args)
    
    def invoke_module(self, runnable_id, function_name, package):
        return self.persistance.invoke_module(runnable_id, function_name, package)
    
    def update_runnable(self, properties):
        return self.persistance.update_runnable(properties)
        
    def get_runnables(self, **kwargs):
        return self.persistance.get_runnables(**kwargs)
    
    def get_runnable(self, **kwargs):
        return self.get_runnables(**kwargs).first()

    def runnables_of_user(self, user_id):
        return self.persistance.runnables_of_user(user_id)
    
runnablemanager = RunnableManager()