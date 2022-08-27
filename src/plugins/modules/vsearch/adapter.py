from os import path

from app.system.exechelper import func_exec_run
from app.dsl.argshelper import get_posix_data_args, get_posix_output_folder_args

vsearch = path.join(path.abspath(path.dirname(__file__)), path.join('bin', 'usearch10.0.240_i86linux32'))

def run_usearch(context, *args, **kwargs):
    paramindex = 0
    command = args[paramindex]
    paramindex, data, fs = get_posix_data_args(paramindex, 'data', context, *args, **kwargs)
    if not fs.exists(data):
        raise ValueError("Input file {0} doesn't exist.".format(fs.strip_root(str(data))))

    cmdargs = ["-" + command, data]
    outtype = args[2] if len(args) > 2 else 'fasta'
    cmdargs.append('-{0}out'.format(outtype))
    outdir = get_posix_output_folder_args(paramindex, 'output', fs, context, *args, **kwargs)
    outpath = fs.join(outdir, 'output.fasta' if outtype == 'fasta' else 'output.fastq') 

    for arg in args[4:]:
        cmdargs.append('-' + arg)
    
    _,err = func_exec_run(vsearch, *cmdargs)
    
    stripped_path = fs.strip_root(outpath)
    if not fs.exists(outpath):
        raise ValueError("FastQC could not generate the file " + stripped_path + " due to error " + err)

    return stripped_path
    