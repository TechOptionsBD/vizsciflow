from os import path

thispath = path.abspath(path.dirname(__file__))

def dag_chainer(context, *args, **kwargs):
    dagchainer = path.join(thispath, 'bin', 'dag_chainer.py')
    arguments = context.parse_args('DagChainer', 'CoGe', *args, **kwargs)

    # Map cmdarg to tool options
    options = {'dag': '-i', 'gap_init': '-o', 'gap_extend': '-e', 'min_score': '-x', 
    'gap_dist': '-g', 'gap_max': '-D', 'e_value': '-E', 'min_aligned_pairs': '-A'}

    output = path.join(context.createoutdir(), path.basename(arguments["dag"]) + ".aligncoords")

    cmdargs = [" ".join([options[key], str(arguments[key])]) for key in arguments.keys() if arguments[key]]
    stdout, log = context.pyvenv_run(thispath, "python2", dagchainer, *cmdargs)
    
    if log:
        # display log report
        context.out.append("DAGChainer log:\n" + str(log))
    
    with open(output, "w") as file:
        # write stdout to output file
        file.write(stdout)
    
    return output