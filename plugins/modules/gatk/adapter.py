import os
from os import path

from app.system.exechelper import func_exec_run
from app.io.fileop import PosixFileSystem
from app.util import Utility

gatk = path.join(path.abspath(path.dirname(__file__)), path.join('lib', 'gatk'))

def run_gatk(*args, **kwargs):
    return func_exec_run(gatk, args)
       

def run_fastq_to_sam(*args, **kwargs):
    
    paramindex = 0
    if 'input' in kwargs.keys():
        inputfile = kwargs['input']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument 'input' missing.")
        inputfile = args[paramindex]
        paramindex +=1
    
    if 'output' in kwargs.keys():
        output = kwargs['output']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument 'output' missing.")
        output = args[paramindex]
        paramindex +=1
    
    inputfile = Utility.get_normalized_path(inputfile)
    output = Utility.get_normalized_path(output)
    
    args = ['FastqToSam', '-F1=' + inputfile, '-O=' + output]
    
    _err, _ = run_gatk(args)
    
    fs = PosixFileSystem(Utility.get_rootdir(2))
    stripped_path = fs.strip_root(output)
    if not os.path.exists(output):
        raise ValueError("CountWords could not generate the file " + stripped_path + " due to error: " + _err)
    
    return stripped_path
