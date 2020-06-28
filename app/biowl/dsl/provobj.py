from json import dumps
import itertools
import operator
from ...graphutil import RunnableItem, ModuleItem, ValueItem, WorkflowItem, UserItem
from ...models import User as DbUser

def remove_duplicate_nodes(d, *args):
    getvals = operator.itemgetter(*args)
    d.sort(key = getvals)
    result = []
    for _, g in itertools.groupby(d, getvals):
        result.append(next(g))
    return result
            
def merge_json(json, other_json, relation, opposite_link = False):
    
    for other_json_item in other_json["nodeDataArray"]:
        if not any(j['key'] == other_json_item['key'] for j in json["nodeDataArray"]):
            json["nodeDataArray"].append(other_json_item)
    
    for other_json_item in other_json["linkDataArray"]:
        if not any(j['from'] == other_json_item['from'] and j['to'] == other_json_item['to'] for j in json["linkDataArray"]):
            json["linkDataArray"].append(other_json_item)
            
    if other_json["nodeDataArray"]:
#         json_node = json["nodeDataArray"][0]
#         other_node = other_json["nodeDataArray"][0]
        json_node = other_json["nodeDataArray"][0] if opposite_link else json["nodeDataArray"][0]
        other_node = json["nodeDataArray"][0] if opposite_link else other_json["nodeDataArray"][0]
        link = { "from": json_node["key"], "frompid": other_node["key"], "to": other_node["key"], "topid": json_node["key"], "value": relation}
        json["linkDataArray"].append(link)
    
    return json

# 
# def merge_json(json, other_json, link_value, opposite_link = False):
#     json["nodeDataArray"].extend(other_json["nodeDataArray"])
#     json["linkDataArray"].extend(other_json["linkDataArray"])
#     if other_json["nodeDataArray"]:
#         json_node = other_json["nodeDataArray"][0] if opposite_link else json["nodeDataArray"][0]
#         other_node = json["nodeDataArray"][0] if opposite_link else other_json["nodeDataArray"][0]
#         link = { "from": json_node["key"], "frompid": other_node["key"], "to": other_node["key"], "topid": json_node["key"], "value": link_value}
#         json["linkDataArray"].append(link)
#     
#     json["nodeDataArray"] = remove_duplicate_nodes(json["nodeDataArray"], 'key')
#     json["linkDataArray"] = remove_duplicate_nodes(json["linkDataArray"], 'from', 'to')
#     return json
    
class Data():
    def __init__(self, data_id = None, data_item = None):
        self._node = ValueItem.load(data_id = data_id) if data_id else data_item
    
    @staticmethod
    def Create(value, datatype):
        workflow = None
        if workflow_id:
            workflow = WorkflowItem.load(workflow_id = workflow_id)
            if workflow:
                return workflow
        
        if not workflow:
            workflow = WorkflowItem.Create(name)
            workflow.workflow_id = workflow_id
            
        return Workflow(workflow)
    
    def json(self):
        this_node = {"key": self._node.id, "type": "Data", "name": self._node.name}
        json = { "nodeDataArray" : [this_node], "linkDataArray":[]}
#         for output in self.Metadata():
#             out_json = output.json()
#             if out_json["nodeDataArray"]:
#                 out_node = out_json["nodeDataArray"][0]
#                 link = { "from": self.id, "frompid": out_node["key"], "to": out_node["key"], "topid": str(self.id), "value": "Output"}
#                 json["linkDataArray"].append(link)
                
        return json
    
    def metadata(self):
        properties = []
        for k,v in self._node.properties:
            properties.append(Property(k, v))
        return properties
    

class Property(object):
    def __init__(self, key, value):
        self._key = key
        self._value = value
        
        @property
        def key(self):
            return self._key
        @property
        def value(self):
            return self._value
        
class Module(object):

    def __init__(self, module_id=None, moduleItem=None):
        self._node = ModuleItem.load(module_id=module_id) if module_id else moduleItem
    
    def outputs(self):
        return [Data(data_item=output) for output in self._node.outputs]
        
    def inputs(self):
        return [Data(data_item=arg) for arg in self._node.inputs]
    
    def json(self):
        this_node = {"key": self._node.id, "type": "Module", "name": self._node.name}
        json = { "nodeDataArray" : [this_node], "linkDataArray":[]}
       
        for outdata in self.outputs():
            json = merge_json(json, outdata.json(), 'Output')
        
        for indata in self.inputs():
            json = merge_json(json, indata.json(), 'Input', True)
            
        return json
        
           
