from os import path
from pathlib import Path

thispath = path.dirname(__file__)

def gene_order(context, *args, **kwargs):
    
    geneorder = path.join(thispath, 'bin', 'gene_order.py')
    arguments = context.parse_args('GeneOrder', 'CoGe', *args, **kwargs)

    output = path.join(context.createoutdir(), path.basename(arguments["input"]) + ".go")
    input = arguments.pop("input")

    cmdargs = [" ".join(["--"+pair[0], pair[1]]) for pair in arguments.items() if pair[1]]
    stdout, err = context.pyvenv_run(thispath, "python2", geneorder, input, output, *cmdargs)
    
    if err:
        raise ValueError("GeneOrder failed to generate " + output + " due to error: " + err)
    
    return output