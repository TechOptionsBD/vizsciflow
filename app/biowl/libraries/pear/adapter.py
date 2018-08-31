import os
from os import path
from ...exechelper import func_exec_run
from ....util import Utility
from pathlib import Path

pear = path.join(path.abspath(path.dirname(__file__)), path.join('bin', 'pear'))

def run_pear(*args, **kwargs):
    
    paramindex = 0
    if 'data' in kwargs.keys():
        data1 = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("Argument missing error in PEAR.")
        data1 = args[paramindex]
        paramindex +=1
    
    fs = Utility.fs_by_prefix_or_default(data1)
    data1 = fs.normalize_path(data1)
    
    if 'data2' in kwargs.keys():
        data2 = kwargs['data2']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument missing error in PEAR.")
        data2 = args[paramindex]
        paramindex +=1
    
    data2 = fs.normalize_path(data2)
    
    output = ''    
    if 'output' in kwargs.keys():
        output = kwargs['output']
    else:
        if len(args) > paramindex:
            output = args[paramindex]
            paramindex +=1
    
    data1_path = Path(os.path.basename(data1))
    if not output:
        outdir = fs.make_unique_dir(path.dirname(data1))
        output = os.path.join(outdir, data1_path.stem)
        
    output = fs.normalize_path(output)
    
    outdir = path.dirname(output)
    if not fs.exists(outdir):
        fs.makedirs(outdir)
    
    assembled_output = output + ".assembled" + data1_path.suffix    
    if os.path.exists(assembled_output):
        os.remove(assembled_output)
        
    cmdargs = []
    cmdargs.append("-o {0}".format(output))
    
    for arg in args[3:]:
        cmdargs.append(arg)
    
    cmdargs.append("-f {0}".format(data1))
    cmdargs.append("-r {0}".format(data2))
    
    _,err = func_exec_run(pear, *cmdargs)

#     prefix = os.path.basename(output) + "."
#     files = os.listdir(outdir)
#     
#     pear_files = []
#     for f in files:
#         if f.startswith(prefix):
#             pear_files.append(fs.strip_root(f))
    
    if not fs.exists(assembled_output):
        raise ValueError("Pear operation failed due to error: " + err)
    
    return assembled_output