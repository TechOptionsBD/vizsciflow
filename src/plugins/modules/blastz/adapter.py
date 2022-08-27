from os import path
from pathlib import Path

thispath = path.dirname(__file__)

def demo_service(context, *args, **kwargs):

    # get paths to tools
    blastz = path.join(thispath, 'bin', 'blastz.py')
    lastz = path.join(thispath, 'bin', 'lastz')

    # parse query sequence and database to blast against
    paramindex, query, fs = context.getdataarg(0, 'query', *args, **kwargs)
    _, db, _ = context.getdataarg(paramindex, 'db', *args, **kwargs)
    
    # run BLASTZ and write result to output file
    output = path.join(context.createoutdir(), "{0}_{1}.{2}".format(Path(query).stem, Path(db).stem, 'lastz'))
    cmdargs = ["-A 44 -i", query, "-d", db, "-o", output, '--path='+lastz]
    
    _, err = context.pyvenv_run(thispath, "python2", blastz, *cmdargs)
    
    stripped_path = fs.strip_root(output)
    
    if not fs.exists(output):
        raise ValueError("BlastZ could not generate the file " + stripped_path + " due to error " + err)

    return output