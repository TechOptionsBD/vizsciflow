import os
from app.dsl.argshelper import get_temp_dir
from dsl.interpreter import Interpreter
from dsl.context import Context
from app.dsl.vizsciflowlib import Library
from app.dsl.vizsciflowsymtab import VizSciFlowSymbolTable
from dsl.wfobj import *
from app.objectmodel.provmod.provobj import View, Stat, Monitor, Run, Module, Workflow
from app.util import Utility
from app.system.exechelper import func_exec_run, func_exec_bash_stdout, pyvenv_run
from app.managers.usermgr import usermanager
from app.managers.modulemgr import modulemanager
from app.dsl.argshelper import get_posix_data_args, get_optional_input_from_args, get_input_from_args
import shutil

registry = {'View': View, 'Stat': Stat, 'Monitor': Monitor, 'Run': Run, 'Module': Module, 'Workflow': Workflow}


class VizSciFlowContext(Context):
    def __init__(self, library, symboltable) -> None:
        super().__init__(library, symboltable)

    @staticmethod
    def moveto(src, dest, ignores=[]):
        if not dest.endswith(os.path.sep):
            shutil.move(src, dest)
        else:
            for file in os.listdir(src):
                if file not in ignores:
                    shutil.move(os.path.join(src, file), dest)

    @staticmethod
    def copyto(src, dest, ignores=[]):
        srcname = os.path.basename(src)
        destdir = os.path.join(dest, srcname)
        if os.path.exists(destdir):
            shutil.rmtree(destdir)
        os.makedirs(destdir)
        ignore_patterns = None
        if ignores:
            ignore_patterns = ','.join(ignores)
        return shutil.copytree(src, destdir, dirs_exist_ok=True, ignore=shutil.ignore_patterns(ignore_patterns))

    def getdataarg(self, paramindex, argname, *args, **kwargs):
        paramindex, data, fs = get_posix_data_args(paramindex, argname, self, *args, **kwargs)
        if not fs.exists(data):
            raise ValueError("Input file/folder {0} doesn't exist.".format(fs.strip_root(str(data))))
        return paramindex, data, fs

    def getarg(self, paramindex, argname, *args, **kwargs):
        paramindex, data = get_input_from_args(paramindex, argname, self, *args, **kwargs)
        return paramindex, data
    
    def getoptionalarg(self, paramindex, argname, *args, **kwargs):
        paramindex, data = get_optional_input_from_args(paramindex, argname, *args, **kwargs)
        return paramindex, data

    @staticmethod
    def addenvpath(path):
        envpaths = os.environ["PATH"]
        if not path in envpaths: # Mainul: may need to check if it ends the envpaths (if it's base of some subdir) or end with :
            os.environ["PATH"] = envpaths + os.pathsep + path
        return os.environ["PATH"]

    def createoutdir(self, outname = None):
        outdir = self.makeuniquedir()
        if outname:
            outdir = os.path.join(outdir, outname)
            os.makedirs(outdir)
        return outdir

    def makeuniquedir(self, parent = None):
        if not parent:
            parent = self.gettempdir()
        fs = Utility.fs_by_prefix_or_guess(parent)
        return fs.make_unique_dir(parent)

    def gettoolsdir(self, name=None, package=None):
        from app import app
        if name == 'txl':
            return '/home/vizsciflow/bin' #TODO: we need to make it flexible
        
        toolsdir = os.path.join(app.config['MODULE_DIR'], 'users', usermanager.get(id = self.user_id).first().username)
        if not name:
            return toolsdir
        func = modulemanager.get_module_by_name_package(name, package)
        if not func:
            return ''
            #raise ValueError('Tool {0} does not exist.'.format(name))
        return os.path.join(app.config['MODULE_DIR'], (os.path.sep).join(func.module.split('.')[2:-1])) # remove plugins/modules from front and adapter from back

    # def getmyprovdir(self):
    #     from app import app
    #     return os.path.join(app.config['PROVENANCE_DIR'], 'users', usermanager.get(id = self.user_id).first().username)

    def getpublicdir(self, typename = "posix"):
        fs = Utility.fs_by_typename(typename)
        return fs.normalize_path(fs.public)
    
    def getnormdir(self, filepath):
        return os.path.dirname(os.path.abspath(filepath))
        
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
    def exec_in_env(f, app, *args, **kwargs):
        oldcwd = os.getcwd() if 'cwd' in kwargs else None
        oldenvpath = os.environ["PATH"] if 'env' in kwargs else None
        try:
            if 'cwd' in kwargs:
                os.chdir(kwargs['cwd'])
            if 'env' in kwargs:
                VizSciFlowContext.addenvpath(kwargs['env'])

            return func_exec_run(app, *args)
        finally:
            if oldcwd: os.chdir(oldcwd)
            if oldenvpath: os.environ["PATH"] = oldenvpath

    @staticmethod
    def exec_run(app, *args, **kwargs):
        return VizSciFlowContext.exec_in_env(func_exec_run, app, *args, **kwargs)

    @staticmethod
    def bash_run(app, *args, **kwargs):
        return VizSciFlowContext.exec_in_env(func_exec_bash_stdout, app, *args, **kwargs)
    
    @staticmethod
    def pyvenv_run(toolpath, app, *args):
        return pyvenv_run(toolpath, app, *args)
    
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