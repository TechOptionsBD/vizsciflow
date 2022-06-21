from os import path
thispath = path.dirname(__file__)

def demo_service(context, *args, **kwargs):
   
    cmdargs = " ".join(["-{0[0]} {1}".format(pair[0], str(pair[1])) for pair in kwargs.items()])

    outdir = context.createoutdir()
    if len(args) < 2:
        # single-end data
        output =  path.join(outdir, 'trimmed_' + args[0].split('/')[-1])
        out, err = context.pyvenv_run(thispath, 'cutadapt -j 6', context.normalize(args[0]), cmdargs + " -o " + output)
   
    else:
        # paired-end data

        # Read 1 with the trimmed and filtered forward reads
        out1 = path.join(outdir, 'out1.fastq')
       
        # Read 2 with the trimmed and filtered reverse reads
        out2 = path.join(outdir, 'out2.fastq')
       
        out, err = context.pyvenv_run(thispath, 'cutadapt -j 6', context.normalize(args[0]) + " " + context.normalize(args[1]), cmdargs + " -o " + out1 + " -p " + out2)
        output = out1
    
    report = context.gettempdir() + '/' + args[0].split("/")[-1].split('.')[0]+ '_report.html'
   
    text = '<html><pre>' + context.denormalize(out) + '</pre></html>'
    file = open(report,"w")
    file.write(text)
    file.close()

    return output, report