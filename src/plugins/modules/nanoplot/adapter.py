from os import path
thispath = path.dirname(__file__)

def demo_service(context, *args, **kwargs):
    arguments = context.parse_args('NanoPlot', 'nanoplot', *args, **kwargs)
    outdir = context.createoutdir()

    # context.pyvenv_run(thispath, 'pip install NanoPlot --upgrade')
    _, err = context.pyvenv_run(thispath, 'NanoPlot', '--fastq ' + arguments['data'] + ' --N50  -o' + outdir)
    
    output = path.join(outdir, 'NanoPlot-report.html')

    if not path.exists(output):
        raise ValueError("NanoPlot could not generate the result file.: " + err)

    return output