from os import path
thispath = path.dirname(__file__)

def demo_service(context, *args, **kwargs):

    arguments = context.parse_args('PycoQC', 'pycoqc', *args, **kwargs)
    output = path.join(context.createoutdir(), 'pycoQC_output.html')

    # context.pyvenv_run(thispath, 'pip install PycoQC --upgrade')
    _, err = context.pyvenv_run(thispath, 'pycoQC', ' -f ' + arguments['data'] + ' -o ' + output)
    
    if not path.exists(output):
        raise ValueError("PycoQC could not generate the result file.: " + err)

    return output