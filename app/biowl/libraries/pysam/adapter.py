import os
import pysam
from pathlib import Path
from os import path
from ....util import Utility

def exec_sam_to_bam(fs, data, output):
    output = fs.normalize_path(output)
    
    if not fs.exists(path.dirname(output)):
        fs.makedirs(path.dirname(output))
        
    if fs.exists(output):
        fs.remove(output)
               
    infile = pysam.AlignmentFile(data, "r")
    outfile = pysam.AlignmentFile(output, "wb", template=infile)
    for s in infile:
        outfile.write(s)
    return output
        
def run_sam_to_bam(*args, **kwargs):
    
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
    
    if fs.isfile(data):
        if not output:
            output = Path(data).stem + ".bam"
            outdir = fs.make_unique_dir(path.dirname(data))
            output = os.path.join(outdir, path.basename(output))
        output = exec_sam_to_bam(fs, data, output)
    else:
        if not output:
            output = fs.make_unique_dir(path.dirname(data))
        
        output = fs.normalize_path(output)
        if fs.isfile(output):
            raise ValueError("File already exists: " + output)
        
        if not fs.exists(output):
            fs.makedirs(output)  
        
        datafiles = []
        for r, _, f in os.walk(data):
            for file in f:
                if file.endswith(".sam"):
                    datafiles.append(os.path.join(r, file))
                    
        for datafile in datafiles:
            try:
                outfile = fs.join(output, Path(datafile).stem + ".bam")
                exec_sam_to_bam(fs, fs.join(data, datafile), outfile)
            except:
                pass
    
    
    stripped_path = fs.strip_root(output)
    if not fs.exists(output):
        raise ValueError("pysam could not generate the file: " + stripped_path)
    
    return stripped_path