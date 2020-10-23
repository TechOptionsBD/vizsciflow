from py2neo.data import Node, PropertyDict
from py2neo.matching import NodeMatch, NodeMatcher
from dsl.datatype import DataType
from .provobj import merge_json
from app.util import Utility
from dsl.symtab import SymbolTable

def merge_json_seq(json, other_json, relation, opposite_link = False):
    
    if not json["nodeDataArray"]:
        return other_json
    if not other_json["nodeDataArray"]:
        return json
    
#    conn_node = json["nodeDataArray"][-1]
    for other_json_item in other_json["nodeDataArray"]:
        if not any(j['key'] == other_json_item['key'] for j in json["nodeDataArray"]):
            json["nodeDataArray"].append(other_json_item)
    
    for other_json_item in other_json["linkDataArray"]:
        if not any(j['from'] == other_json_item['from'] and j['to'] == other_json_item['to'] for j in json["linkDataArray"]):
            json["linkDataArray"].append(other_json_item)
            
#     if other_json["nodeDataArray"]:
# #         json_node = json["nodeDataArray"][0]
# #         other_node = other_json["nodeDataArray"][0]
#         json_node = other_json["nodeDataArray"][0] if opposite_link else conn_node
#         other_node = conn_node if opposite_link else other_json["nodeDataArray"][0]
#         link = { "from": json_node["key"], "frompid": other_node["key"], "to": other_node["key"], "topid": json_node["key"], "value": relation}
#         json["linkDataArray"].append(link)
    
    return json

class GraphNode(object):
    __node = None
    __primarykey__ = "__id__"
    __primaryvalue__ = 10000
    
    __properties = {}
        
    def __init__(self, primarylabel):
        GraphNode.__primaryvalue__ += 1
        self.__primaryvalue__ = GraphNode.__primaryvalue__
        if not self.__primarylabel__:
            self.__primarylabel__ = primarylabel
       
    @property
    def id(self):
        return self.__node.identity if self.__node else self.__primaryvalue__
        
    @id.setter
    def id(self, primaryvalue):
        if self.__node.graph:
            raise ValueError("You can't change the id of an existing node.")
        
        self.__primaryvalue__ = primaryvalue
        
    @property
    def node(self):
        if self.__node is None:
            self.__node = Node(self.__primarylabel__)
        
        if not hasattr(self.__node, "__primarylabel__"):
            setattr(self.__node, "__primarylabel__", self.__primarylabel__)
        if not hasattr(self.__node, "__primarykey__"):
            setattr(self.__node, "__primarykey__", self.__primarykey__)

        return self.__node
    
    def push(self, graph):
        
        if self.node.graph is not None:
            graph.push(self.node)
        else:
            primary_key = getattr(self.node, "__primarykey__", "__id__")
            if primary_key == "__id__":
                graph.create(self.node)
            else:
                graph.merge(self.node)
        
        for k,v in self.__properties:
            setattr(self.__node, k, v)
            
    def pull(self, graph):
        
        if self.node.graph is None:
            self.__node = NodeMatcher.match(self, self.__primarylabel__).where("id(_) = %d" % self.id).first()
        
        graph.pull(self.__node)
            
class Data(GraphNode):
    __primarylabel__ = "Data"
    
    def __init__(self, name=None, value=None):
        super().__init__("Data")
        self.valuetype = DataType.Unknown
        self.datatype = str(type(value))
        self.value = value
        self.name = name
        self.expected = False

    def json(self):
        value = self.value
        if value and (self.valuetype == DataType.File or self.valuetype == DataType.Folder):
            fs = Utility.fs_by_prefix_or_default(self.value)
            value = fs.basename(self.value)
        
        node_value = self.name if self.expected else self.value 
        
        this_node = {"key": self.id, "type": "Data", "name": str(node_value) if node_value else ""}
        return { "nodeDataArray" : [this_node], "linkDataArray":[]}
        
    def push(self, graph):        
        super().push(graph)
        
        setattr(self.__node, "valuetype", self.valuetype)
        setattr(self.__node, "datatype", self.datatype)
        setattr(self.__node, "value", self.value)
        setattr(self.__node, "name", self.name)
        
