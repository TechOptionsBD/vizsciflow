from os import path
from pathlib import Path

thispath = path.abspath(path.dirname(__file__))
            
def demo_service(context, *args, **kwargs):
    fastqc = path.join(thispath, 'bin', 'fastqc')
    
    arguments = context.parse_args('CheckQualityEx', '', *args, **kwargs)
    outdir = context.createoutdir()

    _,err = context.exec_run(fastqc, arguments["data"], f"--outdir={outdir}")
    outname = Path(arguments["data"]).stem
    return path.join(outdir, outname + "_fastqc.html"), path.join(outdir, outname + "_fastqc.zip")