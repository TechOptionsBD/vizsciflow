import os
from json import dumps
import itertools
import operator

from ...graphutil import RunnableItem, ModuleItem, ValueItem, WorkflowItem, UserItem
from ...models import User as DbUser
from app.util import Utility
from dsl.datatype import DataType
from .pluginmgr import plugincollection

    
def EmptyIfNull(value):
    return value if value else ""
    
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

def compare(data1, data2):
    node1 = data1._node if data1 else None
    node2 = data2._node if data2 else None
    json = [{"Heading": { "Title": "Node", "First": node1.label + ":" + node1.name if node1 else "", "Second": node2.name if node2 else ""}, 
                 "Properties": [
                     {
                         "Name": "ID",
                         "First": node1.id if node1 else "",
                         "Second": node2.id if node2 else ""
                     },
                     {
                         "Name": "Value/Path",
                         "First": node1.value if node1 and node1.value else "",
                         "Second": node2.value if node2 and node2.value else ""
                     },
                     {
                         "Name": "Created",
                         "First": node1.created_on if node1 and node1.created_on else "",
                         "Second": node2.created_on  if node2 and node2.created_on else "",
                     },
                     {
                         "Name": "Modified",
                         "First": node1.modified_on if node1 and node1.modified_on else "",
                         "Second": node2.modified_on if node2 and node2.modified_on else ""
                     },
                     {
                         "Name": "Value Type",
                         "First": node1.valuetype if node1 and node1.valuetype else "",
                         "Second": node2.valuetype if node2 and node2.valuetype else ""
                     }
                     ]
                 }
             ]
    return json
        
class Data():
    def __init__(self, id = None, data_item = None, path = None):
        if data_item:
            self._node = data_item
        else:
            self._node = ValueItem.load(id = id, path = path)
    
    @staticmethod
    def get(id = None, path = None):
        return Data(id = id, path = path)
       
    def json(self):
        value = self._node.value
        if self._node.valuetype == DataType.File or self._node.valuetype == DataType.Folder:
            fs = Utility.fs_by_prefix_or_default(self._node.value)
            value = fs.basename(self._node.value)
        this_node = {"key": self._node.id, "type": "Data", "name": value}
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
    
    @staticmethod
    def compare(data1, data2, deep = False):
        node1 = data1._node if data1 else None
        node2 = data2._node if data2 else None
        json = [{"Heading": { "Title": "Data", "First": node1.name if node1 else "", "Second": node2.name if node2 else ""}, 
                     "Properties": [
                         {
                             "Name": "ID",
                             "First": node1.id if node1 else "",
                             "Second": node2.id if node2 else ""
                         },
                         {
                             "Name": "Value/Path",
                             "First": node1.value if node1 and node1.value else "",
                             "Second": node2.value if node2 and node2.value else ""
                         },
                         {
                             "Name": "Created",
                             "First": node1.created_on if node1 and node1.created_on else "",
                             "Second": node2.created_on  if node2 and node2.created_on else "",
                         },
                         {
                             "Name": "Modified",
                             "First": node1.modified_on if node1 and node1.modified_on else "",
                             "Second": node2.modified_on if node2 and node2.modified_on else ""
                         },
                         {
                             "Name": "Value Type",
                             "First": node1.valuetype if node1 and node1.valuetype else "",
                             "Second": node2.valuetype if node2 and node2.valuetype else ""
                         }
                         ]
                     }
                 ]
        return json
    
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

    def __init__(self, id=None, name = None, package = None, moduleItem=None):
        self._node = moduleItem if moduleItem else ModuleItem.load(module_id=id, name = name, package = package) 
    
    @staticmethod
    def get(name, package = None):
        return Module(name = name, package = package)
    
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
    
    @staticmethod
    def compare(module1, module2, deep = False):
        node1 = module1._node if module1 else None
        node2 = module2._node if module2 else None
        json = [{"Heading": { "Title": "Module", "First": node1.name if node1 else "", "Second": node2.name if node2 else ""}, 
                     "Properties": [
                         {
                             "Name": "ID",
                             "First": node1.id if node1 else "",
                             "Second": node2.id if node2 else ""
                         },
                         {
                             "Name": "Package",
                             "First": node1.package if node1 and node1.package else "",
                             "Second": node2.package if node2 and node2.package else ""
                         },
                         {
                             "Name": "Created",
                             "First": str(node1.created_on) if node1 and node1.created_on else "",
                             "Second": str(node2.created_on)  if node2 and node2.created_on else "",
                         },
                         {
                             "Name": "Modified",
                             "First": str(node1.modified_on) if node1 and node1.modified_on else "",
                             "Second": str(node2.modified_on) if node2 and node2.modified_on else ""
                         },
                         {
                             "Name": "Status",
                             "First": node1.status if node1 and node1.status else "",
                             "Second": node2.status if node2 and node2.status else ""
                         },
                         {
                             "Name": "Inputs",
                             "First": str(len(node1.inputs)) if node1 else "",
                             "Second": str(len(node2.inputs)) if node2 else ""
                         },
                         {
                             "Name": "Outputs",
                             "First": str(len(node1.outputs)) if node1 else "",
                             "Second": str(len(node2.outputs)) if node2 else ""
                         }
                         ]
                     }]
