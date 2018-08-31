import os
from os import path
from ...exechelper import func_exec_run
from ....util import Utility

flash = path.join(path.dirname(path.abspath(__file__)), path.join('bin', 'flash'))

# FLASH (Fast Length Adjustment of SHort reads) is a very fast and accurate software tool 
# to merge paired-end reads from next-generation sequencing experiments. FLASH is designed 
# to merge pairs of reads when the original DNA fragments are shorter than twice the 
# length of reads. The resulting longer reads can significantly improve genome assemblies. 
# They can also improve transcriptome assembly when FLASH is used to merge RNA-seq data.
def run_flash(*args, **kwargs):
    paramindex = 0
    if 'data' in kwargs.keys():
        data1 = kwargs['data']
    else:
        if len(args) <= paramindex:
            raise ValueError("Argument missing error in Flash.")
        data1 = args[paramindex]
        paramindex +=1
    
    fs = Utility.fs_by_prefix_or_default(data1)
    data1 = fs.normalize_path(data1)
    
    if 'data2' in kwargs.keys():
        data2 = kwargs['data2']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument missing error in Flash.")
        data2 = args[paramindex]
        paramindex +=1
    
    data2 = fs.normalize_path(data2)
    
    outdir = ''
    if 'outdir' in kwargs.keys():
        outdir = kwargs['outdir']
    else:
        if len(args) > paramindex:
            outdir = args[paramindex]
            paramindex +=1
            
    if outdir:
        outdir = fs.normalize_path(outdir)
    else:
        outdir = fs.make_unique_dir(path.dirname(data1))
    
    if not fs.exists(outdir):
        fs.makedirs(outdir)
    
    max_overlap = 50
    if 'max_overlap' in kwargs.keys():
        max_overlap = kwargs['max_overlap']
    else:
        if len(args) > paramindex:
            max_overlap = args[paramindex]
            paramindex +=1
                        
    cmdargs = ["-d {0}".format(outdir), " -M {0}".format(max_overlap)]

    for arg in args[paramindex + 1:]:
        cmdargs.append(arg)
            
    cmdargs.append(data1)
    cmdargs.append(data2)

    _, err = func_exec_run(flash, *cmdargs)
    
    extended_frags = path.join(outdir, 'out.extendedFrags.fastq')    
    if not fs.exists(extended_frags):
        raise ValueError("Flash operation failed due to error: " + err)
    return fs.strip_root(extended_frags)

def run_flash_recursive(*args, **kwargs):
    
    paramindex = 0
    indir = ''
    if 'indir' in kwargs.keys():
        indir = kwargs['indir']
    else:
        if len(args) <= paramindex:
            raise ValueError("Argument missing error in Flash.")
        indir = args[paramindex]
        paramindex +=1
    
    fs = Utility.fs_by_prefix_or_default(indir)
    indir = fs.normalize_path(indir)    
    
    outdir = ''
    if 'outdir' in kwargs.keys():
        indir = kwargs['outdir']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument missing error in Flash.")
        indir = args[paramindex]
        paramindex +=1
        
    max_overlap = 50
    if 'max_overlap' in kwargs.keys():
        max_overlap = kwargs['max_overlap']
    else:
        if len(args) > paramindex:
            max_overlap = args[paramindex]
            paramindex +=1
    
    if outdir:
        outdir = fs.normalize_path(outdir)
    else:
        outdir = fs.make_unique_dir(path.dirname(indir))
    
    log_path = path.join(outdir, "log")
    
    if not fs.exists(outdir):
        fs.makedirs(outdir) 
    
    if not fs.exists(log_path): 
        fs.makedirs(log_path) 

    #create list of filenames 
    filenames = next(os.walk(indir))[2] 
    filenames.sort() 
    
    #divide forward and reverse read files into sepeate lists 
    R1 = list() 
    R2 = list() 

    for files1 in filenames[::2]: 
        R1.append(files1)  
    
    for files2 in filenames[1:][::2]: 
        R2.append(files2) 
    
    #iterate through filenames and call Flash joining  
    
    if len(R1) != len(R2):
        raise ValueError("R1 and R2 different lengths")
    
    for i in range(len(R1)):
        if R1[i][:-12] == R2[i][:-12]:
            args = []
            args.append(" -M " + str(max_overlap))
            args.append(" -d " + outdir)
            args.append(" -o " + R1[i][:-12])
            args.append(indir + R1[i])
            args.append(indir + R2[i])
            output,_ = func_exec_run(flash, *args)
            
            output_file = path.join(log_path, R1[i][:-12] + ".flash.log")
            
            with open(output_file, 'a+') as f:
                f.write(output)
    
    return log_path