from os import path

from ..models import Service
from dsl.library import LibraryBase, load_module
from dsl.datatype import DataType
from dsl.fileop import FolderItem
from app.runmgr import runnableManager
from app.datamgr import dataManager

from .dsl.provobj import User, Workflow, Module, Data, Property, Run, View, Plugin

registry = {'User':User, 'Workflow':Workflow, 'Module':Module, 'Data':Data, 'Property':Property, 'Run': Run, 'View': View, 'Plugin': Plugin}

class Library(LibraryBase):
    def __init__(self):
        self.tasks = {}
        self.localdir = path.join(path.abspath(path.dirname(__file__)), 'storage')
    
    def add_task(self, name, expr):
        self.tasks[name] = expr
    
    def run_task(self, name, args, dotaskstmt):
        if name in self.tasks:
            return dotaskstmt(self.tasks[name][1:], args)

    def code_run_task(self, name, args, dotaskstmt):
        if name in self.tasks:
            return dotaskstmt(self.tasks[name], args), set()
           
    def get_function(self, name, package = None):
        services = Service.get_service_by_name_package(name, package)
        return services.first().value
    
    @staticmethod
    def is_module(name, package = None):
        return not package and name.lower() == "addmodule"
    
    @staticmethod
    def check_function(name, package = None):
        if not package:
            namelower = name.lower()
            if namelower == "addmodule" or namelower=="user" or namelower=="workflow" or namelower=="run" or namelower=="module" or namelower=="data":
                return True
        if LibraryBase.check_function(name, package):
            return True
        return Service.check_function(name, package)
        
    @staticmethod
    def check_functions(v):
        for f in v:
            if Library.check_function(f.name, f.package):
                return True
        return False
    
    @staticmethod
    def generate_graph(workflow_id, package, function, args):
        
        func = Service.get_first_service_by_name_package(function, package)
        arguments, kwargs = LibraryBase.split_args(args)
        storeArguments = list(arguments)
        for _, v in kwargs.items():
            storeArguments.append(v)
            
        module = runnableManager.add_module(workflow_id, package, function)
        dataManager.StoreModuleArgs(module, func["params"] if func["params"] else [], storeArguments)
                
        result = Library.add_meta_data(func["returns"] if "returns" in func else "")
        
        return result
    
    @staticmethod
    def call_func(context, package, function, args):
        '''
        Call a function from a module.
        :param context: The context for output and error
        :param package: The name of the package. If it's empty, local function is called    
        :param function: Name of the function
        :param args: The arguments for the function
        '''
        task = None
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

            task = runnableManager.create_task(context.runnable, function, package)
            context.task_id = task.id
            task.start()

            if LibraryBase.check_function(function, package):
                result = LibraryBase.call_func(context, package, function, args)
                task.succeeded()
            else:
                arguments, kwargs = LibraryBase.split_args(args)
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
                func = Service.get_first_service_by_name_package(function, package)

                module_obj = load_module(func["module"])
                function = getattr(module_obj, func["internal"])
                
                storeArguments = list(arguments)
                for _, v in kwargs.items():
                    storeArguments.append(v)
                    
                dataManager.StoreArgumentes(context.user_id, task, func["params"] if func["params"] else [], storeArguments)
                result = function(context, *arguments, **kwargs)
                result = Library.add_meta_data(func["returns"] if "returns" in func else "", result, task)
                
                task.succeeded()
                
                if not result:
                    return result
                
                if func["returns"]:
                    if isinstance(func["returns"], list):
                        return result if isinstance(result, tuple) else (result,)
                    else:
                        return result[0]
                    
                result = result if len(result) > 1 else result[0] if result else None
            return result
        except Exception as e:
            if task:
                task.failed(str(e))
            raise
        
    @staticmethod
    def GetDataAndTypeFromFunc(returns, result = None):
        if not result:
            return DataType.Unknown, '', ''
        
        returnstup = returns
        if not isinstance(returnstup, list):
            returnstup = (returnstup,)
            
        resulttup = result
        if not isinstance(resulttup, tuple):
            resulttup = (resulttup,)
        
        dataAndType = []
        mincount = min(len(resulttup), len(returnstup) if returnstup else 0)
        for i in range(0, mincount):
            datatype = DataType.Unknown
            data = ''
            returnsLower = returnstup[i]["type"].lower().split('|')
            if 'file' in returnsLower :
                datatype = datatype | DataType.File
                data = resulttup[i] if isinstance(resulttup[i], FolderItem) else FolderItem(resulttup[i])
            elif 'folder' in returnsLower:
                datatype = datatype | DataType.Folder
                data = resulttup[i] if isinstance(resulttup[i], FolderItem) else FolderItem(resulttup[i])
            elif 'file[]' in returnsLower or 'folder[]' in returnsLower:
                datatype = datatype | DataType.FileList if 'file[]' in returnsLower else datatype | DataType.FolderList
                data = resulttup[i] if isinstance(resulttup[i], list) else [resulttup[i]]
                data = [f if isinstance(f, FolderItem) else FolderItem(f) for f in data]
            else:
                datatype = DataType.Custom
            
            name = returnstup[i]["name"] if "name" in returnstup[i] else ""
            dataAndType.append((datatype, data, name))
        
        for i in range(mincount, len(resulttup)):
            dataAndType.append((DataType.Unknown, resulttup[i]))
        return dataAndType

    @staticmethod
    def add_meta_data(returns, data, task):
        dataAndType = Library.GetDataAndTypeFromFunc(returns, data)
        return dataManager.add_task_data(dataAndType, task)

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

