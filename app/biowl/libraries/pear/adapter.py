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
        
    cmdargs = []
    cmdargs.append("-o {0}".format(output))
    
    for arg in args[3:]:
        cmdargs.append(arg)
    
    cmdargs.append(forward_fastq)
    cmdargs.append(reverse_fastq)
    
    _,err = func_exec_run(pear, *cmdargs)
    
    fs = Utility.fs_by_prefix(output)
    stripped_path = fs.strip_root(output)
    if not os.path.exists(output):
        raise ValueError("Pear could not generate the file " + stripped_path + " due to error " + err)
    
    return stripped_path