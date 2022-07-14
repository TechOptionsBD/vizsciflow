from os import path

thispath = path.dirname(__file__)

def dotplot(context, *args, **kwargs):

    dotplot = path.join(thispath, 'bin', 'dotplot.py')
    arguments = context.parse_args('DotPlot', 'CoGe', *args, **kwargs)
    
    output = context.createuniquefile(arguments["dag_file"], 'svg')
    normalize_output = context.normalize(output)

    cmdargs = ["=".join(["--"+key, '"{}"'.format(arguments[key])]) for key in arguments.keys() if arguments[key]] + ["--output=" + normalize_output, "--no-ks"]
    
    out, err = context.pyvenv_run(thispath, "python2", dotplot, *cmdargs)
    
    if err or not path.exists(normalize_output):
        error_msg = "DotPlot could not generate the file {0}.".format(output)
        if err:
            error_msg = "The generated error is: " + err
        raise ValueError(error_msg)

    return output