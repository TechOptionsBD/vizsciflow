from os import path
import os
from pathlib import Path

fastqc = path.join(path.abspath(path.dirname(__file__)), path.join('bin', 'fastqc'))
            
def run_fastqc(context, *args, **kwargs):
    
    arguments = context.parse_args('CheckQuality', 'fastqc', *args, **kwargs)
    outdir = context.createoutdir()

    if path.isfile(arguments["data"]):
        cmdargs = [arguments["data"], "--outdir=" + outdir]
        _,err = context.exec_run(fastqc, *cmdargs)
        outname = Path(arguments["data"]).stem
        return path.join(outdir, outname + "_fastqc.html"), path.join(outdir, outname + "_fastqc.zip")
    else:
        for r, _, f in os.walk(arguments["data"]):
            for datafile in [os.path.join(r, file) for file in f if file.endswith(".fastq") or file.endswith(".fq")]:
                try:
                    cmdargs = [datafile, "--outdir=" + outdir]
                    _,err = context.exec_run(fastqc, *cmdargs)
                except Exception as err:
                    context.err.append(str(err))

        return outdir, ''