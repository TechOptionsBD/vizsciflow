from os import path
import os
from pathlib import Path

from ....util import Utility
from ...exechelper import func_exec_run


fastqc = path.join(path.abspath(path.dirname(__file__)), path.join('lib', 'fastqc'))

def run_fastqc(*args, **kwargs):
    
    paramindex = 0
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument missing error in FastQC.")
        data = args[paramindex]
        paramindex +=1
    
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data)
    
    outdir = ''
    if 'outdir' in kwargs.keys():
        outdir = kwargs['outdir']
    else:
        if len(args) > paramindex:
            outdir = args[paramindex]
            paramindex +=1
    
    if outdir:
        outdir = fs.normalize_path(outdir)
    else:
        outdir = fs.make_unique_dir(path.dirname(data))
    
    cmdargs = [data, "--outdir=" + outdir]
                       
    for arg in args[2:]:
        cmdargs.append(arg)
    
    outpath = Path(data).stem + "_fastqc.html"
    outpath = os.path.join(outdir, os.path.basename(outpath))
    if fs.exists(outpath):
        fs.remove(outpath)
    
    _,err = func_exec_run(fastqc, *cmdargs)
        
    
    stripped_path = fs.strip_root(outpath)
    if not fs.exists(outpath):
        raise ValueError("FastQC could not generate the file " + stripped_path + " due to error " + err)
    
    return stripped_path
    