#     def match(self):
# #         class GraphObjectMatcher(NodeMatcher):
# #             
# #         GraphObjectMatcher()::Init
# #         NodeMatcher.__init__(self, self._coerce_to_graph(repository))
# #         self._object_class = object_class
# #         self._match_class = type("%sMatch" % self._object_class.__name__,
# #                                  (GraphObjectMatch,), {"_object_class": object_class})
# #         
# #         GraphObjectMatcher::match
# #         cls = self._object_class
#         properties = {}
#         if primary_value is not None:
#             return NodeMatcher.match(self, cls.__primarylabel__).where("id(_) = %d" % primary_value)
#         return NodeMatcher.match(self, cls.__primarylabel__, **properties)
#     
#         matcher.first()
#         
#         return self._object_class.wrap(super(GraphObjectMatch, self).first())
#         
#         NodeMatch.first
#         return self.graph.evaluate(*self._query_and_parameters())
    
class Module(GraphNode):
    
    __primarylabel__ = "Module"
    
    def __init__(self, parent = None, name = None, package = None):
        super().__init__("Module")
        
        self._modules = []
        self._inputs = []
        self._outputs = []        
        self._package = package
        self._name = name
        self._args = []
        self._kwargs = {}
        self._parent = parent
        
        self.properties = PropertyDict()
        self._symtab = None

    def name(self):
        return self._name
    
    def add_symtab(self):
        self._symtab = SymbolTable()
                
    def add_var(self, name, value):
        if self._symtab:
            return self._symtab.add_var(name, value)
        elif self._parent:
            return self._parent.add_var(name, value)

    def update_var(self, name, value):
        if self._symtab and self._symtab.var_exists(name):
            return self._symtab.update_var(name, value)
        elif self._parent:
            return self._parent.update_var(name, value)

    def var_exists(self, name):
        if self._symtab and self._symtab.var_exists(name):
            return True
        elif self._parent:
            return self._parent.var_exists(name)
        
    def check_var(self, name):
        if not self.var_exists(name):
            raise ValueError("var {0} does not exist".format(name))
        return True
            
    def get_var(self, name):
        '''
        Gets value of a variable
        :param name:
        '''
        self.check_var(name)
        if self._symtab and self._symtab.var_exists(name):
            return self._symtab.get_var(name)
        elif self._parent:
            return self._parent.get_var(name)
            
    def Subs(self):
        return self._modules
    
    def All(self, predicates=tuple(), order_by=tuple()):
        yield self
        for m in self.modules():
            yield m.All()

    def modules(self):
        return self._modules
    
    def outputs(self):
        return self._outputs
    
    def inputs(self):
        return self._inputs
    
    def json(self):
        this_node = {"key": self.id, "type": self.__primarylabel__, "name": self._name if self._name else ""}
        json = { "nodeDataArray" : [this_node], "linkDataArray":[]}

        for module in self.modules():
            json = merge_json_seq(json, module.json(), 'Module')
        
        for outdata in self.outputs():
            json = merge_json(json, outdata.json(), 'Output')
        
        for indata in self.inputs():
            if isinstance(indata, Data) and indata.value and indata.expected:
                continue
            json = merge_json(json, indata.json(), 'Input', True)
                
        return json
    
    def addmodule(self, package, name, *args, **kwargs):
        self._package = package
        self._name = name
        if args:
            self._args = args
        if kwargs:
            self._kwargs = kwargs
    
    def push(self, graph):
        
        super.push(graph)
        
        for i in self.inputs():
            i.push(graph)
        
        for o in self.outputs():
            o.push(graph)
                
        for m in self.modules():
            m.push(graph)
    
    def pull(self, graph):
        
        if self.node.graph is None:
            self.__node = NodeMatcher.match(self, self.__primarylabel__).where("id(_) = %d" % self.node.identity).first()
                
        graph.pull(self.__node)
        
        for i in self.inputs():
            i.pull(graph)
        
        for o in self.outputs():
            o.pull(graph)
                
        for m in self.modules():
            m.pull(graph)
