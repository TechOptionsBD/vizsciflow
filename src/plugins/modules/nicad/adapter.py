import os
from os import path
from pathlib import Path
import shutil

from app.dsl.argshelper import get_posix_data_args, get_optional_input_from_args

thispath = path.abspath(path.dirname(__file__))
nicad = path.join(thispath, 'NiCad-6.2', 'nicad6')
nicadcross = path.join(thispath, 'NiCad-6.2', 'nicad6cross')
systemsdir = os.path.join(thispath, 'NiCad-6.2', 'systems/')

def run_nicad(context, *args, **kwargs):

    txldir = context.getsystooldir('txl')
    if not txldir:
        raise ValueError("NiCad needs TXL. But it is not installed. Please install TXL first.")

    paramindex, data, fs = context.getarg(0, 'data', *args, **kwargs)
    paramindex, granularity = context.getoptionalarg(paramindex, 'granularity', *args, **kwargs)
    paramindex, language = context.getoptionalarg(paramindex, 'language', *args, **kwargs)
    
    srcdir = context.copyto(data, systemsdir, ".git")
    srcname = os.path.basename(srcdir)
    cmdargs = [granularity, language, os.path.join('systems', srcname), 'default-report']
    out, err = context.exec_run(nicad, *cmdargs, cwd=os.path.dirname(nicad), env='/home/vizsciflow/bin')
    shutil.rmtree(srcdir)
    
    outdir = context.createoutdir(srcname)
    context.moveto(systemsdir, outdir)

    return outdir
    
def run_nicadcross(context, *args, **kwargs):
    txldir = context.getsystooldir('txl')
    if not txldir:
        raise ValueError("NiCad needs TXL. But it is not installed. Please install TXL first.")

    paramindex, data, fs = context.getarg(0, 'data', *args, **kwargs)
    paramindex, granularity = context.getoptionalarg(paramindex, 'granularity', *args, **kwargs)
    paramindex, language = context.getoptionalarg(paramindex, 'language', *args, **kwargs)
    
    srcdir = context.copyto(data, systemsdir, ".git")
    srcname = os.path.basename(srcdir)
    cmdargs = [granularity, language, os.path.join('systems', srcname), 'default-report']
    out, err = context.exec_run(nicadcross, *cmdargs, cwd=os.path.dirname(nicad), env='/home/vizsciflow/bin')
    shutil.rmtree(srcdir)
    
    outdir = context.createoutdir(srcname)
    context.moveto(systemsdir, outdir)

    return outdir