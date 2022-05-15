import os
from app.dsl.argshelper import get_temp_dir
from dsl.interpreter import Interpreter
from dsl.context import Context
from app.dsl.vizsciflowlib import Library
from app.dsl.vizsciflowsymtab import VizSciFlowSymbolTable
from dsl.wfobj import *
from app.objectmodel.provmod.provobj import View, Stat, Monitor, Run, Module, Workflow
from app.util import Utility
from app.system.exechelper import func_exec_run
from app.managers.usermgr import usermanager

registry = {'View': View, 'Stat': Stat, 'Monitor': Monitor, 'Run': Run, 'Module': Module, 'Workflow': Workflow}

class VizSciFlowContext(Context):
    def __init__(self, library, symboltable) -> None:
        super().__init__(library, symboltable)
    
    def getpublicdir(self, typename = "posix"):
        fs = Utility.fs_by_typename(typename)
        return fs.normalize_path(fs.public)
        
    def gettempdir(self, typename = "posix") -> str:
        '''
        The user directory for a fs type is the temp directory.
        '''
        if self.user_id:
            if not typename in self.tempdirs:
                fs = Utility.fs_by_typename(typename)
                if fs.temp:
                    temp = fs.temp
                else:
                    temp = os.path.join('/users', usermanager.get(id = self.user_id).first().username, 'temp')
                self.tempdirs[typename] = fs.make_unique_dir(temp)
            return self.tempdirs[typename]
        else:
            import tempfile
            return tempfile.gettempdir()

    @staticmethod
    def exec_run(app, *args):
        return func_exec_run(app, *args)
    
    @staticmethod
    def bash_run(app, *args):
        return func_exec_run(app, *args)
    
    @staticmethod
    def normalize(data):
        fs = Utility.fs_by_prefix_or_guess(data)
        return fs.normalize_path(str(data))
    
    @staticmethod
    def denormalize(data):
        fs = Utility.fs_by_prefix_or_guess(data)
        return fs.strip_root(str(data))

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