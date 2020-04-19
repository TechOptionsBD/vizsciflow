import json
from ...graphutil import RunnableItem, ModuleItem, ValueItem, DataPropertyItem

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
       
        for output in self.Outputs():
            out_json = output.json()
            json["nodeDataArray"].extend(out_json["nodeDataArray"])
            if out_json["nodeDataArray"]:
                out_node = out_json["nodeDataArray"][0]
                link = { "from": self._node.id, "frompid": out_node["key"], "to": out_node["key"], "topid": self._node.id, "value": "Output"}
                json["linkDataArray"].append(link)
        
        for output in self.Inputs():
            out_json = output.json()
            json["nodeDataArray"].extend(out_json["nodeDataArray"])
            if out_json["nodeDataArray"]:
                out_node = out_json["nodeDataArray"][0]
                link = { "from": out_node["key"], "frompid": self._node.id, "to": self._node.id, "topid": out_node["key"], "value": "Input"}
                json["linkDataArray"].append(link)
                       
        return json
        
           
class Run(object):
    def __init__(self, run_id = None, runItem = None):
        self._node = RunnableItem.load(run_id = run_id) if run_id else runItem
    
    @staticmethod
    def get(runid = None, workflow_id = None):
        try:
            runs = []
            runItems = RunnableItem.load(runid, workflow_id)
            for run in runItems:
                runs.append(Run(runItem = run))
                #yield Run(runItem = run)
            return runs
        except:
            raise ValueError("Runnable with id {0} doesn't exist.", runid)
        
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
            mod_json = module.json()
            json["nodeDataArray"].extend(mod_json["nodeDataArray"])
            if mod_json["nodeDataArray"]:
                mod_node = mod_json["nodeDataArray"][0]
                link = { "from": self._node.id, "frompid": mod_node["key"], "to": mod_node["key"], "topid": str(self._node.id), "value": "Module"}
                json["linkDataArray"].append(link)
        return json
    
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
