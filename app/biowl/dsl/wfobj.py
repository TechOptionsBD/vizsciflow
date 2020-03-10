import uuid
from ...models import DataType

class WfRuns:
    def Filter(self, **kwargs):
        pass

class WfModel:
    pass

class WfWorkflow(WfModel):
    def __init__(self, name):
        self.name = name
        self.id = str(uuid.uuid4())
        self.subworkflows = []
        self.modules = []
        self.properties = []
        pass
    
    def Filter(self, **kwargs):
        pass
    
    @staticmethod
    def Create(name):
        return WfWorkflow(name)
    
    @staticmethod
    def Runs():
        pass
    
    def Add(self, subworkflow):
        self.subworkflows.append(subworkflow)
    def remove(self, subworkflow):
        pass

class WfModule(WfModel):
    def __init__(self, name, package):
        self.package = package
        self.name = name
        self.id = str(uuid.uuid4())
        self.inputs = ()
        self.outputs = ()
        self.properties = []
    
    @staticmethod
    def Create(name, package):
        return WfModule(name, package)
    
class WfData(WfModel):
    def __init__(self, name, value, datatype = DataType.Unknown):
        self.name = name
        self.value = value
        self.datatype = datatype
        self.id = str(uuid.uuid4())
        self.properties = []
    
    @staticmethod
    def Create(name, value):
        return WfData(name, value)

class WfProperty(WfModel):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.id = str(uuid.uuid4())
    
    @staticmethod
    def Create(name, value):
        return WfProperty(name, value)
