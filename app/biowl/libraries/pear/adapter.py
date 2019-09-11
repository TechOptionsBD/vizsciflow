import os
from os import path
from pathlib import Path

from ...exechelper import func_exec_run
from ...argshelper import get_posix_data_args, get_posix_output_args
from ....util import Utility
from app.models import AccessRights, DataType
from ...fileop import FolderItem

pear = path.join(path.abspath(path.dirname(__file__)), path.join('bin', 'pear'))

def prepare_args(fs, data1, data2, output, *args):
    cmdargs = []
    
    if fs.exists(output):
        separator_index = output.index('.')
        stem = output[:separator_index]
        extensions = output[separator_index + 1:]
        output = fs.unique_filename(os.path.dirname(output), os.path.basename(stem), extensions)
        
    cmdargs.append("-o {0}".format(output))
    
#     for arg in args[3:]:
#         cmdargs.append(arg)
    
    cmdargs.append("-f {0}".format(data1))
    cmdargs.append("-r {0}".format(data2))
    
    return cmdargs

def run_pear(context, *args, **kwargs):
    
    paramindex, data1, fs = get_posix_data_args(0, 'data', context, *args, **kwargs)
    paramindex, data2, _ = get_posix_data_args(paramindex, 'data2', context, *args, **kwargs)
    output = get_posix_output_args(paramindex, 'output', fs, data1, context, None, *args, **kwargs)
    
    data1_path = Path(output)
    assembled_output = fs.join(fs.dirname(output), data1_path.stem) + ".assembled" + data1_path.suffix    
    cmdargs = prepare_args(fs, data1, data2, fs.join(fs.dirname(output), data1_path.stem), *args, **kwargs)
    
    _,err = func_exec_run(pear, *cmdargs)

#     prefix = os.path.basename(output) + "."
#     files = os.listdir(outdir)
#     
#     pear_files = []
#     for f in files:
#         if f.startswith(prefix):
#             pear_files.append(fs.strip_root(f))
    stripped_path = fs.strip_root(assembled_output)
    if not fs.exists(assembled_output):
        raise ValueError("Pear operation failed due to error: " + err)
    
    Utility.add_meta_data(stripped_path, context.user_id, context.runnable, context.task_id, AccessRights.Owner, DataType.File if fs.isfile(output) else DataType.Folder)
    
    return FolderItem(stripped_path)