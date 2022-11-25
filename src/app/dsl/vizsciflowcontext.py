import os
import copy
import shutil
import threading
from dsl.context import Context
from dsl.symtab import SymbolTable

from app.util import Utility
from app.managers.usermgr import usermanager
from app.managers.modulemgr import modulemanager
from app.system.exechelper import func_exec_run, func_exec_bash_stdout, pyvenv_run, func_exec_bash_out_err_exit
from app.dsl.argshelper import get_posix_data_args, get_optional_input_from_args, get_input_from_args
from app.objectmodel.models.rdb import Task
from app.objectmodel.common import LogType

class VizSciFlowContext(Context):
    lock = threading.Lock()
    def __init__(self, library, symboltable) -> None:
        self.propstack = {threading.get_ident(): SymbolTable()}
        super().__init__(library, symboltable)

    def getprop(self, propname):
        ident = threading.get_ident()
        if ident in self.propstack and self.propstack[ident].var_exists(propname):
            return self.propstack[ident].get_var(propname)
    def setprop(self, propname, value):
        ident = threading.get_ident()
        if not ident in self.propstack:
            self.propstack[ident] = SymbolTable()
        self.propstack[ident].update_var(propname, value) if self.propstack[ident].var_exists(propname) else self.propstack[ident].add_var(propname, value)
    
    def copyprops_to_currentthread(self):
        ident = threading.get_ident()
        if ident != self.ident:
            self.propstack[ident] = copy.copy(self.propstack[self.ident])
    
    @property
    def task_id(self):
        return self.getprop('task_id')
    
    @task_id.setter
    def task_id(self, value):
        self.setprop('task_id', value)
                
    @property
    def user_id(self):
        return self.getprop('user_id')
    
    @user_id.setter
    def user_id(self, value):
        self.setprop('user_id', value)

    @property
    def task_id(self):
        return self.getprop('task_id')
    
    @task_id.setter
    def task_id(self, value):
        self.setprop('task_id', value)
    
    @property
    def provenance(self):
        return self.getprop('provenance')
    
    @provenance.setter
    def provenance(self, value):
        self.setprop('provenance', value)

    @property
    def outdir(self):
        return self.getprop('outdir')# if self.getprop('outdir') else self.createoutdir()
    
    @outdir.setter
    def outdir(self, value):
        with self.lock:
            self.setprop('outdir', value)
    
    def save_stdout_stderr(self, out, err):
        if out:
            Task.query.get(self.task_id).add_log(out, LogType.STDOUT)
        if err:
            Task.query.get(self.task_id).add_log(err, LogType.STDERR)

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
            os.environ["PATH"] =  path + os.pathsep + envpaths
        return os.environ["PATH"]

    def createuniquefile(self, prefix='', extension=''):
        outdir = self.createoutdir()
        fs = Utility.fs_by_prefix_or_guess(outdir)
        return fs.unique_filename(outdir, prefix, extension)
    
    def createoutdir(self, outname = None):
        if not self.outdir:
            self.outdir = self.makeuniquedir()
        if outname:
            outdir = os.path.join(self.outdir, outname)
            os.makedirs(outdir)
            return outdir
        return self.outdir

    def makeuniquedir(self, parent = None):
        if not parent:
            parent = self.gettempdir()
        fs = Utility.fs_by_prefix_or_guess(parent)
        return fs.make_unique_dir(parent)

    def gettoolsdir(self, name=None, package=None):
        from app import app
        
        func = modulemanager.get_module_by_name_package(name, package)
        if not func:
            raise ValueError('Tool {0} does not exist.'.format(name))
        tooldir = os.path.join(app.config['MODULE_DIR'], (os.path.sep).join(func.module.split('.')[2:-1])) # remove plugins/modules from front and adapter from back
        if not os.path.exists(tooldir):
            raise ValueError(f"Path for tool {package}.{name} does not exist")
        return tooldir

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

            return f(app, *args)
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
    def bash_run_out_err_exit(app, *args, **kwargs):
        return VizSciFlowContext.exec_in_env(func_exec_bash_out_err_exit, app, *args, **kwargs)
    
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

    def parse_args(self, funcname, package, *args, **kwargs):
        func = modulemanager.get_module_by_name_package(funcname, package)
        if not func:
            raise ValueError(f"Function {funcname} doesn't exist.")

        arguments = {}
        usedIndex = 0
        if hasattr(func, 'params'):
            for param in func.params:
                if param.name in kwargs:
                    arguments[param.name] = kwargs[param.name]
                elif usedIndex < len(args):
                    arguments[param.name] = args[usedIndex]
                    usedIndex += 1
                elif hasattr(param, 'default'):
                    arguments[param.name] = param.default

        return arguments

    def workflow_id(*args, **kwargs):
        id = kwargs.pop('id', None)
        if not id:
            id = args[0]
        if not id:
            raise ValueError("No valid workflow.")
        return id