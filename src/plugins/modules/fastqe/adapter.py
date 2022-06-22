from os import path
from pathlib import Path

thispath = path.dirname(__file__)

def demo_service(context, *args, **kwargs):
    
    arguments = context.parse_args('FastQE', 'fastqc', *args, **kwargs)
    
    outdir = context.createoutdir()
    output = path.join(outdir, Path(arguments['data']).stem + "_fastqe.html")
    _, err = context.pyvenv_run(thispath, 'fastqe', arguments['data'] + ' --min --max --output=' + output)
    
    if not path.exists(output):
        raise ValueError("FastQE could not generate the result file: " + err)

    f = open(output, 'r+')
    emoji = f.read()
   
    html = '''<!DOCTYPE html>
    <html lang="en", style="font-size:25px">
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <h6>
    '''

    html += emoji
    html += '''    </h6>
    </body>
    </html>'''
   
    f.seek(0)
    f.write(html)
    f.close()
   
    return output