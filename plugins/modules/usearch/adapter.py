import os
from os import path

from app.biowl.exechelper import func_exec_run
from app.biowl.fileop import PosixFileSystem
from app.util import Utility

usearch = path.join(path.abspath(path.dirname(__file__)), path.join('bin', 'usearch10.0.240_i86linux32'))

def run_usearch(context, *args, **kwargs):
    cmdargs = ["-" + args[0]]
    
    fs = PosixFileSystem(Utility.get_rootdir(2))
    input = fs.normalize_path(Utility.get_quota_path(args[1]))
    
    cmdargs.append(input)
    
    output = ''
    if len(args) > 2:
        out_opt = args[2]
        cmdargs.append('-' + out_opt)
        output = fs.normalize_path(Utility.get_quota_path(args[3]))
        cmdargs.append(output)

    for arg in args[4:]:
        cmdargs.append('-' + arg)
    
    func_exec_run(usearch, *cmdargs)
    
    return fs.strip_root(output)
    