from os import path
from pathlib import Path
from ...exechelper import func_exec_stdout
from ....util import Utility

seqtk = path.join(path.abspath(path.dirname(__file__)), path.join('bin', 'seqtk'))

def run_seqtk(*args, **kwargs):
    
    fs = Utility.fs_by_prefix_or_default(args[0])
    data = fs.normalize_path(args[0])
    output = fs.normalize_path(args[2])
    
    cmdargs = [args[1]]
    for arg in args[3:]:
        cmdargs.append(arg)
            
    cmdargs.append(data)

    outdata,_ = func_exec_stdout(seqtk, *cmdargs)
    with open(output, 'wb') as f:
        f.write(outdata)
        
    return fs.strip_root(output)

def seqtk_fastq_to_fasta(*args, **kwargs):
    paramindex = 0
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument missing error in pysam.")
        data = args[paramindex]
        paramindex +=1
    
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data)
    
    output = ''
    if 'output' in kwargs.keys():
        output = kwargs['output']
    else:
        if len(args) > paramindex:
            output = args[paramindex]
            paramindex +=1
    
    outdir = ''
    if not output:
        output = Path(data).stem + ".fasta"
        outdir = fs.make_unique_dir(path.dirname(data))
        output = path.join(outdir, path.basename(output))
        
    output = fs.normalize_path(output)
    outdir = path.dirname(output)
    
    if not fs.exists(outdir):
        fs.makedirs(outdir)
        
    if fs.exists(output):
        fs.remove(output)

    cmdargs = [data, 'seq -a', output]
    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)
    return run_seqtk(*cmdargs)

def seqtk_extract_sample(*args, **kwargs):
    paramindex = 0
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument missing error in pysam.")
        data = args[paramindex]
        paramindex +=1
    
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data)
    
    output = ''
    if 'output' in kwargs.keys():
        output = kwargs['output']
    else:
        if len(args) > paramindex:
            output = args[paramindex]
            paramindex +=1
    
    outdir = ''
    if not output:
        p = Path(path.basename(data))
        outdir = fs.make_unique_dir(path.dirname(data))
        output = path.join(outdir, str(p.with_suffix('')) + '_output' + p.suffix)
        
    output = fs.normalize_path(output)
    outdir = path.dirname(output)
    
    if not fs.exists(outdir):
        fs.makedirs(outdir)
        
    if fs.exists(output):
        fs.remove(output)
            
    seed = 100
    if 'seed' in kwargs.keys():
        seed = kwargs['seed']
    else:
        if len(args) > paramindex:
            seed = args[paramindex]
            paramindex += 1
            
    sample = 10000
    if 'sample' in kwargs.keys():
        sample = kwargs['sample']
    else:
        if len(args) > paramindex:
            sample = args[paramindex]
            paramindex += 1
    
    cmdargs = ['sample -s{0}'.format(seed), data, str(sample)]
    
    outdata,_ = func_exec_stdout(seqtk, *cmdargs)
    with open(output, 'wb') as f:
        f.write(outdata)
        
    return fs.strip_root(output)

def seqtk_trim(*args, **kwargs):
    paramindex = 0
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument missing error in pysam.")
        data = args[paramindex]
        paramindex +=1
    
    fs = Utility.fs_by_prefix_or_default(data)
    data = fs.normalize_path(data)
    
    output = ''
    if 'output' in kwargs.keys():
        output = kwargs['output']
    else:
        if len(args) > paramindex:
            output = args[paramindex]
            paramindex +=1
    
    outdir = ''
    if not output:
        p = Path(path.basename(data))
        outdir = fs.make_unique_dir(path.dirname(data))
        output = path.join(outdir, str(p.with_suffix('')) + '_output' + p.suffix)
        
    output = fs.normalize_path(output)
    outdir = path.dirname(output)
    
    if not fs.exists(outdir):
        fs.makedirs(outdir)
        
    if fs.exists(output):
        fs.remove(output)
    
    begin = None
    if 'begin' in kwargs.keys():
        begin = kwargs['begin']
    else:
        if len(args) > paramindex:
            begin = args[paramindex]
            paramindex += 1
    
    end = None
    if 'end' in kwargs.keys():
        end = kwargs['end']
    else:
        if len(args) > paramindex:
            end = args[paramindex]
            paramindex += 1
    
    cmdargs = [data, 'trimfq', output]
    if begin:
        cmdargs.append('-b ' + str(begin))
        
    if end:
        cmdargs.append('-e ' + str(end))
    
    for arg in args[4:]:
        cmdargs.append(arg)
        
    return run_seqtk(*cmdargs)