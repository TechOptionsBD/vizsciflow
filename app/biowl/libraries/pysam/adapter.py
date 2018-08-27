import os
import pysam
from pathlib import Path
from os import path
from ....util import Utility

def run_sam_to_bam(*args, **kwargs):
    
    paramindex = 0
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument missing error in pysam.")
        data = args[paramindex]
        paramindex +=1
    
    fs = Utility.fs_by_prefix(data)
    data = fs.normalize_path(data)
    
    output = ''
    if 'output' in kwargs.keys():
        output = kwargs['output']
    else:
        if len(args) > paramindex:
            output = args[paramindex]
    
    if not output:
        output = Path(data).stem + ".bam"
        outdir = fs.make_unique_dir(path.dirname(data))
        output = os.path.join(outdir, path.basename(output))
        
    output = fs.normalize_path(output)
    
    if not fs.exists(path.dirname(output)):
        fs.makedirs(path.dirname(output))
        
    if fs.exists(output):
        fs.remove(output)
               
    infile = pysam.AlignmentFile(data, "r")
    outfile = pysam.AlignmentFile(output, "wb", template=infile)
    for s in infile:
        outfile.write(s)
    
    stripped_path = fs.strip_root(output)
    if not fs.exists(output):
        raise ValueError("pysam could not generate the file: " + stripped_path)
    
    return stripped_path