#         
#     # related objects    
#         self.__match_args = {"nodes": (self.node, None), "r_type": relationship_type}
#             self.__start_node = False
#             self.__end_node = True
#             self.__relationship_pattern = "(a)-[_:%s]->(b)" % cypher_escape(relationship_type)
            
            
    def __db_pull__(self, tx):
        related_objects = {}
        matcher = tx.graph.match(**self.__match_args)
        if self.order_by:
            matcher = matcher.order_by(self.order_by)
        for r in matcher:
            nodes = []
            n = self.node
            a = r.start_node
            b = r.end_node
            if a == b:
                nodes.append(a)
            else:
                if self.__start_node and a != n:
                    nodes.append(r.start_node)
                if self.__end_node and b != n:
                    nodes.append(r.end_node)
            for node in nodes:
                related_object = self.related_class.wrap(node)
                related_objects[node] = (related_object, PropertyDict(r))
        self._related_objects[:] = related_objects.values()

    def __db_push__(self, tx):
        related_objects = self._related_objects
        # 1. merge all nodes (create ones that don't)
        for related_object, _ in related_objects:
            tx.merge(related_object)
        # 2a. remove any relationships not in list of nodes
        subject_id = self.node.identity
        tx.run("MATCH %s WHERE id(a) = $x AND NOT id(b) IN $y DELETE _" % self.__relationship_pattern,
               x=subject_id, y=[obj.__node__.identity for obj, _ in related_objects])
        # 2b. merge all relationships
        for related_object, properties in related_objects:
            tx.run("MATCH (a) WHERE id(a) = $x MATCH (b) WHERE id(b) = $y "
                   "MERGE %s SET _ = $z" % self.__relationship_pattern,
                   x=subject_id, y=related_object.__node__.identity, z=properties)

# split
# join

class AssignModule(Module):
    __primarylabel__ = "AssignModule"
    
    def __init__(self, parent, var, value):
        super().__init__(parent, "=")
        
        parent.update_var(var, self) if parent.var_exists(var) else parent.add_var(var, self)
        self.var = var
        self.inputs().append(value)
        self.__primarylabel__ = "Operator"
    
    def json(self):
        this_node = {"key": self.id, "type": self.__primarylabel__, "name": self.var + self._name}
        json = { "nodeDataArray" : [this_node], "linkDataArray":[]}
        for indata in self.inputs():
            if isinstance(indata, Data) and indata.value and indata.expected:
                continue
            json = merge_json(json, indata.json(), 'Input', True)
        
        return json
        
class CondModule(Module):
    __primarylabel__ = "LogModule"
    
    def __init__(self, parent):
        super().__init__(parent, "Logical")
        
class BinModule(Module):
    __primarylabel__ = "BinaryModule"
    
    def __init__(self, parent, opname, left, right):
        super().__init__(parent, opname)
        self.inputs().extend([left, right])

class UnaryModule(Module):
    __primarylabel__ = "UnaryModule"
    
    def __init__(self, parent, left):
        super().__init__(parent, "")
        self.inputs().append(left)
                
class IfModule(Module):
    __primarylabel__ = "IfModule"
    
    def __init__(self, parent, cond):
        super().__init__(parent, "If")
        self.cond = cond
    
    def json(self):
        this_node = {"key": self.id, "type": "If", "name": ""}
        json = { "nodeDataArray" : [this_node], "linkDataArray":[]}

        if self.cond:
            json = merge_json(json, self.cond.json(), 'Condition', True)
            
        if len(self._modules) > 0:
            json = merge_json(json, self._modules[0].json(), 'Module')

        if len(self._modules) > 1:
            json = merge_json(json, self._modules[0].json(), 'Module')

                
        return json    
                           
class Workflow(Module):
    __workflow_id = None
    __primarylabel__ = "Workflow"
    
    def __init__(self, parent = None, workflow_id = None, name = None):
        super().__init__(parent, name)
        if not self.__workflow_id:
            self.__workflow_id = workflow_id
        self._symtab = SymbolTable()
    
    @property
    def id(self):
        return self.__workflow_id
    
    @id.setter
    def id(self, workflow_id):
        self.__workflow_id = workflow_id
    
    def push(self, graph):        
        super.push(graph)
        
        setattr(self.__node, "workflow_id", self.__workflow_id)
    
    def json(self):
        this_node = {"key": self.__workflow_id, "type": "Workflow", "name": self._name if self._name else ""}
        #this_json = { "nodeDataArray" : [this_node], "linkDataArray":[]}
        
        json = { "nodeDataArray" : [], "linkDataArray":[]}
        for module in self.modules():
            json = merge_json_seq(json, module.json(), 'Module')
        
        return json
#         return merge_json(this_json, json, 'Module') 
        
class View(object):
    def __init__(self):
        pass
    
    @staticmethod
    def graph(node):
        return node.json()

    @staticmethod             
    def compare(node1, node2, deep = True):
        node1 = Run.get(node1)
        node2 = Run.get(node2)
        return node1.compare(node1, node2, deep)