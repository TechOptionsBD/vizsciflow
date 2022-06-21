from os import path
thispath = path.dirname(__file__)

def demo_service(context, *args, **kwargs):
    output = path.join(context.createoutdir(), 'pycoQC_output.html')
    context.pyvenv_run(thispath, 'pip install PycoQC --upgrade')
    context.pyvenv_run(thispath, 'pycoQC', '-f ' + args[0] + ' -o ' + output)    
    return output