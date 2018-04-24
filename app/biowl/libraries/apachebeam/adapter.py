import sys
import os
import uuid

from ...exechelper import func_exec_run
from ...fileop import PosixFileSystem
from ....util import Utility

python_ex = path.join(path.abspath(path.dirname(__file__)), path.join('lib', 'venv', 'bin', 'python'))

def run_apachebeam(*args, **kwargs):
    return func_exec_run(python_ex, args)
       

def count_words(*args, **kwargs):
    
    paramindex = 0
    if 'input' in kwargs.keys():
        input = kwargs['input']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument 'input' missing.")
        input = args[paramindex]
        paramindex +=1
    
    if 'output' in kwargs.keys():
        output = kwargs['output']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument 'output' missing.")
        output = args[paramindex]
        paramindex +=1
    
    input = Utility.get_normalized_path(input)
    output = Utility.get_normalized_path(output)
    
    args = ['-m', 'apache_beam.examples.wordcount', input, output]
    
    _err, _ = run_apachebeam(args)
    
    fs = PosixFileSystem(Utility.get_rootdir(2))
    stripped_path = fs.strip_root(output)
    if not os.path.exists(output):
        raise ValueError("CountWords could not generate the file " + stripped_path + " due to error: " + err)
    
    return stripped_path
    
if __name__ == "__main__":
    run_hadoop(sys.argv[1], sys.argv[2])
