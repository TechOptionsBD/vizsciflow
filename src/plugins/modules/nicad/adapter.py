import os
from os import path
from pathlib import Path
import shutil

from app.dsl.argshelper import get_posix_data_args, get_optional_input_from_args, get_optional_posix_data_args

thispath = path.abspath(path.dirname(__file__))
nicad = path.join(thispath, 'NiCad-6.2', 'nicad6')
nicadcross = path.join(thispath, 'NiCad-6.2', 'nicad6cross')
systemsdir = os.path.join(thispath, 'NiCad-6.2', 'systems')

def run_nicad(context, *args, **kwargs):
    paramindex, data, fs = get_posix_data_args(0, 'data', context, *args, **kwargs)
    if not fs.exists(data):
        raise ValueError("Input folder {0} doesn't exist.".format(fs.strip_root(str(data))))

    paramindex, granularity = get_optional_input_from_args(paramindex, 'granularity', *args, **kwargs)
    paramindex, language = get_optional_input_from_args(paramindex, 'language', *args, **kwargs)
    
    srcname = os.path.basename(data)
    srcdir = os.path.join(systemsdir, srcname)
    if os.path.exists(srcdir):
        shutil.rmtree(srcdir)
    os.makedirs(srcdir)
    srcdir = shutil.copytree(data, srcdir, dirs_exist_ok=True, ignore=shutil.ignore_patterns(".git"))

    cmdargs = [granularity, language, os.path.join('systems', srcname), 'default-report']

    oldcwd = os.getcwd()
    oldenvpath = os.environ["PATH"]
    os.chdir(os.path.dirname(nicad))

    out = ""
    err = ""
    try:
        os.environ["PATH"] = os.environ["PATH"] + os.pathsep + '/home/vizsciflow/bin'
        out, err = context.exec_run(nicad, *cmdargs)
    finally:
        os.chdir(oldcwd)
        os.environ["PATH"] = oldenvpath

    shutil.rmtree(srcdir)
    
    resultdir = os.path.join(fs.make_unique_dir(context.gettempdir()), srcname)
    os.makedirs(resultdir)
    for file in os.listdir(systemsdir):
        if file != 'README.txt':
            shutil.move(os.path.join(systemsdir, file), resultdir)

    return resultdir
    
def run_nicadcross(context, *args, **kwargs):
    paramindex, data, fs = get_posix_data_args(0, 'data', context, *args, **kwargs)
    if not fs.exists(data):
        raise ValueError("Input folder {0} doesn't exist.".format(fs.strip_root(str(data))))

    paramindex, data2, fs = get_optional_posix_data_args(0, 'data2', context, *args, **kwargs)

    paramindex, granularity = get_optional_input_from_args(paramindex, 'granularity', *args, **kwargs)
    paramindex, language = get_optional_input_from_args(paramindex, 'language', *args, **kwargs)
    
    srcname = os.path.basename(data)
    srcdir = shutil.copytree(srcdir, os.path.join(thispath, 'NiCad-6.2', 'systems'), dirs_exist_ok=True)

    cmdargs = [granularity, language, 'systems' + '/' + srcname]
    # for arg in args[2:]:
    #     cmdargs.append(arg)
       
    _,err = context.exec_run(nicad, *cmdargs)

    resultname = srcname + '_functions--blind-clones'
    resultpath = os.path.join(thispath, 'NiCad-6.2', 'systems', resultname)

    resultdir = fs.make_unique_dir(context.gettempdir())
    shutil.move(resultpath, resultdir)

    shutil.rmtree(srcdir)
    return context.denormalize(os.path.join(resultdir, resultname))