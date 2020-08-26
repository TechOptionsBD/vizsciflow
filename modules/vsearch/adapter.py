import os
from os import path

from ...exechelper import func_exec_run
from ...fileop import PosixFileSystem
from ....util import Utility

vsearch = 'vsearch' # vsearch must be in the path

def run_usearch(context, *args, **kwargs):
    cmdargs = ["-" + args[0]]
    
    fs = PosixFileSystem(Utility.get_rootdir(2))
    input = fs.normalize_path(Utility.get_quota_path(args[1]))
    
    output = ''
    if len(args) > 2:
        out_opt = args[2]
        cmdargs.append('-' + out_opt)
        output = fs.normalize_path(Utility.get_quota_path(args[3]))
        cmdargs.append(output)

    for arg in args[4:]:
        cmdargs.append('-' + arg)
    
    func_exec_run(vsearch, *cmdargs)
    
    return fs.strip_root(output)
    