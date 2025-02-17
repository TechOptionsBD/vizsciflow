import os
import sys
import logging
import requests
import jsonpickle
from timeit import time
from collections import namedtuple
from urllib.parse import urljoin, urlencode

from dsl.library import LibraryBase, load_module
from dsl.datatype import DataType
from dsl.filemgr import FileManager

from app.dsl.vizsciflowcontext import VizSciFlowContext
from app.managers.runmgr import runnablemanager
from app.managers.datamgr import datamanager
from app.managers.modulemgr import modulemanager
from app.objectmodel.common import isiterable, known_types
from app.managers.workflowmgr import workflowmanager
from app.objectmodel.common import dict2obj, LogType

from app.objectmodel.provmod.provobj import *
registry = {'User':User, 'Workflow':Workflow, 'Module':Module, 'Data':Data, 'Property':Property, 'Run': Run, 'View': View, 'Plugin': Plugin, 'Stat': Stat, 'Monitor': Monitor}

class Library(LibraryBase):
    def __init__(self):
        super(Library, self).__init__(FileManager())
        self.localdir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'storage')
    
    def add_task(self, name, expr):
        self.tasks[name] = expr
    
    def run_task(self, name, args, dotaskstmt):
        if name in self.tasks:
            return dotaskstmt(self.tasks[name][1:], args)

    def code_run_task(self, name, args, dotaskstmt):
        if name in self.tasks:
            return dotaskstmt(self.tasks[name], args), set()
           
    def get_function(self, name, package = None):
        service = modulemanager.get_module_by_name_package(name, package)
        return service.value
    
    @staticmethod
    def is_module(name, package = None):
        return not package and name.lower() == "addmodule"
    
    def check_function(self, name, package = None):
        if not package:
            namelower = name.lower()
            if namelower == "addmodule" or namelower=="user" or namelower=="workflow" or namelower=="run" or namelower=="module" or namelower=="data":
                return True
        return modulemanager.check_function(name, package)
        
    @staticmethod
    def check_functions(v):
        for f in v:
            if Library.check_function(f.name, f.package):
                return True
        return False
    
    @staticmethod
    def generate_graph(context, workflow_id, package, function, args):
        
        func = modulemanager.get_first_service_by_name_package_json(function, package).value
        arguments, kwargs = LibraryBase.split_args(args)
        storeArguments = list(arguments)
        for _, v in kwargs.items():
            storeArguments.append(v)
            
        module = runnablemanager.add_module(workflow_id, package, function)
        datamanager.StoreModuleArgs(module, func["params"] if func["params"] else [], storeArguments)
                
        return Library.add_meta_data(context, func["returns"] if "returns" in func else "")

    @staticmethod
    def needs_normalization(paramType):
        if not paramType:
            return False
        paramType = paramType.lower()
        return paramType == 'file' or paramType == 'folder' or paramType == 'file|folder'  or paramType == 'folder|file' or paramType == 'file[]' or paramType == 'filder[]' or paramType == 'file[]|folder[]' or paramType == 'file[]|folder[]'

    @staticmethod
    def normalize(context, paramType, arg):
        if not arg: # for empty string and None, return empty string
            return ''
        paramType = paramType.lower()
        if paramType == 'file' or paramType == 'folder' or paramType == 'file|folder'  or paramType == 'folder|file':
            return context.normalize(str(arg))
        elif paramType == 'file[]' or paramType == 'folder[]' or paramType == 'file[]|folder[]' or paramType == 'file[]|folder[]':
            if isiterable(arg):
                return [context.normalize(str(a)) for a in arg]
            else:
                return [context.normalize(str(arg))]
    
    @staticmethod
    def denormalize(context, paramType, arg):
        paramType = paramType.lower()
        if paramType == 'file' or paramType == 'folder' or paramType == 'file|folder'  or paramType == 'folder|file':
            return context.denormalize(str(arg))
        elif paramType == 'file[]' or paramType == 'folder[]' or paramType == 'file[]|folder[]' or paramType == 'file[]|folder[]':
            if isiterable(arg):
                return [context.denormalize(str(a)) for a in arg]
            else:
                return [context.denormalize(str(arg))]
    
    @staticmethod
    def normalize_args(context, params, *arguments, **kwargs):
        usedIndex = 0
        arguments = list(arguments)
        kwargs = dict(kwargs)
        for param in params:
            type = param.type if hasattr(param, 'type') else 'str'
            if not param.name or not Library.needs_normalization(type): continue

            if param.name in kwargs:
                kwargs[param.name] = Library.normalize(context, type, kwargs[param.name])
            elif usedIndex < len(arguments):
                arguments[usedIndex] = Library.normalize(context, type, arguments[usedIndex])
                usedIndex += 1
        return arguments, kwargs

    def call_func(self, context, package, function, args):
        '''
        Call a function from a module.
        :param context: The context for output and error
        :param package: The name of the package. If it's empty, local function is called    
        :param function: Name of the function
        :param args: The arguments for the function
        '''
        from app import app
        sys.path.append(os.path.dirname(app.instance_path))

        task = None
        ts = time.perf_counter()
        try:
            if not package and function.lower() == "addmodule":
                f = args[0]
                pkgfunc = f.split(".")
                if pkgfunc == 1:
                    function = pkgfunc
                else:
                    package = pkgfunc[0]
                    function = pkgfunc[1]
                args = args[1:]

            task = runnablemanager.invoke_module(context.runnable, function, package)
            context.task_id = task.id
            task.start()

            arguments, kwargs = LibraryBase.split_args(args)
            if context.provenance:
                if not package and function in registry:
                    provcls = None
                    if function.lower() == "run":
                        provcls = Run(*arguments, **kwargs)
                    elif function.lower() == "user":
                        provcls = User(*arguments, **kwargs)
                    elif function.lower() == "workflow":
                        provcls = Workflow(*arguments, **kwargs)
                    elif function.lower() == "module":
                        provcls = Module(*arguments, **kwargs)
                    elif function.lower() == "data":
                        provcls = Data(*arguments, **kwargs)
                    #provcls = getattr(".dsl.provobj", registry[function])
                    #return provcls(*arguments, **kwargs)
                    return provcls
            
            func = modulemanager.get_module_by_name_package_json(function, package)
            if not func.active:
                if func.user_id == context.user_id:
                    logging.info(f"You are running unpublish function {pkgfuncname}")
                else:
                    pkgfuncname = f"{func.package}{'.' if func.package else ''}{func.name}"
                    raise ValueError(f"{pkgfuncname} is not published")
            
            remote = func.module.startswith("http://") or func.module.startswith("https://")
            if remote:
                remotefunc = requests.get(urljoin(func.module, f'api/service?name={func.name}&package={func.package}')).json()
                params = []
                if 'params' in remotefunc:
                    params = [namedtuple("Param", v.keys())(*v.values()) for v in remotefunc['params']]
                returns = []
                if 'returns' in remotefunc:
                    returns = [namedtuple("Return", v.keys())(*v.values()) for v in remotefunc['returns']]
            else:
                if func.package == 'system' and func.name.lower() == 'workflow':
                    id = kwargs.pop('id', None)
                    if not id:
                        id = arguments.pop()
                    workflow = workflowmanager.first(id=id)
                    params = [dict2obj(param.value) for param in workflow.params if workflow.params]
                    returns = [dict2obj(ret.value) for ret in workflow.returns if workflow.returns]
                    kwargs = VizSciFlowContext.params_to_args(params, *arguments, **kwargs) #id must not exist here
                    arguments = [id]
                else:
                    params = list(func.params) if hasattr(func, 'params') else []
                    returns = func.returns if hasattr(func, 'returns') else None

            Library.StoreArguments(context, task, params, arguments, **kwargs)

            if remote:
                qs =  '/api/runservice' + '?' + urlencode({'funcname': func.name, 'funcpackage': func.package})
                arguments, kwargs = Library.normalize_args(context, params, *arguments, **kwargs)
                argstoken = '&'.join(arguments)
                if argstoken:
                    qs += '&' + argstoken
                kwtoken = urlencode(kwargs)
                if kwtoken:
                    qs = qs + '&' + kwtoken
                result = requests.get(urljoin(func.module, qs))
                if result.status_code == 500:
                    raise ValueError(result.text)
                result = jsonpickle.decode(result.text)
            else:
                arguments, kwargs = Library.normalize_args(context, params, *arguments, **kwargs)
                module_obj = load_module(func.module)
                funcdef = getattr(module_obj, func.internal)
                try:
                    oldcwd = os.getcwd()
                    os.chdir(os.path.dirname(module_obj.__file__))
                    result = funcdef(context, *arguments, **kwargs)
                finally:
                    os.chdir(oldcwd)

            result = Library.add_meta_data(context, result, returns, task)

            task.succeeded()
            return result
        except Exception as e:
            if task:
                task.failed(str(e))                
            logging.error("Error calling the service {0}:{1}".format(function, str(e)))
            raise
        finally:
            if task:
                task.duration = time.perf_counter() - ts

    @staticmethod
    def StoreArguments(context, task, params, arguments, **kwargs):
        storeArguments = list(arguments)
        for _, v in kwargs.items():
            storeArguments.append(v)
            
        datamanager.StoreArgumentes(context.user_id, task, params, storeArguments)

    @staticmethod
    def check_file(result, task):
        fs = Utility.fs_by_prefix_or_guess(str(result))
        if not fs or not fs.isfile(str(result)):
            task.add_log(log="Tool definition indicates file, tool generates no file.", logtype=LogType.WARNING)

    @staticmethod
    def check_folder(result, task):
        fs = Utility.fs_by_prefix_or_guess(str(result))
        if not fs or not fs.isdir(str(result)):
            task.add_log(log="Tool definition indicates folder, but tool generates no folder.", logtype=LogType.WARNING)

    @staticmethod
    def get_data_and_type_from_result(context, result, ret, task = None):
        '''
        Prepare the return value for the storage into the db.
        '''
        name = ret.name if hasattr(ret, 'name') else ''
        datatype = ret.type.lower().split('|')[0] if hasattr(ret, 'type') else ''
        if 'file[]' in datatype or 'folder[]' in datatype:
            t = DataType.FileList if 'file[]' in datatype else DataType.FolderList
            result = Library.denormalize(context, datatype, result)
            fsitems = list(result) if isiterable(result) else [result]
            if task:
                if 'file[]' in datatype:
                    for file in fsitems:
                        Library.check_file(file, task)

                if 'folder[]' in datatype:
                    for folder in fsitems:
                        Library.check_folder(folder, task)

            return t, fsitems, name, result if isiterable(result) else [result]
        elif 'file' in datatype or 'folder' in datatype:
            if task:
                if 'file' in datatype:
                    Library.check_file(result, task)
                if 'folder' in datatype:
                    Library.check_folder(result, task)

            result = Library.denormalize(context, datatype, result)
            return DataType.File if 'file' in datatype else DataType.Folder, result, name, result
        elif 'any' in datatype:
            return DataType.Unknown, result, name, result
        elif datatype in known_types.keys():
            return DataType.Value, result, name, result
        else:
            return DataType.Unknown, result, name, result

    @staticmethod
    def add_meta_data(context, result, returns, task):
        if not result:
            if returns:
                task.add_log(log="Tools didn't return any value.", logtype=LogType.WARNING)
            return None

        if not returns:
            task.add_log(log="Tools returns value though tool definition doesn't specify return value.", logtype=LogType.WARNING)
            return result
        
        if not isiterable(returns) and isinstance(result, tuple):
            task.add_log(log="Tool returns tuple but tool definition indicates single value.", logtype=LogType.WARNING)
            output = Library.get_data_and_type_from_result(context, result[0], returns, task)
            datamanager.add_task_data(output, task)
            return output[3]

        if isiterable(returns) and not isinstance(result, tuple):
            task.add_log(log="Tool returns single value but tool definition indicates tuple.", logtype=LogType.WARNING)
            output = Library.get_data_and_type_from_result(context, result, returns[0], task)
            datamanager.add_task_data(output, task)
            return output[3]

        task.add_log(log=f"Tool returns {len(result)} values but tool definition indicates {len(returns)} values. Keeping the minimum values.", logtype=LogType.WARNING)

        output = []
        mincount = min(len(result), len(returns))
        for i in range(0, mincount):
            dataAndType = Library.get_data_and_type_from_result(context, result[i], returns[i], task)
            datamanager.add_task_data(dataAndType, task)
            output.append(dataAndType[3])
        
        return tuple(output)

    @staticmethod
    def add_runnable_returns(context, result, returns):
        if not result:
            return None

        if not returns:
            return result
        
        if not isiterable(returns) and isinstance(result, tuple):
            output = Library.get_data_and_type_from_result(context, result[0], returns)
            runnablemanager.add_return(context.runnable, output)
            return output[3]

        if isiterable(returns) and not isinstance(result, tuple):
            output = Library.get_data_and_type_from_result(context, result, returns[0])
            runnablemanager.add_return(context.runnable, output)
            return output[3]

        output = []
        mincount = min(len(result), len(returns))
        for i in range(0, mincount):
            dataAndType = Library.get_data_and_type_from_result(context, result[i], returns[i])
            runnablemanager.add_return(context.runnable, output)
            output.append(dataAndType[3])
        
        return tuple(output)

    def code_func(self, context, package, function, arguments):
        '''
        Call a function from a module.
        :param context: The context for output and error
        :param package: The name of the package. If it's empty, local function is called    
        :param function: Name of the function
        :param arguments: The arguments for the function
        '''
        imports = set()
        args = ','.join(arguments)
        code = ''
        if not package or package == "None":
            if function.lower() == "print":
                code = "print({0})".format(args)
            elif function.lower() == "range":
                code = "range({0})".format(args)
            elif function.lower() == "read":
                imports.add("from fileop import IOHelper")
                code = "IOHelper.read({0})".format(args)
            elif function.lower() == "write":
                imports.add("from fileop import IOHelper")
                code = "IOHelper.write({0})".format(args)
            elif function.lower() == "getfiles":
                imports.add("from fileop import IOHelper")
                code = "IOHelper.getfiles({0})".format(args)
            elif function.lower() == "getfolders":
                imports.add("from fileop import IOHelper")
                code = "IOHelper.getfolders({0})".format(args)
            elif function.lower() == "remove":
                imports.add("from fileop import IOHelper")
                code = "IOHelper.remove({0})".format(args)
            elif function.lower() == "createfolder":
                imports.add("from fileop import IOHelper")
                code = "IOHelper.makedirs({0})".format(args)
            elif function.lower() == "getcwd":
                imports.add("import os")
                code = "os.getcwd()"
            elif function.lower() == "len":
                code = "len({0})".format(arguments[0])
            elif function.lower() == "exec":
                imports.add("import subprocess")
                code =  "func_exec_run({0}, {1})".format(arguments[0], arguments[1])

        if code:
            return code, imports
        
        imports.add("from importlib import import_module")
        func = self.get_function(function, package)
        code = "module_obj = load_module({0})\n".format(func[0].module)
        code += "function = getattr(module_obj, {0})\n".format(func[0].internal)
        if context.dci and context.dci[-1] and func.runmode == 'distibuted':
            args = [context.dci[-1]] + args
        code += "function({0})".format(args)
        return code, imports
            
    def __repr__(self):
        return "Library: " + repr(self.funcs)
    def __getitem__(self, key):
        return self.funcs[key]
    def __setitem__(self, key, val):
        self.funcs[key] = val
    def __delitem__(self, key):
        del self.funcs[key]
    def __contains__(self, key):
        return key in self.funcs
    def __iter__(self):
        return iter(self.funcs.keys())

    def __str__(self):
        funcs = self.funcs_flat();
        #funcs = [num for elem in funcs for num in elem]
            
        if len(funcs) > 0:
            mod_name = "Module name"
            mod_len = max(max(len(i.module) if i.module is not None else 0 for i in funcs), len(mod_name))
         
            internal_name = "Internal Name"
            internal_len = max(max(len(i.internal) for i in funcs), len(internal_name))
            
            func_name = "Function Name"
            func_len = max(max(len(i.name) for i in funcs), len(func_name))
           
            param_names = "Parameters"
            param_len = len(param_names)
            l = 0
            for a in funcs:
                for v in a.params:
                    l += len(v)
                param_len = max(param_len, l)
            
            # print table header for vars
            display = "\n\n{0:3s} | {1:^{2}s} | {3:^{4}s} | {5:^{6}s} | {7:^{8}s}".format(" No", mod_name, mod_len, internal_name, internal_len, func_name, func_len, param_names, param_len)
            display += ("\n-------------------" + "-" * (mod_len + internal_len + func_len + param_len))
            # print symbol table
            
            i = 1
            for v in funcs:
                module = v.module if v.module is not None else "None"
                parameters = ""
                for p in v.params:
                    if parameters == "":
                        parameters = "{0}".format(p)
                    else:
                        parameters += ", {0}".format(p)
                display += "\n{0:3d} | {1:^{2}s} | {3:^{4}s} | {5:^{6}s} | {7:^{8}s}".format(i, module, mod_len, v.internal, internal_len, v.name, func_len, parameters, param_len)
                
                i += 1
                
        return display

