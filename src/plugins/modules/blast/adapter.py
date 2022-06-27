from os import path
from pathlib import Path

def run_blast(blast, context, *args, **kwargs):
    arguments = context.parse_args('BlastN', 'blast', *args, **kwargs)

    cmdargs = ["-db", arguments['db'], "-query", arguments['query']]

    out, err = context.exec_run(blast, *cmdargs)

    if out:
        report = path.join(context.createoutdir(), "{0}-{1}.{2}".format(Path(arguments['query']).stem, Path(arguments['db']).stem, 'protein-protein.blast.html'))

        text = '<html><pre>' + out + '</pre></html>'
        with open(report, "w") as file:
            file.write(text)
   
        return report
    
    else:
        raise ValueError("Blast didn't run successfully:" + err)

def run_blastn(context, *args, **kwargs):
    blastn = path.join(context.getnormdir(__file__), 'bin', 'blastn')
    return run_blast(blastn, context, *args, **kwargs)

def run_blastp(context, *args, **kwargs):
    blastp = path.join(context.getnormdir(__file__), 'bin', 'blastp')
    return run_blast(blastp, context, *args, **kwargs)