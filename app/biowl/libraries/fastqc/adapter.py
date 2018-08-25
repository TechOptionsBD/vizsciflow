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
    
    fs = Utility.fs_by_prefix(data)
    data = fs.normalize_path(data)
    
    outdir = ''
    if 'outdir' in kwargs.keys():
        outdir = kwargs['outdir']
    else:
        if len(args) > paramindex:
            outdir = args[paramindex]
            paramindex +=1
    
    if not outdir:
        outdir = path.dirname(data)

    outdir = fs.normalize_path(outdir)    
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    
    cmdargs = [data, "--outdir=" + outdir]
                       
    for arg in args[2:]:
        cmdargs.append(arg)
    
    outpath = Path(data).stem + "_fastqc.html"
    outpath = os.path.join(outdir, os.path.basename(outpath))
    if os.path.exists(outpath):
        os.remove(outpath)
    
    _,err = func_exec_run(fastqc, *cmdargs)
        
    
    stripped_path = fs.strip_root(outpath)
    if not os.path.exists(outpath):
        raise ValueError("FastQC could not generate the file " + stripped_path + " due to error " + err)
    
    return stripped_path
    