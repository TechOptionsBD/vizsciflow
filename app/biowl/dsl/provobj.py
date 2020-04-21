from json import dumps 
from ...graphutil import RunnableItem, ModuleItem, ValueItem

def merge_json(json, other_json, link_value, opposite_link = False):
    json["nodeDataArray"].extend(other_json["nodeDataArray"])
    json["linkDataArray"].extend(other_json["linkDataArray"])
    if other_json["nodeDataArray"]:
        json_node = other_json["nodeDataArray"][0] if opposite_link else json["nodeDataArray"][0]
        other_node = json["nodeDataArray"][0] if opposite_link else other_json["nodeDataArray"][0]
        link = { "from": json_node["key"], "frompid": other_node["key"], "to": other_node["key"], "topid": json_node["key"], "value": link_value}
        json["linkDataArray"].append(link)
                
    return json
    
class Data():
    def __init__(self, data_id = None, data_item = None):
        self._node = ValueItem.load(data_id = data_id) if data_id else data_item
    
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
    
    def Metadata(self):
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

    def __init__(self, module_id=None, module_item=None):
        self._node = ModuleItem.load(module_id=module_id) if module_id else module_item
    
    def Outputs(self):
        return [Data(data_item=output) for output in self._node.outputs]
        
    def Inputs(self):
        return [Data(data_item=arg) for arg in self._node.inputs]
    
    def json(self):
        this_node = {"key": self._node.id, "type": "Module", "name": self._node.name}
        json = { "nodeDataArray" : [this_node], "linkDataArray":[]}
       
        for outdata in self.Outputs():
            json = merge_json(json, outdata.json(), 'Output')
        
        for indata in self.Inputs():
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
        
    def view(self, viewer = None):
        pass
    
#     def module(self, index):
#         return self._node.task_by_index(index)
    
    def Modules(self, index = None, name = None):
        modules = []
        moduleItems = self._node.modules
        if index:
            modules.append(Module(module_item=moduleItems[index]))
        elif name:
            for module in moduleItems:
                if module.name == name:
                    modules.append(Module(module_item=module))
        else:
            for module in moduleItems:
                modules.append(Module(module_item=module))
        return modules
        #return self._node.task_by_index(index) if index else self._node.task_by_name(name)
    
    def nodes(self, key, value = None):
        return self._node.nodes_by_property(key, value)
       
    def json(self):
        this_node = {"key": self._node.id, "type": "Run", "name": self._node.name}
        json = { "nodeDataArray" : [this_node], "linkDataArray":[]}
        for module in self.Modules():
            json = merge_json(json, module.json(), 'Module')
        return dumps(json)
    
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
