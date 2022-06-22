from os import path
from pathlib import Path

thispath = path.dirname(__file__)

def demo_service(context, *args, **kwargs):
    arguments = context.parse_args('CutAdapt', 'cutadapt', *args, **kwargs)

    data = arguments.pop('data')
    data2 = arguments.pop('data2') if 'data2' in arguments else ''

    cmdargs = " ".join(["-{0[0]} {1}".format(pair[0], str(pair[1])) for pair in arguments.items()])

    outdir = context.createoutdir()
    outputs = []
    if not data2:
        # single-end data
        output =  path.join(outdir, 'trimmed_' + path.basename(data))
        _, err = context.pyvenv_run(thispath, 'cutadapt', '-j 6', data, cmdargs + " -o " + output)
        outputs.append(output)
    else:
        # paired-end data

        # Read 1 with the trimmed and filtered forward reads
        out1 = path.join(outdir, 'out1.fastq')
       
        # Read 2 with the trimmed and filtered reverse reads
        out2 = path.join(outdir, 'out2.fastq')
       
        out, err = context.pyvenv_run(thispath, 'cutadapt', '-j 6', data + " " + data2, cmdargs + " -o " + out1 + " -p " + out2)
        outputs.append(out1)
        outputs.append(out2)
    
    if not path.exists(outputs[0]):
        raise ValueError("CutAdapt could not generate the result file: " + err)

    report = path.join(outdir, Path(data).stem + '_report.html')
   
    text = '<html><pre>' + context.denormalize(outputs[0]) + '</pre></html>'
    with open(report,"w") as file:
        file.write(text)

    outputs.append(report)
    return outputs