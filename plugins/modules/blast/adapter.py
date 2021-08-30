import os
from os import path
import uuid

from app.system.exechelper import func_exec_run
from app.dsl.argshelper import get_posix_data_args, get_input_from_args
from pathlib import Path
blastn = path.join(path.abspath(path.dirname(__file__)), path.join('bin', 'blastn'))
            
def run_blastn(context, *args, **kwargs):
           
    paramindex, data, fs = get_posix_data_args(0, 'data', context, *args, **kwargs)
    _, db, fs = get_posix_data_args(paramindex, 'db', context, *args, **kwargs)

    outpath = path.abspath(path.join(path.dirname(__file__), '../../storage/output', str(context.task_id)))
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    outpath = path.join(outpath, str(uuid.uuid4()))
        
    pwd = os.curdir
    os.chdir(path.dirname(db))
    try:
        cmdargs = ["-query", data, "-db", Path(db).stem, "-out", outpath]
        _,err = func_exec_run(blastn, *cmdargs)
    finally:
        os.chdir(pwd)

    stripped_html_path = fs.strip_root(outpath)
    if not fs.exists(outpath):
        raise ValueError("FastQC could not generate the file " + stripped_html_path + " due to error " + err)

    return outpath