from ..models import Service
from dsl.library import Pair
from dsl.datatype import DataType
from .vizsciflowlib import Library
from .dsl.wfdsl import Data, Module

class LibraryComposition(Library):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def adjust_datatype(data):
        if isinstance(data, Data):
            return data
        elif isinstance(data, tuple):
            result = tuple()
            for t in data:
                d = LibraryComposition.adjust_datatype(t)
                result = result + (d,)
            return result
        else:
            d = Data()
            d.value = data
            d.datatype = str(type(d))
            return d
            
    @staticmethod
    def split_args(arguments):
        args = []
        kwargs = {}
        for arg in arguments:
            if isinstance(arg, Pair):
                kwargs[arg[0]] = arg[1]
            elif isinstance(arg, tuple):
                for t in arg:
                    args.append(t)
            else:
                args.append(arg)
        return args, kwargs
        
    @staticmethod
    def call_func(parent, package, function, args):
        '''
        Call a function from a module.
        :param parent: The parent for output and error
        :param package: The name of the package. If it's empty, local function is called    
        :param function: Name of the function
        :param args: The arguments for the function
        '''
        if not package and function.lower() == "addmodule":
            f = args[0].value if isinstance(args[0], Data) else args[0]
            pkgfunc = f.split(".")
            if pkgfunc == 1:
                function = pkgfunc
            else:
                package = pkgfunc[0]
                function = pkgfunc[1]
            args = args[1:]
        func = Service.get_first_service_by_name_package(function, package)
        arguments, kwargs = LibraryComposition.split_args(args)
        storeArguments = list(arguments)
        for _, v in kwargs.items():
            storeArguments.append(v)
                   
        module = Module(function, package)
        
        params = func["params"] if func["params"] else []
        for i in range(0, len(storeArguments)):
            data = LibraryComposition.adjust_datatype(storeArguments[i])
            paramType = DataType.Value
            if i < len(params):
                data.name = params[i]["name"]
                paramType = params[i]["type"]
                paramType = paramType.lower().split('|')
                if 'file' in paramType:
                    paramType = DataType.File
                elif 'folder' in paramType:
                    paramType = DataType.Folder

            data.valuetype = paramType
            if not isinstance(storeArguments[i], Data):
                data.value = storeArguments[i]
            module.inputs().append(data)
        
        returns = func["returns"] if func["returns"] else []
        if not isinstance(returns, list) and not isinstance(returns, tuple):
            returns = [returns]
        for ret in returns:
            output = Data()
            output.expected = True
            if "type" in ret:
                returnType = ret["type"]
                returnType = returnType.lower().split('|')
                if 'file' in returnType:
                    returnType = DataType.File
                elif 'folder' in paramType:
                    returnType = DataType.Folder
                output.valuetype = returnType
            if "name" in ret:
                output.name =ret["name"]
            
            module.outputs().append(output)
        
        parent.modules().append(module)
        return tuple(module.outputs()) if len(module.outputs()) else module.outputs()[0]
        
