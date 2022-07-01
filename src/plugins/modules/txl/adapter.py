from os import path

thispath = path.abspath(path.dirname(__file__))

def get_txldir(context):
    txldir = path.join(context.gettoolsdir('txl'), 'bin', 'bin')
    #txldir =  context.gettoolsdir('txl')
    if not path.exists(txldir):
        raise ValueError("TXL is not installed. Please install TXL.")
    return txldir

def run_txl(context, *args, **kwargs):
    arguments = context.parse_args('Txl', 'txl', *args, **kwargs)
    txl = path.join(get_txldir(context), 'txl')

    outfilepath = context.createoutfile()
    cmdargs = ['-o '.format(outfilepath), arguments['data']] #"-Dapply"
    if 'txlfile' in arguments.keys() and arguments['txlfile']:
        cmdargs.append(arguments['txlfile'])
    out, err = context.exec_run(txl, *cmdargs, cwd=path.dirname(arguments['data']), env=get_txldir(context))
    return outfilepath