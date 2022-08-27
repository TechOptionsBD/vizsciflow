import os
from os import path
from app.system.exechelper import func_exec_run
from app.util import Utility

flash = path.join(path.dirname(path.abspath(__file__)), path.join('bin', 'flash'))

# FLASH (Fast Length Adjustment of SHort reads) is a very fast and accurate software tool 
# to merge paired-end reads from next-generation sequencing experiments. FLASH is designed 
# to merge pairs of reads when the original DNA fragments are shorter than twice the 
# length of reads. The resulting longer reads can significantly improve genome assemblies. 
# They can also improve transcriptome assembly when FLASH is used to merge RNA-seq data.
def run_flash(context, *args, **kwargs):

    arguments = context.parse_args('flash', 'Merge', *args, **kwargs)
    
    outdir = context.createoutdir()
    
    cmdargs = ["-d {0}".format(outdir), " -M {0}".format(arguments['max_overlap']), arguments['data'], arguments['data2']]

    _, err = context.exec_run(flash, *cmdargs)
    
    extended_frags = path.join(outdir, 'out.extendedFrags.fastq')    
    if not path.exists(extended_frags):
        raise ValueError("Flash operation failed due to error: " + err)
    return extended_frags

def run_flash_recursive(context, *args, **kwargs):
    
    arguments = context.parse_args('flash', 'MergeR', *args, **kwargs)
    outdir = context.createoutdir()
    
    log_path = path.join(outdir, "log")
    
    if not path.exists(log_path): 
        os.makedirs(log_path) 

    #create list of filenames 
    filenames = next(os.walk(arguments['data']))[2] 
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
            args.append(" -M " + str(arguments['max_overlap']))
            args.append(" -d " + outdir)
            args.append(" -o " + R1[i][:-12])
            args.append(path.join(arguments['data'], R1[i]))
            args.append(path.join(arguments['data'], R2[i]))
            output,_ = context.exec_run(flash, *args)
            
            output_file = path.join(log_path, R1[i][:-12] + ".flash.log")
            
            with open(output_file, 'a+') as f:
                f.write(output)
    
    return log_path