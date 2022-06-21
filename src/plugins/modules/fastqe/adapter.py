from os import path
thispath = path.dirname(__file__)

def demo_service(context, *args, **kwargs):
    outdir = context.createoutdir()
    output = path.join(outdir, args[0].split("/")[-1].split('.')[0]+ '_fastqe.html')
    context.pyvenv_run(thispath, 'fastqe', args[0] + ' --min --max --output=' + output)
    
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