import os
from os import path
from pathlib import Path

from app.biowl.exechelper import func_exec_run
from app.biowl.argshelper import get_posix_data_args, get_posix_output_args, get_optional_posix_data_args, get_posix_output_folder_args, get_temp_dir
from app.models import AccessRights, DataSourceAllocation
from dsl.fileop import FolderItem

bwa = path.join(path.abspath(path.dirname(__file__)), path.join('bin', 'bwa'))

def prepare_args(fs, ref, data1, data2, output, *args):
    
    cmdargs = ['mem', ref, data1]
    if data2:
        cmdargs.append(data2)
    
    if fs.isdir(output):
        data_path = Path(data1)
        output = fs.join(output, data_path.stem) + ".sam"
    cmdargs.append("-o {0}".format(output))
    
#     for arg in args[paramindex + 1:]:
#         cmdargs.append(arg)
        
    return cmdargs, output

def build_bwa_index(ref):
    cmdargs = ['index', ref]
    return func_exec_run(bwa, *cmdargs)
    
def run_bwa(context, *args, **kwargs):
    paramindex, ref, fs = get_posix_data_args(0, 'ref', context, *args, **kwargs)
    paramindex, data1, _ = get_posix_data_args(paramindex, 'data', context, *args, **kwargs)
    paramindex, data2, _ = get_optional_posix_data_args(paramindex, 'data2', context, *args, **kwargs)
    paramindex, indexpath, _ = get_optional_posix_data_args(paramindex, 'index', context, *args, **kwargs)
    output = get_posix_output_args(paramindex, 'output', fs, data1, context, ".sam", *args, **kwargs) if fs.isfile(data1) else get_posix_output_folder_args(paramindex, 'output', fs, context, *args, **kwargs)

    if not indexpath:
        indexpath = Path(ref).stem + ".bwt"
        indexpath = fs.join(fs.dirname(ref), indexpath)
        
        if not fs.exists(indexpath):
            if not DataSourceAllocation.has_access_rights(context.user_id, fs.dirname(ref), AccessRights.Write):
                ref = fs.copyfile(ref, fs.join(get_temp_dir(context, fs.typename()), fs.basename(ref)))
                indexpath = Path(ref).stem + ".bwt"
                indexpath = fs.join(fs.dirname(ref), indexpath)
            build_bwa_index(ref)

    if fs.isfile(data1):
        cmdargs, output = prepare_args(fs, ref, data1, data2, output, *args)
        _,err = func_exec_run(bwa, *cmdargs)
    else:
        for r, _, f in os.walk(data1):
            for datafile in [os.path.join(r, file) for file in f if file.endswith(".fastq") or file.endswith(".fq")]:
                try:
                    cmdargs, _ = prepare_args(fs, ref, datafile, None, output, *args)
                    _,err = func_exec_run(bwa, *cmdargs)
                except Exception as err:
                    context.err.append(str(err))
    
    stripped_path = fs.strip_root(output)
    if not fs.exists(output):
        raise ValueError("bwa could not generate the file " + stripped_path + " due to error " + err)
    
    return FolderItem(stripped_path)