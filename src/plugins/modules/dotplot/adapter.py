from os import path

thispath = path.dirname(__file__)

def dotplot(context, *args, **kwargs):

    dotplot = path.join(thispath, 'bin', 'dotplot.py')
    arguments = context.parse_args('DotPlot', 'CoGe', *args, **kwargs)
    
    output = context.createuniquefile(arguments["dag_file"], '.svg')

    cmdargs = ["=".join(["--"+key, '"{}"'.format(arguments[key])]) for key in arguments.keys() if arguments[key]] + ["--output=" + output, "--no-ks"]
    print(*cmdargs)
    
    out, err = context.pyvenv_run(thispath, "python2", dotplot, *cmdargs)
    
    if err:
        raise ValueError("DotPlot could not generate the file " + output + " due to error: " + err)

    # from cairosvg import svg2png
    # with open(output, "r") as f:
    #     svg_code = file.read()
    #     print(svg_code)

    # svg2png(bytestring=svg_code,write_to=output)

    return output #+".svg"