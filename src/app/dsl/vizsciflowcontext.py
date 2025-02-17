import os
import ast
import copy
import shutil
import threading
from dsl.context import Context
from dsl.symtab import SymbolTable

from app.util import Utility
from app.managers.usermgr import usermanager
from app.managers.modulemgr import modulemanager
from app.system.exechelper import func_exec_run, func_exec_bash_stdout, pyvenv_run, func_exec_bash_out_err_exit, py_exec_out_err_exit, pyvenv_run_venv_args, docker_exec_out_exit
from app.dsl.argshelper import get_posix_data_args, get_optional_input_from_args, get_input_from_args
from app.objectmodel.models.rdb import Task
from app.objectmodel.common import LogType, get_python_venvs, strip_quote

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
        if not self.getprop('outdir'):
            self.createoutdir()
        return self.getprop('outdir')
    
    @outdir.setter
    def outdir(self, value):
        with self.lock:
            self.setprop('outdir', value)
    
    @property
    def tempdirs(self):
        if self.getprop('tempdirs') is None:
            self.tempdirs = {}
        return self.getprop('tempdirs')
    
    @tempdirs.setter
    def tempdirs(self, value):
        with self.lock:
            self.setprop('tempdirs', value)

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
        paths = path.split(os.pathsep)
        envpaths = os.environ["PATH"]
        for path in paths:
            if not path in envpaths: # Mainul: may need to check if it ends the envpaths (if it's base of some subdir) or end with :
                envpaths =  path + os.pathsep + envpaths
        if os.environ["PATH"] != envpaths:
            os.environ["PATH"] = envpaths
        return envpaths

    @staticmethod
    def checkenvpath(path):
        paths = path.split('os.pathsep')
        envpaths = os.environ["PATH"]
        for path in paths:
            if not path in envpaths: # Mainul: may need to check if it ends the envpaths (if it's base of some subdir) or end with :
                return False
        return True
    
    def createuniquefile(self, prefix='', extension=''):
        outdir = self.createoutdir()
        fs = Utility.fs_by_prefix_or_guess(outdir)
        return fs.unique_filename(outdir, prefix, extension)
    
    def createoutdir(self, outname = None):
        if not self.getprop('outdir'):
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
        oldcwd = os.getcwd() if 'cwd' in kwargs and kwargs['cwd'] != os.getcwd() else None
        oldenvpath = os.environ["PATH"] if 'env' in kwargs and not VizSciFlowContext.checkenvpath(kwargs['env']) else None
        try:
            if oldcwd: os.chdir(kwargs['cwd'])
            if oldenvpath: VizSciFlowContext.addenvpath(kwargs['env'])
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
    def pyvenv_run_in_env(toolpath, app, *args, **kwargs):
        return VizSciFlowContext.exec_in_env(pyvenv_run, toolpath, app, *args, **kwargs)

    @staticmethod
    def pyvenv_run(toolpath, app, *args):
        return pyvenv_run(toolpath, app, *args)
    
    def pyvenv_run_at_venv(self, toolpath, app, venv, *args):
        venvs = get_python_venvs(self.user_id)
        if not venvs.get(venv):
            raise ValueError(f"{self.user_id}/{venv} virtual environment doesn't exist.")

        args = (os.path.join(venvs[venv], 'bin', 'activate'), *args)
        return pyvenv_run_venv_args(toolpath, app, *args)

    def pyvenv_run_at_venv_in_env(self, toolpath, app, venv, *args, **kwargs):
        venvs = get_python_venvs(self.user_id)
        if not venvs.get(venv):
            raise ValueError(f"{self.user_id}/{venv} virtual environment doesn't exist.")

        args = (os.path.join(venvs[venv], 'bin', 'activate'), *args)
        return VizSciFlowContext.exec_in_env(pyvenv_run_venv_args, toolpath, app, *args, **kwargs)

    @staticmethod
    def normalize(data):
        data = strip_quote(data)
        fs = Utility.fs_by_prefix_or_guess(data)
        return fs.normalize_path(str(data))
    
    @staticmethod
    def denormalize(data):
        fs = Utility.fs_by_prefix_or_guess(data)
        return fs.strip_root(str(data))

    @staticmethod
    def params_to_args(params, *args, **kwargs):
        arguments = {}
        usedIndex = 0
        for param in params:
            if param.name in kwargs:
                arguments[param.name] = kwargs[param.name]
            elif usedIndex < len(args):
                arguments[param.name] = args[usedIndex]
                usedIndex += 1
            elif hasattr(param, 'default'):
                arguments[param.name] = ast.literal_eval(param.default)

        return arguments

    def parse_args(self, funcname, package, *args, **kwargs):
        func = modulemanager.get_module_by_name_package(funcname, package)
        if not func:
            raise ValueError(f"Function {funcname} doesn't exist.")
        return VizSciFlowContext.params_to_args(func.params, *args, **kwargs) if hasattr(func, 'params') else {}
    
    # def get_mypyvenv(self, name = 'None'):
    #     from app import app

    #     venvpath = os.path.join(app.config['VENVS_ROOT_PATH'], "users", self.user_id, name)
    #     if not os.path.isdir(venvpath):
    #         raise ValueError(f"{name} virtual environment for user {self.user_id} doesn't exist.")
    #     return venvpath

    @staticmethod
    def get_pyvenv(name = None):
        from app import app
        if not name:
            name = '.venv'
        venvpath = os.path.join(app.config['VENVS_ROOT_PATH'], name)
        if not os.path.isdir(venvpath):
            raise ValueError(f"{name} virtual environment doesn't exist.")
        return venvpath

    # @staticmethod
    # def get_pyvenv(venv):
    #     return get_python_venvs[venv]

    @staticmethod
    def py_run(app, *args):
        return py_exec_out_err_exit(app, *args)
    
    @staticmethod
    def docker_run(container, app, *args, **kwargs):
        return docker_exec_out_exit(container, app, *args, **kwargs)
