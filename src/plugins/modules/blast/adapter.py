from os import path
from pathlib import Path
blastn = path.join(path.abspath(path.dirname(__file__)), path.join('bin', 'blastn'))
            
def run_blastn(context, *args, **kwargs):
           
    paramindex, data, fs = context.getdataarg(0, 'data', *args, **kwargs)
    _, db, _ = context.getdataarg(paramindex, 'db', *args, **kwargs)

    outpath = context.createoutdir()
        
    cmdargs = ["-query", data, "-db", Path(db).stem, "-out", outpath]
    _,err = context.exec_run(blastn, *cmdargs, cwd=path.dirname(db))

    stripped_html_path = fs.strip_root(outpath)
    if not fs.exists(outpath):
        raise ValueError("Blast could not generate the file " + stripped_html_path + " due to error " + err)

    return outpath