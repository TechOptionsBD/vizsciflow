import os
from os import path
from pathlib import Path
import shutil

from app.dsl.argshelper import get_posix_data_args, get_optional_input_from_args

thispath = path.abspath(path.dirname(__file__))
nicad = path.join(thispath, 'NiCad-6.2', 'nicad6')
nicadcross = path.join(thispath, 'NiCad-6.2', 'nicad6cross')

def run_nicad(context, *args, **kwargs):

    txldir = context.gettoolsdir('txl')
    if not txldir:
        raise ValueError("NiCad needs TXL. But it is not installed. Please install TXL first.")

    paramindex, data, fs = context.getdataarg(0, 'data', *args, **kwargs)
    paramindex, granularity = context.getoptionalarg(paramindex, 'granularity', *args, **kwargs)
    paramindex, language = context.getoptionalarg(paramindex, 'language', *args, **kwargs)
    paramindex, makecopy = context.getoptionalarg(paramindex, 'makecopy', *args, **kwargs)
    
    outdir = data
    if makecopy:
        outdir = context.createoutdir()
        data = context.copyto(data, outdir, ".git")
    cmdargs = [granularity, language, data, 'default-report']
    out, err = context.exec_run(nicad, *cmdargs, cwd=os.path.dirname(nicad), env=txldir)

    return path.dirname(data)
    
def run_nicadcross(context, *args, **kwargs):
    txldir = context.gettoolsdir('txl')
    if not txldir:
        raise ValueError("NiCad needs TXL. But it is not installed. Please install TXL first.")

    paramindex, data, fs = context.getdataarg(0, 'data', *args, **kwargs)
    paramindex, granularity = context.getoptionalarg(paramindex, 'granularity', *args, **kwargs)
    paramindex, language = context.getoptionalarg(paramindex, 'language', *args, **kwargs)
    paramindex, makecopy = context.getoptionalarg(paramindex, 'makecopy', *args, **kwargs)
    
    outdir = data
    if makecopy:
        outdir = context.createoutdir()
        data = context.copyto(data, outdir, ".git")
    cmdargs = [granularity, language, data, 'default-report']
    out, err = context.exec_run(nicadcross, *cmdargs, cwd=os.path.dirname(nicad), env=txldir)

    return path.dirname(data)