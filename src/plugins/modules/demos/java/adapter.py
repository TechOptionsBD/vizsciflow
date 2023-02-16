from os import path
from pathlib import Path

thispath = path.abspath(path.dirname(__file__))
            
def demo_service(context, *args, **kwargs):
    # sets the path to the external executable
    fastqc = path.join(thispath, 'bin', 'fastqc')
    
    # Parse arguments as given in params in json mapper
    arguments = context.parse_args('CheckQualityEx', 'demo', *args, **kwargs)
    
    # You can create an output directory using context.createoutdir(). context.outdir creates a default one for you.
    outdir = context.outdir

    _,err = context.exec_run(fastqc, arguments["data"], f"--outdir={outdir}")
    outname = Path(arguments["data"]).stem
    # Two files are created by fastqc program in output directory - a html file adding _fastqc.html
    # and a zip file adding _fastqc.zip to the input file's stem. Return these two as specified in 
    # the returns in json mapper
    return path.join(outdir, outname + "_fastqc.html"), path.join(outdir, outname + "_fastqc.zip")