from flask import g
from app.models import Status

from ..models import Workflow
from datetime import datetime

def mockruns():
    if 'mockruns' not in g:
        g.mockruns = {}
    return g.mockruns

class ModuleMock:
    def __init__(self, name, package = None):
        self.package = package
        self._name = name
        self._id = 0
        self._inputs = []
        self._outputs = []
        self.logs = []
        self.status = Status.RECEIVED
        _started_on = datetime.utcnow()
        _duration = 0
        
    def name(self):
        return self._name
        
    def inputs(self):
        return self._inputs
    
    def outputs(self):
        return self._outputs
    
    @property
    def run_id(self):
        return list(self.runs)[0].id
    
    @property
    def duration(self):
        if self.status == Status.STARTED:
            self._duration = datetime.utcnow() - self._started_on
            #graph().push(self)
            
        return self._duration  
    
    @duration.setter
    def duration(self, value):
        self._duration = value
    
    @property
    def id(self):
        return self._id
    
    def start(self):
        self.status = Status.STARTED
        self._started_on = datetime.utcnow()
        
        self._duration = 0                    
        #self.add_log(Status.STARTED, LogType.INFO)
    
    def succeeded(self):
        self.status = Status.SUCCESS
        #self.add_log(Status.SUCCESS, LogType.INFO)
        self.modified_on = datetime.utcnow()
        self._duration = datetime.utcnow() - self._started_on
    
    def failed(self, log = "Task Failed."):
        self.status = Status.FAILURE
#        self.add_log(log, LogType.INFO)
        self.modified_on = datetime.utcnow()
        self._duration = datetime.utcnow() - self._started_on
    
    def add_arg(self, datatype, value):
        self._inputs.append(value)
        return value
    
    def add_input(self, user_id, datatype, value, rights, **kwargs):
        self._inputs.append(value)
        return datatype
    
    def add_outputs(self, dataAndType):
        result = ()        
        for d in dataAndType:
            self._outputs.append(str(d[1]))
            result += (d[1],)
        return result
    
    def to_json_log(self):
        
        data = [{ "datatype": "Unknown", "data": str(data)} for data in self._outputs]
            
        return { 
            'name': self._name if self._name else "", 
            'status': self.status,
            'data': data
        }
            
class RunnableMock:
    def __init__(self, user_id = 2, workflow_id = None, script = None, provenance = None, args = None):
        self.user_id = user_id
        self.workflow_id = workflow_id
        self.script = script
        self.provenance = provenance
        self.args = args
        self.out = ""
        self.error = ""
        self.view = ""
        self._modules = []
        self._status = Status.RECEIVED
        maxid = max(mockruns().keys()) if mockruns().keys() else 0
        self._id = maxid + 1
        mockruns().update({self._id: self})
    
    @staticmethod
    def create(user_id, workflow_id, script, provenance, args):
        return RunnableMock(user_id, workflow_id, script, provenance, args)
    
    @staticmethod
    def load(runnable_id):
        return mockruns()[runnable_id]
    
    def add_module(self, package, function):
        item = ModuleMock(function, package)
        item._id = len(self._modules) + 1
        self._modules.append(item)
        return item
    
    @staticmethod
    def load_for_users(user_id):
        runs = []
        for r in mockruns():
            if r.user_id == user_id:
                runs.append(r)
        return runs
    
    def update(self):
        pass
    
    def set_status(self, value, update = True):
        self._status = value
        self.update()
        
    @property
    def id(self):
        return self._id
    
    def to_json_log(self):
        log = []
        
        for module in self._modules:
            log.append(module.to_json_log())

        return {
            'id': self.id,
            'script': self.script,
            'status': self._status,
            'out': self.out,
            'err': self.error,
            'duration': "{0:.3f}".format(0),
            'log': log
        }
        
class WorkflowMock:
    @staticmethod
    def add_module(package, function):
        pass
    
    @staticmethod
    def load(workflow_id):
        pass
    
    
class ModuleManagerMock():   
    @staticmethod
    def create_runnable(user_id, workflow_id, script, provenance, args):
        return RunnableMock.create(user_id, workflow_id, script, provenance, args)
    
#     @staticmethod
#     def update_runnable(properties):
#         try:
#             runnable = RunnableItem(properties['workflow_id'], properties['script'], properties['arguments'])
#             workflow = properties['workflow_id']
#             result = runnable.update_json(properties)            
#             print(result)
#             run = graphgen.graph.run("MATCH (x) WHERE x.workflow_id = {dict_param} SET x = {dict_param2}",{'dict_param': workflow, 'dict_param2': result}).data()
#             return run
#         except Exception as e:
#             return e
    
    @staticmethod
    def add_module(workflow_id, package, function):
        workflowItem = WorkflowMock.load(workflow_id)
        return workflowItem.add_module(package, function)
    
    @staticmethod
    def create_task(runnable_id, function_name, package):
        runnableItem = RunnableMock.load(runnable_id)
        return runnableItem.add_module(function_name, package)
    
    @staticmethod
    def get_workflow(workflow_id):
        return Workflow.query.get(workflow_id)    
    
#    @staticmethod
#     def create_workflow(user_id, name, desc, script, access, users, temp, derived = 0):
#         workflow = WorkflowItem(name, desc if desc else '', script, 2 if not access else int(access), users, temp, derived)
#         workflow = graphgen.graph.run(
#             statement="CREATE (x) SET x = {dict_param}",
#             parameters={'dict_param': workflow.json()})
#         
#         matcher = NodeMatcher(graphgen.graph)
#         user = matcher.match(id=user_id).first()
#         Relationship(user, "WORKFLOW", workflow)
#         
#         return workflow
    
    @staticmethod
    def create_workflow(user_id, name, desc, script, access, users, temp, derived = 0):
        return Workflow.create(user_id, name, desc if desc else '', script, 2 if not access else int(access), users, temp, derived)

    @staticmethod
    def get_runnable(runnable_id):
        return RunnableMock.load(runnable_id)
    
    @staticmethod
    def runnables_of_user(user_id):
        return RunnableMock.load_for_users(user_id)