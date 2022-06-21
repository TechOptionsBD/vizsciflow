from os import path
thispath = path.dirname(__file__)

def demo_service(context, *args, **kwargs):
    context.pyvenv_run(thispath, 'pip install NanoPlot --upgrade')
    output = path.join(context.createoutdir() + '/' + args[0].split("/")[-1].split('.')[0] + '_nanoplot')

    out, err = context.pyvenv_run(thispath, 'NanoPlot', ' --fastq ' + args[0] + ' --N50 -o ' + output)    
    return output + '/NanoPlot-report.html'