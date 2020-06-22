from os import path

from ..models import Service
from dsl.library import LibraryBase, load_module
from dsl.datatype import DataType
from dsl.fileop import FolderItem
from app.runmgr import runnableManager
from app.datamgr import dataManager

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
    def check_function(name, package = None):
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
            task = runnableManager.create_task(context.runnable, function)
            context.task_id = task.id
            task.start()

            if LibraryBase.check_function(function, package):
                result = LibraryBase.call_func(context, package, function, args)
                task.succeeded()
            else:
                arguments, kwargs = LibraryBase.split_args(args)
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
        
        if not isinstance(result, tuple):
            result = (result,)
        
        dataAndType = []
        mincount = min(len(result), len(returns) if returns else 0)
        for i in range(0, mincount):
            datatype = DataType.Unknown
            data = ''
            returnsLower = returns[i]["type"].lower().split('|')
            if 'file' in returnsLower :
                datatype = datatype | DataType.File
                data = result[i] if isinstance(result[i], FolderItem) else FolderItem(result[i])
            elif 'folder' in returnsLower:
                datatype = datatype | DataType.Folder
                data = result[i] if isinstance(result[i], FolderItem) else FolderItem(result[i])
            elif 'file[]' in returnsLower or 'folder[]' in returnsLower:
                datatype = datatype | DataType.FileList if 'file[]' in returnsLower else datatype | DataType.FolderList
                data = result[i] if isinstance(result[i], list) else [result[i]]
                data = [f if isinstance(f, FolderItem) else FolderItem(f) for f in data]
            else:
                datatype = DataType.Custom
        
            dataAndType.append((datatype, data))
        
        for i in range(mincount, len(result)):
            dataAndType.append((DataType.Unknown, result[i]))
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

