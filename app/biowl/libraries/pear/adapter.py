import os
from os import path
from ...exechelper import func_exec_run
from ....util import Utility

pear = path.join(path.abspath(path.dirname(__file__)), path.join('bin', 'pear'))

def run_pear(*args, **kwargs):
    
    paramindex = 0
    if 'data1' in kwargs.keys():
        data1 = kwargs['data1']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument missing error in Pear.")
        data1 = args[paramindex]
        paramindex +=1
    
    data1 = Utility.get_normalized_path(data1)
    
    if 'data2' in kwargs.keys():
        data2 = kwargs['data2']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument missing error in Pear.")
        data2 = args[paramindex]
        paramindex +=1
    
    data2 = Utility.get_normalized_path(data2)
    
    forward_fastq = "-f {0}".format(data1)
    reverse_fastq = "-r {0}".format(data2)
    
    output = ''
    if 'output' in kwargs.keys():
        output = kwargs['output']
    else:
        if len(args) == paramindex:
            raise ValueError("Invalid call format for PEAR.")
        output = args[paramindex]
        paramindex +=1
     
    output = Utility.get_normalized_path(output)
       
    cmdargs = []
    cmdargs.append("-o {0}".format(output))
    
    for arg in args[3:]:
        cmdargs.append(arg)
    
    cmdargs.append(forward_fastq)
    cmdargs.append(reverse_fastq)
    
    _,err = func_exec_run(pear, *cmdargs)

    outdir = os.path.dirname(output)
    prefix = os.path.basename(output) + "."
    files = os.listdir(outdir)
    
    fs = Utility.fs_by_prefix(outdir) 
    pear_files = []
    for f in files:
        if f.startswith(prefix):
            pear_files.append(fs.strip_root(f))
    
    if not pear_files:
        raise ValueError("Pear operation failed due to error: " + err)
    
    return pear_files