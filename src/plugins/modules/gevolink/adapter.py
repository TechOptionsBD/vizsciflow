from os import path
from pathlib import Path

thispath = path.dirname(__file__)

def gevo_link(context, *args, **kwargs):
    
    gevolink = path.join(context.getnormdir(__file__), 'bin', 'gevolinks.pl')
    
    arguments = context.parse_args('GevoLink', 'CoGe', *args, **kwargs)
    infile = arguments.pop("data")
    outdir = path.join(context.createoutdir(), path.basename(infile))

    cmdargs = ["--infile", infile] + ["--"+key + " " + arguments[key] for key in arguments.keys() if arguments[key]] + ["--outfile", outdir]
    _, err = context.pyvenv_run(thispath, "perl", gevolink, *cmdargs)

    gevo = outdir + ".gevolinks"
    condensed = outdir + ".condensed"

    if err or not (path.exists(gevo) and path.exists(condensed)):
        error_msg = "GevoLink could not generate the files {0}, {1}".format(gevo, condensed)
        if err:
            error_msg = "The generated error is: " + err
        raise ValueError(error_msg)

    return (gevo, condensed)