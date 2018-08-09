from os import path
from pathlib import Path
from ...exechelper import func_exec_stdout
from ....util import Utility

seqtk = path.join(path.abspath(path.dirname(__file__)), path.join('bin', 'seqtk'))

def run_seqtk(*args, **kwargs):
    
    fs = Utility.fs_by_prefix(args[0])
    data = fs.normalize_path(args[0])
    output = fs.normalize_path(args[1])
    
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
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument not given.")
        data = args[paramindex]
        paramindex += 1
    
    output = ''            
    if 'output' in kwargs.keys():
        output = kwargs['output']
    else:
        if len(args) > paramindex:
            output = args[paramindex]
            paramindex += 1

    cmdargs = [data, 'seq -a', output]
    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)
    return run_seqtk(*cmdargs)

def seqtk_extract_sample(*args, **kwargs):
    paramindex = 0
    data = ''
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument not given.")
        data = args[paramindex]
        paramindex += 1
    
    output = ''            
    if 'output' in kwargs.keys():
        output = kwargs['output']
    else:
        if len(args) > paramindex:
            output = args[paramindex]
            paramindex += 1
    
    if not output:
        filename = Path(path.basename(data))
        output = path.join(path.dirname(data), filename.with_suffix('') + '_output.' + filename.suffix())
        
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
    
    fs = Utility.fs_by_prefix(data)
    data = fs.normalize_path(data)
    output = fs.normalize_path(output)
    
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
            raise ValueError("Argument not given.")
        data = args[paramindex]
        paramindex += 1
                
    if 'output' in kwargs.keys():
        output = kwargs['output']
    else:
        if len(args) > paramindex:
            output = args[paramindex]
            paramindex += 1
    
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
    
    fs = Utility.fs_by_prefix(data)
    data = fs.normalize_path(data)
    output = fs.normalize_path(output)
            
    cmdargs = [data, 'trimfq', output]
    if begin:
        cmdargs.append('-b ' + str(begin))
        
    if end:
        cmdargs.append('-e ' + str(end))
    
    for arg in args[4:]:
        cmdargs.append(arg)
        
    return run_seqtk(*cmdargs)