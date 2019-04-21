from importlib import import_module
import json
from os import path, getcwd
import os
import pathlib

from ...util import Utility
from ..exechelper import func_exec_run
from flask_login import current_user
from ...models import Task, Status, DataType, AccessRights, DataSourceAllocation

# import_module can't load the following modules in the NGINX server
# while running in 'immediate' mode. The early imports here are needed.
# This needs to be fixed, otherwise dynamic loading will not work.
try:
    import app.biowl.libraries.galaxy.adapter
except:
    pass

try:
    import app.biowl.libraries.seqtk.adapter
    import app.biowl.libraries.bowtie2.adapter
    import app.biowl.libraries.bwa.adapter
    import app.biowl.libraries.pysam.adapter
    import app.biowl.libraries.fastqc.adapter    
    import app.biowl.libraries.apachebeam.adapter
    import app.biowl.libraries.flash.adapter
    import app.biowl.libraries.hadoop.adapter
    import app.biowl.libraries.pear.adapter
    import app.biowl.libraries.seqtk.adapter
    import app.biowl.libraries.usearch.adapter
    import app.biowl.libraries.vsearch.adapter
except:
    pass

def load_module(modulename):
    '''
    Load a module dynamically from a string module name.
    It was first implemented with __import__, but later
    replaced by importlib.import_module.
    :param modulename:
    '''
    #if modulename not in sys.modules:
    #name = "package." + modulename
    #return __import__(modulename, fromlist=[''])
    return import_module(modulename)

class Function():
    def __init__(self, name, internal, package = None, module = None, params = [], example = None, desc = None, runmode = None, level = 0, group = None, user = None, access = 0, example2 = None, returns = None):
        self.name = name
        self.internal = internal
        self.package = package
        self.module = module
        self.params = params
        self.example = example
        self.desc = desc
        self.runmode = runmode
        self.level = level
        self.group = group
        self.user = user
        self.access = access
        self.example2 = example2
        self.returns = returns
        
class Library():
    def __init__(self, funcs = {}):
        self.funcs = funcs
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
            
    @staticmethod
    def load(library_def_file):
        library = Library()
        
