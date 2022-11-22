from app.dsl.argshelper import get_temp_dir
from dsl.interpreter import Interpreter
from dsl.taskmgr import TaskManager
from app.dsl.vizsciflowlib import Library
from app.dsl.vizsciflowsymtab import VizSciFlowSymbolTable
from dsl.wfobj import *
from app.objectmodel.provmod.provobj import View, Stat, Monitor, Run, Module, Workflow
from app import app
from app.dsl.vizsciflowcontext import VizSciFlowContext

registry = {'View': View, 'Stat': Stat, 'Monitor': Monitor, 'Run': Run, 'Module': Module, 'Workflow': Workflow}

class VizSciFlowInterpreter(Interpreter):
    def __init__(self):
        super().__init__(VizSciFlowContext(Library(), VizSciFlowSymbolTable))
    
    def prepare_view(self, function, result):
        if not hasattr(self.context, 'view'):
            self.context.view = {}
        if function in self.context.view:
            self.context.view[function].append(result)
        else:
            self.context.view[function] = [result]

    def doforpar_stmt(self, vars, expr):
        for k,v in vars.items():
            self.context.add_var(k, v)
        self.dopar_stmt(expr)
        
    def dopar_stmt(self, expr):
        '''
        Execute a for expression.
        :param expr:
        '''
        self.context.copyprops_to_currentthread()
        with app.app_context():
            self.run_multstmt(lambda: self.eval(expr))
        
    def dofor(self, expr):
        '''
        Execute a for expression.
        :param expr:
        '''
        if len(expr) <= 3:
            #sequential for
            super().dofor(expr)
        else:
            #parallel for
            taskManager = TaskManager() 
            for var in self.eval(expr[1]):
                taskManager.submit_func(self.doforpar_stmt, {expr[0]: var}, expr[3])
            taskManager.wait()
                        
    def dofunc(self, expr):
        '''
        Execute func expression.
        :param expr:
        '''
        function = expr[0] if len(expr) < 3 else expr[1]
        package = expr[0][:-1] if len(expr) > 2 else None
        
        params = expr[1] if len(expr) < 3 else expr[2]
        v = self.get_args(params)
                    
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
    