#         if deep:
#             from2 = []
#             for m1 in module1.inputs():
#                 addsize = len(from2)
#                 if node2:
#                     for m2 in module2.inputs():
#                         if m1._node.name == m2._node.name and m2 not in from2:
#                             json.extend(Data.compare(m1, m2))
#                             from2.append(m2)
#                 if addsize == len(from2):
#                     json.extend(Data.compare(m1, None))
#             
#             for m2 in node2.inputs():
#                 if m2 not in from2:
#                     json.extend(Data.compare(None, m2))
#         
#             from2 = []
#             for m1 in node1.outputs():
#                 addsize = len(from2)
#                 if node2:
#                     for m2 in node2.outputs():
#                         if m1.name == m2.name and m2 not in from2:
#                             json.extend(Data.compare(m1, m2))
#                             from2.extend(m2)
#                 if addsize == len(from2):
#                     json.extend(Data.compare(m1, None))
#             
#             for m2 in node2.outputs:
#                 if m2 not in from2:
#                     json.append(Data.extend(None, m2))
                    
        return json
        
class Run(object):
    def __init__(self, id = None, runItem = None):
        self._node = RunnableItem.load(id = id) if id else runItem
    
    @staticmethod
    def get(id = None, workflow_id = None):
        try:        
            runItems = RunnableItem.load(int(id) if id else None, int(workflow_id) if workflow_id else None)
            if not isinstance(runItems, list):
                return Run(runItem = runItems)
            
            return [Run(runItem = run) for run in runItems]
        except:
            raise ValueError("Runnable with id {0} doesn't exist.", id)
        
    def modules(self, index = None, name = None):
        modules = []
        moduleItems = self._node.modules
        if index:
            modules.append(Module(moduleItem=moduleItems[int(index)]))
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
    
    @staticmethod
    def compare(run1, run2, deep = False):
        node1 = run1._node if run1 else None
        node2 = run2._node if run2 else None
        json = [{"Heading": { "Title": "Run", "First": node1.name if node1 else "", "Second": node2.name if node2 else ""}, 
                     "Properties": [
                         {
                             "Name": "ID",
                             "First": node1.id if node1 else "",
                             "Second": node2.id if node2 else ""
                         },
                         {
                             "Name": "Created",
                             "First": str(node1.created_on) if node1 and node1.created_on else "",
                             "Second": str(node2.created_on)  if node2 and node2.created_on else "",
                         },
                         {
                             "Name": "Modified",
                             "First": str(node1.modified_on) if node1 and node1.modified_on else "",
                             "Second": str(node2.modified_on) if node2 and node2.modified_on else ""
                         },
                         {
                             "Name": "Output",
                             "First": node1.out if node1 and node1.out else "",
                             "Second": node2.out if node2 and node2.out else ""
                         },
                         {
                             "Name": "Error",
                             "First": node1.error if node1 and node1.error else "",
                             "Second": node2.error if node2 and node2.error else ""
                         },
                         {
                             "Name": "Status",
                             "First": node1.status if node1 and node1.status else "",
                             "Second": node2.status if node2 and node2.status else ""
                         },
                        {
                            "Name": "Duration",
                            "First": str(node1.duration) if node1 and node1.duration else "",
                            "Second": str(node2.duration) if node2 and node2.duration else ""
                        },
                         {
                             "Name": "Modules",
                             "First": str(len(node1.modules)) if node1 else "",
                             "Second": str(len(node2.modules)) if node2 else ""
                         }
                         ]
                     }]
        if deep:
            from2 = []
            if run1:
                for m1 in run1.modules():
                    addsize = len(from2)
                    if run2:
                        for m2 in run2.modules():
                            if m1._node.name == m2._node.name and m2 not in from2:
                                json.extend(Module.compare(m1, m2, deep))
                                from2.append(m1._node.name)
                    if addsize == len(from2):
                        json.extend(Module.compare(m1, None))
                
            for m2 in run2.modules():
                if m2._node.name not in from2:
                    json.extend(Module.compare(None, m2))
                    
        return json
       
    def json(self):
        this_node = {"key": self._node.id, "type": "Run", "name": self._node.name}
        json = { "nodeDataArray" : [this_node], "linkDataArray":[]}
        for module in self.modules():
            json = merge_json(json, module.json(), 'Module')
        return json