class Run(object):
    def __init__(self, run_id = None, runItem = None):
        self._node = RunnableItem.load(run_id = run_id) if run_id else runItem
    
    @staticmethod
    def get(run_id = None, workflow_id = None):
        try:        
            runItems = RunnableItem.load(run_id, workflow_id)
            if not isinstance(runItems, list):
                return Run(runItem = runItems)
            
            return [Run(runItem = run) for run in runItems]
        except:
            raise ValueError("Runnable with id {0} doesn't exist.", run_id)
        
    def modules(self, index = None, name = None):
        modules = []
        moduleItems = self._node.modules
        if index:
            modules.append(Module(moduleItem=moduleItems[index]))
        elif name:
            for module in moduleItems:
                if module.name == name:
                    modules.append(Module(moduleItem=module))
        else:
            for module in moduleItems:
                modules.append(Module(moduleItem=module))
        return modules
    
    def nodes(self, key, value = None):
        return self._node.nodes_by_property(key, value)
       
    def json(self):
        this_node = {"key": self._node.id, "type": "Run", "name": self._node.name}
        json = { "nodeDataArray" : [this_node], "linkDataArray":[]}
        for module in self.modules():
            json = merge_json(json, module.json(), 'Module')
        return json

class Workflow(object):
    def __init__(self, workflow_id = None, workflowItem = None):
        self._node = WorkflowItem.load(workflow_id = workflow_id) if workflow_id else workflowItem
    
    @staticmethod
    def Create(workflow_id = None, name = None):
        workflow = None
        if workflow_id:
            workflow = WorkflowItem.load(workflow_id = workflow_id)
            if workflow:
                return workflow
        
        if not workflow:
            workflow = WorkflowItem.Create(name)
            workflow.workflow_id = workflow_id
            
        return Workflow(workflowItem = workflow)
    
    @staticmethod
    def get(workflow_id = None):
        try:        
            workflowItems = WorkflowItem.load(workflow_id)
            if not isinstance(workflowItems, list):
                return Workflow(workflowItem = workflowItems)
            
            return [Workflow(workflowItem = workflow) for workflow in workflowItems]
        except:
            raise ValueError("Workflow with id {0} doesn't exist.", workflow_id)
        
    def modules(self, index = None, name = None):
        modules = []
        moduleItems = self._node.modules
        if index:
            modules.append(Module(moduleItem=moduleItems[index]))
        elif name:
            for module in moduleItems:
                if module.name == name:
                    modules.append(Module(moduleItem=module))
        else:
            for module in moduleItems:
                modules.append(Module(moduleItem=module))
        return modules
       
    def runs(self, index = None, name = None):
        runs = []
        runsItems = self._node.Runs
        if index:
            runs.append(Run(run_item=runsItems[index]))
        elif name:
            for run in runsItems:
                if run.name == name:
                    runs.append(Run(runItem=run))
        else:
            for run in runsItems:
                runs.append(Run(runItem=run))
        return runs
    
    def json(self):
        this_node = {"key": self._node.id, "type": "Workflow", "name": self._node.name}
        json = { "nodeDataArray" : [this_node], "linkDataArray":[]}
        for run in self.runs():
            json = merge_json(json, run.json(), 'Run')
        return json

class User(object):
    def __init__(self, user_id = None, userItem = None):
        self._node = UserItem.load(user_id = user_id) if user_id else userItem
    
    @staticmethod
    def get(id = None, username = None):
        try:
            userItems = None
            if not id and username:
                user = DbUser.query.filter_by(username = username).first()
                if user:
                    id = user.id
                
            userItems = UserItem.load(id)
            
            if not isinstance(userItems, list):
                return User(userItem = userItems)
            
            return [User(userItem = user) for user in userItems]
        except:
            raise ValueError("User with id {0} doesn't exist.", id)

    def workflows(self, index = None, name = None):
        workflows = []
        workflowsItems = self._node.Workflows
        if index:
            workflows.append(Workflow(workflow_item=workflowsItems[index]))
        elif name:
            for workflow in workflowsItems:
                if workflow.name == name:
                    workflows.append(Workflow(workflow_item=workflow))
        else:
            for workflow in workflowsItems:
                workflows.append(Workflow(workflowItem=workflow))
        return workflows

    def runs(self, index = None, name = None):
        runs = []
        runsItems = self._node.Runs
        if index:
            runs.append(Run(run_item=runsItems[index]))
        elif name:
            for run in runsItems:
                if run.name == name:
                    runs.append(Run(runItem=run))
        else:
            for run in runsItems:
                runs.append(Run(runItem=run))
        return runs
        
    def json(self):
        this_node = {"key": self._node.id, "type": "User", "name": self._node.name}
        json = { "nodeDataArray" : [this_node], "linkDataArray":[]}
        for workflow in self.workflows():
            json = merge_json(json, workflow.json(), 'Workflow')
        return json

class View(object):
    def __init__(self):
        pass
    
    @staticmethod             
    def graph(node):
        return dumps(node.json())
        
class Monitor(object):
    
    def time(self, node_id):
        pass
    
    def proportional_time(self, module_id):
        pass
    
    def metric(self):
        pass
    
    def aggr(self, property):
        pass
    
    def proportional_aggr(self, property):
        pass
    
    def aggr_metric(self):
        pass
    
class Stat(object):
    @staticmethod
    def Similarity(g1, g2):
        pass
    
    @staticmethod
    def get(condition):
        pass
    
    @staticmethod
    def centrality(workflow):
        pass
    
    @staticmethod
    def corelation(property1, property2):
        pass
    
    @staticmethod
    def predict(property):
        pass
    
    @staticmethod
    def pattern(property):
        pass
