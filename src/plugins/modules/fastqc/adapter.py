from os import path
import os
from pathlib import Path

from app.system.exechelper import func_exec_run
from app.dsl.argshelper import get_posix_data_args, get_posix_output_folder_args

fastqc = path.join(path.abspath(path.dirname(__file__)), path.join('bin', 'fastqc'))

def prepare_args(fs, data, outdir, paramindex, *args):   
    outname = Path(data).stem + "_fastqc.html"
    outpath = fs.join(outdir, outname)
    if fs.exists(outpath):
        outdir = fs.make_unique_dir(outdir) # create a subdirectory
        outpath = fs.join(outdir, outname)
    
    cmdargs = [data, "--outdir=" + outdir]
                           
    for arg in args[paramindex:]:
        cmdargs.append(arg)

    return cmdargs, fs.join(outdir, outname), fs.join(outdir, Path(data).stem + "_fastqc.zip")
            
def run_fastqc(context, *args, **kwargs):
    
    paramindex, data, fs = get_posix_data_args(0, 'data', context, *args, **kwargs)
    if not fs.exists(data):
        raise ValueError("Input file {0} doesn't exist.".format(fs.strip_root(str(data))))

    outdir = get_posix_output_folder_args(paramindex, 'outdir', fs, context, *args, **kwargs)

    outpath = outdir
    outzip = outdir
    err = ''
    if fs.isfile(data):
        cmdargs, outpath, outzip = prepare_args(fs, data, outdir, paramindex, *args)
        _,err = func_exec_run(fastqc, *cmdargs)
    else:
        for r, _, f in os.walk(data):
            for datafile in [os.path.join(r, file) for file in f if file.endswith(".fastq") or file.endswith(".fq")]:
                try:
                    cmdargs, _, _ = prepare_args(fs, datafile, outdir, paramindex, *args)
                    _,err = func_exec_run(fastqc, *cmdargs)
                except Exception as err:
                    context.err.append(str(err))
                        
    stripped_html_path = fs.strip_root(outpath)
    if not fs.exists(outpath):
        raise ValueError("FastQC could not generate the file " + stripped_html_path + " due to error " + err)

    return stripped_html_path, fs.strip_root(outzip)