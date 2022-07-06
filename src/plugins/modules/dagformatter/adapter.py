from os import path
from pathlib import Path

thispath = path.dirname(__file__)

def demo_service(context, *args, **kwargs):
    
    dagtool = path.join(thispath, 'dag_tools.py')
    arguments = context.parse_args('DAGFormatter', 'CoGe', *args, **kwargs)

    
    outdir = path.join(context.createoutdir(), Path(arguments["blast_file"]).stem + ".dag.all")

    cmdargs = ["=".join(["--"+pair[0], pair[1]]) for pair in arguments.items()] + ["-c"]
    stdout, err = context.pyvenv_run(thispath, "python", dagtool, *cmdargs)
    
    if err:
        raise ValueError("DAGFormatter failed to generate " + outdir + " due to error: " + err)
    
    with open(outdir, "w") as file:
		# write stdout to output file
        file.write(stdout)
    
    return outdir