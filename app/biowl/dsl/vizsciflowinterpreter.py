from dsl.interpreter import Interpreter
from dsl.context import Context
from ..vizsciflowlib import Library
from ..vizsciflowsymtab import VizSciFlowSymbolTable
from dsl.wfobj import *
from .provobj import *

registry = {'Workflow':WfWorkflow, 'Module':WfModule, 'Data':WfData, 'Property':WfProperty, 'Run': Run}

class VizSciFlowInterpreter(Interpreter):
    def __init__(self):
        super().__init__(Context(Library(), VizSciFlowSymbolTable))
        
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
                return getattr(obj, function)(*v)
            
            if package in registry:
                args, kwargs = Library.split_args(v)
                return getattr(registry[package], function)(*args, **kwargs)
           
        # call task if exists
        if package is None and function in self.context.library.tasks:
            return self.context.library.run_task(function, v, self.dotaskstmt)

        if not self.context.library.check_function(function, package):
            raise Exception(r"Function '{0}' doesn't exist.".format(function))
            
        return self.context.library.call_func(self.context, package, function, v)