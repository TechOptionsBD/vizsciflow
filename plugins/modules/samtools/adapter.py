import os
from os import path

from app.system.exechelper import func_exec_run
from app.dsl.argshelper import get_posix_data_args, get_posix_output_args, get_optional_posix_data_args, get_posix_output_folder_args

samtools = path.join(path.abspath(path.dirname(__file__)), path.join('bin', 'samtools'))

def prepare_args(fs, datas, output):
    
    if fs.exists(output):
        separator_index = output.index('.')
        stem = output[:separator_index]
        extensions = output[separator_index + 1:]
        output = fs.unique_filename(os.path.dirname(output), os.path.basename(stem), extensions)

    cmdargs = ['merge', output]
    cmdargs.extend(datas)
    
    return cmdargs

def run_samtools_merge(context, *args, **kwargs):
    
    paramindex, data, fs = get_posix_data_args(0, 'data', context, *args, **kwargs)
    datas = [data]
    while True:
        paramindex, data, _ = get_optional_posix_data_args(paramindex, '', context, *args, **kwargs)
        if not data:
            break
        datas.append(data)
    
    output = get_posix_output_args(-1, 'output', fs, datas[0], context, None, *args, **kwargs)
    
    cmdargs = prepare_args(fs, datas, output)
    
    _,err = func_exec_run(samtools, *cmdargs)
    
    stripped_path = fs.strip_root(output)
    if not fs.exists(output):
        raise ValueError("Merge operation failed due to error: " + err)
    
    return stripped_path

def run_rmdup(context, *args, **kwargs):
    paramindex, data, fs = get_posix_data_args(0, 'data', context, *args, **kwargs)
    if not fs.exists(data):
        raise ValueError("Input file {0} doesn't exist.".format(fs.strip_root(str(data))))

    outdir = get_posix_output_folder_args(paramindex, 'output', fs, context, *args, **kwargs)

    outpath = fs.join(outdir, 'output.bam')
    err = ''
    cmdargs = ['rmdup', data, outpath]
    if fs.isfile(data):
        _,err = func_exec_run(samtools, *cmdargs)

    stripped_html_path = fs.strip_root(outpath)
    if not fs.exists(outpath):
        raise ValueError("Rmdup could not generate the file " + stripped_html_path + " due to error " + err)

    return stripped_html_path