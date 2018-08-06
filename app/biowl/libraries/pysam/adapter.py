import os
import pysam
from pathlib import Path
from ....util import Utility

def run_sam_to_bam(*args, **kwargs):
    paramindex = 0
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        if len(args) == paramindex:
            raise ValueError("Argument not given.")
        data = args[paramindex]
        paramindex += 1
    
    data = Utility.get_normalized_path(data)
                
    if 'output' in kwargs.keys():
        output = kwargs['output']
    else:
        if len(args) > paramindex:
            output = args[paramindex]
    
    if output:
        output = Utility.get_normalized_path(output)
    else:
        output = Path(data).stem + ".bam"
        output = os.path.join(os.path.dirname(data), os.path.basename(output))
        output = Utility.get_normalized_path(output)
    
    if os.path.exists(output):
        os.remove(output)
               
    infile = pysam.AlignmentFile(data, "r")
    outfile = pysam.AlignmentFile(output, "wb", template=infile)
    for s in infile:
        outfile.write(s)
    
    fs = Utility.fs_by_prefix(output)
    stripped_path = fs.strip_root(output)
    if not os.path.exists(output):
        raise ValueError("pysam could not generate the file " + stripped_path)
    
    return stripped_path