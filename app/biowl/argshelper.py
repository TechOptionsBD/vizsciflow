import os
from pathlib import Path
from ..util import Utility

def get_temp_dir(context, typename = "posix"):
    '''
    The user directory for a fs type is the temp directory.
    '''
    if context.user_id:
        if not typename in context.tempdirs:
            fs = Utility.fs_by_typename(typename)
            context.tempdirs[typename] = fs.make_unique_dir(fs.temp if fs.temp else 'temp')
        return context.tempdirs[typename]
        
def get_input_from_args(paramindex, keyname, *args, **kwargs):
    
    barcode = ''
    if keyname in kwargs.keys():
        barcode = str(kwargs[keyname])
    else:
        if len(args) == paramindex:
            raise ValueError("Argument {0} missing error in function call.".format(keyname))
        barcode = str(args[paramindex])
        paramindex +=1
    
    return paramindex, barcode

def get_optional_input_from_args(paramindex, keyname, *args, **kwargs):
    
    barcode = ''
    if keyname in kwargs.keys():
        barcode = str(kwargs[keyname])
    else:
        if len(args) > paramindex:
            barcode = str(args[paramindex])
            paramindex +=1
    
    return paramindex, barcode

def get_optional_posix_data_args(paramindex, keyname, context, *args, **kwargs):
    
    paramindex, data = get_optional_input_from_args(paramindex, keyname, *args, **kwargs)
    if not data:
        return paramindex, data, None
    
    #DataAllocation.check_access_rights(context.user_id, str(data), AccessRights.Read)
    
    fs = None
    if Utility.fs_type_by_prefix(data) != 'posix':
        tempdir = get_temp_dir(context, 'posix')
        fssrc = Utility.fs_by_prefix(data)
        if not fssrc:
            raise ValueError("Data doesn't exist: " + str(data))
        fs = Utility.fs_by_prefix(tempdir)
        dest = fs.join(tempdir, fssrc.basename(data))
        fs.write(dest, fssrc.read(data))
        data = dest
    else:
        fs = Utility.fs_by_prefix_or_guess(data)
        
    data = fs.normalize_path(str(data))
    
    return paramindex, data, fs

def get_posix_data_args(paramindex, keyname, context, *args, **kwargs):
    
    paramindex, data = get_input_from_args(paramindex, keyname, *args, **kwargs)
    
    #DataSourceAllocation.check_access_rights(context.user_id, data, AccessRights.Read)
    
    fs = None
    if Utility.fs_type_by_prefix(data) != 'posix':
        tempdir = get_temp_dir(context, 'posix')
        fssrc = Utility.fs_by_prefix_or_guess(data)
        if not fssrc:
            raise ValueError("Data doesn't exist: " + str(data))
        fs = Utility.fs_by_prefix(tempdir)
        dest = fs.join(tempdir, fssrc.basename(data))
        fs.write(dest, fssrc.read(data))
        data = dest
    else:
        fs = Utility.fs_by_prefix_or_guess(data)
        
    data = fs.normalize_path(data)
    
    return paramindex, data, fs

def get_posix_output_folder_args(paramindex, keyname, fs, context, *args, **kwargs):
    outdir = ''
    if keyname in kwargs.keys():
        outdir = str(kwargs[keyname])
    else:
        if len(args) > paramindex:
            outdir = str(args[paramindex])
            paramindex +=1
    
    if outdir and Utility.fs_type_by_prefix(outdir) == 'posix':
        outdir = fs.normalize_path(outdir)
        #DataSourceAllocation.check_access_rights(context.user_id, outdir, AccessRights.Write)
        if not fs.exists(outdir):
            fs.makedirs(outdir)
    else:
        outdir = get_temp_dir(context, 'posix')
    
    return outdir

def get_posix_output_args(paramindex, keyname, fs, data, context, ext, *args, **kwargs):
    output = ''
    if keyname in kwargs.keys():
        output = str(kwargs[keyname])
    else:
        if paramindex >= 0 and len(args) > paramindex:
            output = str(args[paramindex])
            paramindex +=1
    
    data_path = Path(os.path.basename(data))
    if not output:
        output = fs.join(get_temp_dir(context, fs.typename()), data_path.stem)
        output += ext if ext else "_output" + data_path.suffix
    else:
        #DataSourceAllocation.check_access_rights(context.user_id, output, AccessRights.Write)
        if not fs.exists(fs.dirname(output)):
            fs.mkdir(fs.dirname(output))
    
    return fs.normalize_path(output)

def get_input_from_args_optional(paramindex, keyname, default, *args, **kwargs):
    
    barcode = default
    if keyname in kwargs.keys():
        barcode = str(kwargs[keyname])
    else:
        if len(args) > paramindex:
            barcode = str(args[paramindex])
            paramindex +=1
            
    return paramindex, barcode

def get_output_path_from_args(paramindex, fs, data, keyname, default, *args, **kwargs):
    repseqs=default
    if keyname in kwargs.keys():
        repseqs = str(kwargs[keyname])
    else:
        if len(args) > paramindex:
            repseqs = str(args[paramindex])
            paramindex +=1
    
    if not repseqs:
        repseqs = fs.join(os.path.dirname(data), repseqs)
        
    if fs.exists(repseqs):
        repseqs =  fs.make_unique_dir(os.path.dirname(repseqs))
    
    return paramindex, fs.normalize_path(repseqs)