from os import path
from pathlib import Path
import re

thispath = path.dirname(__file__)

def demo_service(context, *args, **kwargs):

    # get paths to tools
    blastz = path.join(thispath, 'bin', 'blastz.py')
    lastz = path.join(thispath, 'bin', 'lastz')

    # parse query sequence and database to blast against
    paramindex, query, fs = context.getdataarg(0, 'query', *args, **kwargs)
    _, db, _ = context.getdataarg(paramindex, 'db', *args, **kwargs)
    
    # find databse ID of input data
    ids = re.findall(r'\d+', Path(query).stem + Path(db).stem)

    if not ids:
        raise ValueError("Invalid input files.")
    
    # run BLASTZ and write result to output file
    output = path.join(context.createoutdir(), "{0}_{1}.CDS-CDS.{2}".format(ids[0], ids[1], 'lastz'))
    cmdargs = ["-A", "44", "-i", query, "-d", db, "-o", output, '--path='+lastz]
    
    out, err = context.pyvenv_run_at_venv(thispath, "python2", '.venvpy2', blastz, *cmdargs)
    context.save_stdout_stderr(out, err)

    stripped_path = fs.strip_root(output)
    
    if not fs.exists(output):
        raise ValueError("BlastZ could not generate the file " + stripped_path + " due to error " + err)

    return output