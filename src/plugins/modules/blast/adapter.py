import os
from os import path
import uuid

from app.system.exechelper import func_exec_run
from pathlib import Path
blastn = path.join(path.abspath(path.dirname(__file__)), path.join('bin', 'blastn'))
            
def run_blastn(context, *args, **kwargs):
           
    paramindex, data, fs = context.getdataarg(0, 'data', context, *args, **kwargs)
    _, db, _ = context.getdataarg(paramindex, 'db', context, *args, **kwargs)

    outpath = context.createoutdir()
        
    cmdargs = ["-query", data, "-db", Path(db).stem, "-out", outpath]
    _,err = func_exec_run(blastn, *cmdargs, cwd=path.dirname(db))

    stripped_html_path = fs.strip_root(outpath)
    if not fs.exists(outpath):
        raise ValueError("Blast could not generate the file " + stripped_html_path + " due to error " + err)

    return outpath