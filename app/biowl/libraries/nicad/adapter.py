import os
from os import path
from pathlib import Path
import shutil

from ...exechelper import func_exec_run
from ...fileop import PosixFileSystem
from ....util import Utility

nicad = path.join(path.abspath(path.dirname(__file__)), path.join('lib', 'nicad'))
nicadcross = path.join(path.abspath(path.dirname(__file__)), path.join('lib', 'nicad'))

def run_nicad(*args, **kwargs):
    
    paramindex = 0
    if 'granularity' in kwargs.keys():
        granularity = kwargs['granularity']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument 'granularity' missing in nicad.")
        granularity = args[paramindex]
        paramindex +=1
    
    if 'language' in kwargs.keys():
        language = kwargs['language']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument 'language' missing in nicad.")
        language = args[paramindex]
        paramindex +=1
    
    if 'srcdir' in kwargs.keys():
        srcdir = kwargs['srcdir']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument 'srcdir' missing in nicad.")
        srcdir = args[paramindex]
        paramindex +=1
        
    srcdir = Utility.get_normalized_path(srcdir)
    if not os.path.exists(srcdir):
        raise ValueError("'srcdir' doesn't exist for NiCad operation.")
    
    if 'outdir' in kwargs.keys():
        outdir = kwargs['outdir']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument 'outdir' missing in nicad.")
        srcdir = args[paramindex]
        paramindex +=1
    
    outdir = Utility.get_normalized_path(outdir)
    
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    
    shutil.copytree(srcdir, outdir)
    cmdargs = [granularity, language, srcdir, outdir]
                       
    for arg in args[2:]:
        cmdargs.append(arg)
       
    _,err = func_exec_run(nicad, *cmdargs)
        
    fs = PosixFileSystem(Utility.get_rootdir(2))
    stripped_path = fs.strip_root(outdir)
    
    return stripped_path
    
def run_nicadcross(*args, **kwargs):
    
    paramindex = 0
    if 'granularity' in kwargs.keys():
        granularity = kwargs['granularity']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument 'granularity' missing in nicad.")
        granularity = args[paramindex]
        paramindex +=1
    
    if 'language' in kwargs.keys():
        language = kwargs['language']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument 'language' missing in nicad.")
        language = args[paramindex]
        paramindex +=1
    
    if 'srcdir1' in kwargs.keys():
        srcdir = kwargs['srcdir1']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument 'srcdir1' missing in nicad.")
        srcdir1 = args[paramindex]
        paramindex +=1
    
    srcdir1 = Utility.get_normalized_path(srcdir1)
    
    if 'srcdir2' in kwargs.keys():
        srcdir = kwargs['srcdir2']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument 'srcdir2' missing in nicad.")
        srcdir2 = args[paramindex]
        paramindex +=1
        
    srcdir2 = Utility.get_normalized_path(srcdir2)
    
    if 'outdir' in kwargs.keys():
        outdir = kwargs['outdir']
    else:
        if len(args) > paramindex:
            outdir = args[paramindex]
            paramindex +=1
    
    if outdir:
        outdir = Utility.get_normalized_path(outdir)
    else:
        outdir = srcdir
    
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    
    cmdargs = [granularity, language, srcdir1, srcdir2, outdir]
                       
    for arg in args[2:]:
        cmdargs.append(arg)
       
    _,err = func_exec_run(nicadcross, *cmdargs)
        
    fs = PosixFileSystem(Utility.get_rootdir(2))
    stripped_path = fs.strip_root(outdir)
    
    return stripped_path