class Workflow(object):
    def __init__(self, id = None, workflowItem = None):
        self._node = WorkflowItem.load(id = id) if id else workflowItem
    
    @staticmethod
    def Create(id = None, name = None):
        workflow = None
        if id:
            workflow = WorkflowItem.load(id = int(id) if id else None)
            if workflow:
                return workflow
        
        if not workflow:
            workflow = WorkflowItem.Create(name)
            workflow.id = id
            
        return Workflow(workflowItem = workflow)
    
    @staticmethod
    def get(id = None):
        try:        
            workflowItems = WorkflowItem.load(int(id) if id else None)
            if workflowItems:
                if not isinstance(workflowItems, list):
                    return Workflow(workflowItem = workflowItems)
            
            return [Workflow(workflowItem = workflow) for workflow in workflowItems]
        except:
            raise ValueError("Workflow with id {0} doesn't exist.", id)
        
    def modules(self, index = None, name = None):
        modules = []
        moduleItems = self._node.modules
        if index:
            modules.append(Module(moduleItem=moduleItems[int(index)]))
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
            runs.append(Run(run_item=runsItems[int(index)]))
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
    def __init__(self, id = None, userItem = None):
        self._node = UserItem.load(id = id) if id else userItem
    
    @staticmethod
    def get(id = None, username = None):
        try:
            userItems = None
            if not id and username:
                user = DbUser.query.filter_by(username = username).first()
                if user:
                    id = user.id
            
            id = int(id) if id else None
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
            workflows.append(Workflow(workflow_item=workflowsItems[int(index)]))
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
            runs.append(Run(run_item=runsItems[int(index)]))
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

class Plugin():
    def __init__(self, name):
        self._plugin = plugincollection.get(name)
    
    @staticmethod
    def get(name):
        return Plugin(name)
    
    def apply(self, *args, **kwargs):
        return self._plugin.perform_operation(*args, **kwargs)
        
class View(object):
    def __init__(self):
        pass
    
    @staticmethod             
    def graph(node):
        return dumps(node.json())

    @staticmethod             
    def compare(node1, node2, deep = True):
        return dumps(node1.compare(node1, node2, deep))
   
class Monitor(object):
    
    def time(self, node_id):
        pass
    
    def proportional_time(self, id):
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
