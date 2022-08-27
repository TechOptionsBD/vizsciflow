from os import path
from pathlib import Path
import os

thispath = path.dirname(__file__)

def run_last(context, *args, **kwargs):
    
    last = path.join(context.getnormdir(__file__), 'bin', 'last.py')

    arguments = context.parse_args('Last', 'CoGe', *args, **kwargs)

    # parse ID of query and db sequence
    id1 = "".join([s for s in Path(arguments["data"]).stem if s.isdigit()])
    id2 = "".join([s for s in Path(arguments["data2"]).stem if s.isdigit()])

    outpath = path.join(context.createoutdir(), "{0}_{1}.{2}".format(id1, id2, 'CDS-CDS.last'))
    cmdargs = ["-a 44 --dbpath="+context.createoutdir(), arguments["data"], arguments["data2"], "-o", outpath]
    
    _, log = context.pyvenv_run(thispath, "python2", last, *cmdargs)

    if os.stat(outpath).st_size == 0:
        # if output file is empty, Last failed
        raise ValueError("Last failed to generate file: " + outpath + " due to error: " + log)
    else:
        # report log
        context.out.append("Last log:\n" + str(log))

    return outpath