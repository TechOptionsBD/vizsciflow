from dsl.interpreter import Interpreter
from dsl.context import Context
from ..vizsciflowlib import Library
from ..vizsciflowsymtab import VizSciFlowSymbolTable
from dsl.wfobj import *
from app.objectmodel.provmod.provobj import View, Stat, Monitor, Run, Module, Workflow

registry = {'View': View, 'Stat': Stat, 'Monitor': Monitor, 'Run': Run, 'Module': Module, 'Workflow': Workflow}

class VizSciFlowInterpreter(Interpreter):
    def __init__(self):
        super().__init__(Context(Library(), VizSciFlowSymbolTable))
    
    def prepare_view(self, function, result):
        if not hasattr(self.context, 'view'):
            self.context.view = {}
        if function in self.context.view:
            self.context.view[function].append(result)
        else:
            self.context.view[function] = [result]
                
    def dofunc(self, expr):
        '''
        Execute func expression.
        :param expr:
        '''
        function = expr[0] if len(expr) < 3 else expr[1]
        package = expr[0][:-1] if len(expr) > 2 else None
        
        params = expr[1] if len(expr) < 3 else expr[2]
        v = self.get_args(params)
        
        if package:
            if self.context.var_exists(package):
                obj = self.context.get_var(package)
                args, kwargs = Library.split_args(v)
                return getattr(obj, function.lower())(*args, **kwargs)
            
            if self.context.provenance:
                if package in registry:
                    args, kwargs = Library.split_args(v)
                    result = getattr(registry[package], function.lower())(*args, **kwargs)
                    if package == "View" or package == "Stat"  or package == "Monitor":
                        self.prepare_view(function.lower(), result)
                    return result
           
        # call task if exists
        if package is None and function in self.context.library.tasks:
            return self.context.library.run_task(function, v, self.dotaskstmt)

        if not self.context.library.check_function(function, package):
            raise Exception(r"Function '{0}' doesn't exist.".format(function))
            
        return self.context.library.call_func(self.context, package, function, v)