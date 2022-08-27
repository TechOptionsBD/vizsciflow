import os
from os import path
from pathlib import Path

thispath = path.dirname(__file__)

def run_cutadapt(context, *args, **kwargs):
    """
    Remove adapter sequences from high-throughput sequencing reads
    """

    arguments = context.parse_args('CutAdapt', 'cutadapt', *args, **kwargs)

    data = arguments.pop('data')
    data2 = arguments.pop('data2') if 'data2' in arguments else ''

    cmdargs = ["-{0[0]} {1}".format(pair[0], str(pair[1])) for pair in arguments.items()]

    outdir = context.createoutdir()
    outputs = []
    out = None

    if not data2:
        # Process single-end data
        output = path.join(outdir, 'trimmed_' + path.basename(data))

        # run cutadapt and send trimmed data to output file
        out, err = context.pyvenv_run(thispath, 'cutadapt', '-j 8', data, *cmdargs, "-o", output)
        outputs.append(output)

    else:
        # Process paired-end data

        # Read 1 with the trimmed and filtered forward reads
        out1 = path.join(outdir, 'trimmed_' + path.basename(data))
       
        # Read 2 with the trimmed and filtered reverse reads
        out2 = path.join(outdir, 'trimmed_' + path.basename(data2))
       
        out, err = context.pyvenv_run(thispath, 'cutadapt', " ".join(['-j 8', data, data2]), *cmdargs, "-o" + out1 + " -p " + out2)

        outputs.append(out1)
        outputs.append(out2)
    
    if not path.exists(outputs[0]):
        raise ValueError("CutAdapt could not generate the result file: " + err)

    if out:
        # Cutadapt send summary report to stdout. Write this to .txt file to display
        report = path.join(outdir, Path(data).stem + '_report.html')

        text = '<html><pre>' + out + '</pre></html>'
        with open(report, "w") as file:
            file.write(text)
        
        outputs.append(report)

    return outputs