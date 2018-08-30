import os
from os import path
from pathlib import Path

from ...exechelper import func_exec_run
from ....util import Utility

bwa = path.join(path.abspath(path.dirname(__file__)), path.join('bin', 'bwa'))

def build_bwa_index(ref):
    cmdargs = ['index', ref]
    return func_exec_run(bwa, *cmdargs)
    
def run_bwa(*args, **kwargs):
    
    paramindex = 0
    ref = ''
    if 'ref' in kwargs.keys():
        ref = kwargs['ref']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument error")
        ref = args[paramindex]
        paramindex +=1
        
    fs = Utility.fs_by_prefix_or_default(ref)
    ref = fs.normalize_path(ref)
    
    indexpath = Path(ref).stem + ".bwt"
    indexpath = os.path.join(os.path.dirname(ref), os.path.basename(indexpath))
    if not fs.exists(indexpath):
        build_bwa_index(ref)
    
    data1 = ''
    if 'data1' in kwargs.keys():
        data1 = kwargs['data1']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument error")
        data1 = args[paramindex]
        paramindex +=1
    
    data1 = fs.normalize_path(data1)
    
    data2 = ''
    if 'data2' in kwargs.keys():
        data2 = kwargs['data2']
    else:
        if len(args) > paramindex:
            data2 = args[paramindex]
            paramindex +=1
    
    if data2:
        data2 = fs.normalize_path(data2)
    
    output = ''    
    if 'output' in kwargs.keys():
        output = kwargs['output']
    else:
        if len(args) > paramindex:
            output = args[paramindex]
            paramindex +=1
    
    if not output:
        output = Path(data1).stem + ".sam"
        outdir = fs.make_unique_dir(path.dirname(data1))
        output = os.path.join(outdir, os.path.basename(output))
        
    output = fs.normalize_path(output)
    
    if not fs.exists(path.dirname(output)):
        fs.makedirs(path.dirname(output))
        
    if os.path.exists(output):
        os.remove(output)

    cmdargs = ['mem', ref, data1]
    if data2:
        cmdargs.append(data2)
        
    cmdargs.append("-o {0}".format(output))
    
    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)
    
    _,err = func_exec_run(bwa, *cmdargs)
    
    stripped_path = fs.strip_root(output)
    if not fs.exists(output):
        raise ValueError("bwa could not generate the file " + stripped_path + " due to error " + err)
    
    return stripped_path