#         datafiles = []
#         for r, d, f in os.walk(library_def_file):
#             datafiles.extend([os.path.join(r, file) for file in f if file.endswith(".json")])
            
        all_funcs = {}
        for f in os.listdir(library_def_file):
            fsitem = os.path.join(library_def_file, f)
            if os.path.isdir(fsitem) and f == 'users':
                for fuser in os.listdir(fsitem):
                    Library.merge_funcs(all_funcs, Library.load_funcs_recursive(os.path.join(fsitem, fuser), fuser))
            else:
                Library.merge_funcs(all_funcs, Library.load_funcs_recursive(fsitem, None))

        library.funcs = all_funcs
        return library
    
    
    @staticmethod
    def merge_funcs(all_funcs, funcs):
        for k,v in funcs.items():
            if k in all_funcs:
                all_funcs[k].extend(v)
            else:
                all_funcs[k] = v if isinstance(v, list) else [v]
        
    @staticmethod
    def load_funcs_recursive(library_def_file, user):
        if os.path.isfile(library_def_file):
            return Library.load_funcs(library_def_file, user) if pathlib.Path(library_def_file).suffix == ".json" else {}

        all_funcs = {}
        for f in os.listdir(library_def_file):
            Library.merge_funcs(all_funcs, Library.load_funcs_recursive(os.path.join(library_def_file, f), user))
        return all_funcs
       
    @staticmethod
    def load_funcs(library_def_file, user):
        funcs = {}
        try:
            if not os.path.isfile(library_def_file) or not library_def_file.endswith(".json"):
                return funcs
            
            with open(library_def_file, 'r') as json_data:
                d = json.load(json_data)
                libraries = d["functions"]
                libraries = sorted(libraries, key = lambda k : k['package'].lower() if k['package'] else '')
                for f in libraries:
                    name = f["name"] if f.get("name") else f["internal"]
                    internal = f["internal"] if f.get("internal") else f["name"]
                    module = f["module"] if f.get("module") else None
                    package = f["package"] if f.get("package") else ""
                    example = f["example"] if f.get("example") else ""
                    example2 = f["example2"] if f.get("example2") else ""
                    desc = f["desc"] if f.get("desc") else ""
                    runmode = f["runmode"] if f.get("runmode") else ""
                    level = int(f["level"]) if f.get("level") else 0
                    group = f["group"] if f.get("group") else ""
                    access = int(f["access"]) if f.get("access") else 0
                    returns = f["returns"] if f.get("returns") else ""
                    params = []
                    if f.get("params"):
                        for param in f["params"]:
                            params.append(param)
                    func = Function(name, internal, package, module, params, example, desc, runmode, level, group, user, access, example2, returns)
                    if name.lower() in funcs:
                        funcs[name.lower()].extend([func])
                    else:
                        funcs[name.lower()] = [func]
        finally:
            return funcs
    
    def func_to_internal_name(self, funcname):
        for f in self.funcs:
            if f.get("name") and self.iequal(f["name"], funcname):
                return f["internal"]
            
    def get_function(self, name, package = None):
        if package:
            for func in self.funcs[name.lower()]:
                if func.package == package:
                    return [func]
        else:
            return self.funcs[name.lower()]
    
    def check_function(self, name, package = None):
        if package:
            for func in self.funcs[name.lower()]:
                if func.package == package:
                    return True
        else:
            return name.lower() in self.funcs
        
    def funcs_flat(self):
        funcs = []
        for v in self.funcs.values():
            funcs.extend(v)
        return funcs
        
    @staticmethod
    def split_args(arguments):
        args = []
        kwargs = {}
        for arg in arguments:
            if isinstance(arg, tuple):
                kwargs[arg[0]] = arg[1]
            else:
                args.append(arg)
        return args, kwargs
    
    @staticmethod
    def GetDataTypeFromFunc(returns):
        if returns:
            returnsLower = returns.lower()
            if returnsLower == 'File':
                return DataType.File
            elif returnsLower == 'Folder':
                return DataType.Folder
            elif returnsLower == 'File[]':
                return DataType.FileList
        return DataType.Custom

    def call_func(self, context, package, function, args):
        '''
        Call a function from a module.
        :param context: The context for output and error
        :param package: The name of the package. If it's empty, local function is called    
        :param function: Name of the function
        :param args: The arguments for the function
        '''
        task = None
        try:
            arguments, kwargs = Library.split_args(args)
            func = self.get_function(function, package)
    
            task = Task.create_task(context.runnable, func[0].name)
            task.start()
        
            if not package or package == "None":
                if function.lower() == "print":
                    result = context.write(*arguments)
                elif function.lower() == "range":
                    result = range(*arguments)
                elif function.lower() == "read":
                    if not arguments:
                        raise ValueError("Read must have one argument.")
                    
                    DataSourceAllocation.check_access_rights(context.user_id, arguments[0], AccessRights.Read)
                    fs = Utility.fs_by_prefix_or_default(arguments[0])
                    result = fs.read(arguments[0])
                elif function.lower() == "write":
                    if len(arguments) < 2:
                        raise ValueError("Write must have two arguments.")
                    DataSourceAllocation.check_access_rights(context.user_id, arguments[0], AccessRights.Write)
                    fs = Utility.fs_by_prefix_or_default(arguments[0])
                    return fs.write(arguments[0], arguments[1])
                elif function.lower() == "getfiles":
                    DataSourceAllocation.check_access_rights(context.user_id, arguments[0], AccessRights.Read)
                    fs = Utility.fs_by_prefix_or_default(arguments[0])
                    return fs.get_files(arguments[0])
                elif function.lower() == "getfolders":
                    DataSourceAllocation.check_access_rights(context.user_id, arguments[0], AccessRights.Read)
                    fs = Utility.fs_by_prefix_or_default(arguments[0])
                    return fs.get_folders(arguments[0])
                elif function.lower() == "createfolder":
                    DataSourceAllocation.check_access_rights(context.user_id, arguments[0], AccessRights.Write)
                    fs = Utility.fs_by_prefix_or_default(arguments[0])
                    return fs.makedirs(arguments[0])
                elif function.lower() == "remove":
                    DataSourceAllocation.check_access_rights(context.user_id, arguments[0], AccessRights.Write)
                    fs = Utility.fs_by_prefix_or_default(arguments[0])
                    return fs.remove(arguments[0])
                elif function.lower() == "makedirs":
                    DataSourceAllocation.check_access_rights(context.user_id, arguments[0], AccessRights.Write)
                    fs = Utility.fs_by_prefix_or_default(arguments[0])
                    return fs.makedirs(arguments[0])
                elif function.lower() == "getcwd":
                    return getcwd()
                elif function.lower() == "isfile":
                    fs = Utility.fs_by_prefix_or_default(arguments[0])
                    return fs.isfile(arguments[0])
                elif function.lower() == "dirname":
                    return os.path.dirname(arguments[0])
                elif function.lower() == "basename":
                    return os.path.basename(arguments[0])
                elif function.lower() == "getdatatype":
                    DataSourceAllocation.check_access_rights(context.user_id, arguments[0], AccessRights.Write)
                    fs = Utility.fs_by_prefix_or_default(arguments[0])
                    extension = pathlib.Path(arguments[0]).suffix
                    return extension[1:] if extension else extension
                elif function.lower() == "len":
                    return len(arguments[0])
                elif function.lower() == "exec":
                    DataSourceAllocation.check_access_rights(context.user_id, arguments[0], AccessRights.Read)
                    return func_exec_run(arguments[0], *arguments[1:])            
                elif function.lower() == "copyfile":
                    DataSourceAllocation.check_access_rights(context.user_id, arguments[1], AccessRights.Write)
                    fs = Utility.fs_by_prefix_or_default(arguments[0])
                    return fs.copy(arguments[0], arguments[1])                        
                elif function.lower() == "deletefile":
                    DataSourceAllocation.check_access_rights(context.user_id, arguments[0], AccessRights.Write)
                    fs = Utility.fs_by_prefix_or_default(arguments[0])
                    return fs.remove(arguments[0])
            #    return func_exec(arguments[0], *arguments[1:])
#             else:
#                 raise ValueError("{0} function not implemented".format(function))
    #             possibles = globals().copy()
    #             possibles.update(locals())
    #             function = possibles.get(function)
    #             return function(*arguments)
        
#             if not 'history_id' in kwargs and context.var_exists('history_id'):
# #                     create_history_function = getattr(module_obj, "create_history") # history not running, create one
# #                     history_id = create_history_function(context.get_activedci())
# #                     context.add_var('history_id', history_id)
#                 fullargspec = inspect.getfullargspec(function)
#                 if fullargspec.varkw:
#                     kwargs['history_id'] = context.get_var('history_id')
            else:
                module_obj = load_module(func[0].module)
                function = getattr(module_obj, func[0].internal)
                
                result = function(context, *arguments, **kwargs)
                datatype = Library.GetDataTypeFromFunc(func[0].returns)
                task.succeeded(datatype, result)
            return result
        except Exception as e:
            if task:
                task.failed(str(e))
            raise

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

