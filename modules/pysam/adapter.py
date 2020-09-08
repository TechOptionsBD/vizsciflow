import os
import pysam
from pathlib import Path

from dsl.fileop import FolderItem
from app.biowl.argshelper import get_posix_data_args, get_posix_output_args, get_posix_output_folder_args

def exec_sam_to_bam(fs, data, output):

    if not fs.exists(fs.dirname(output)):
        fs.makedirs(fs.dirname(output))

    if fs.exists(output):
        ext = Path(output).suffix
        if ext:
            ext = ext[1:] # remove the .
        output = fs.unique_filename(fs.dirname(output), Path(output).stem, ext)
           
    infile = pysam.AlignmentFile(data, "r")
    outfile = pysam.AlignmentFile(fs.normalize_path(output), "wb", template=infile)
    for s in infile:
        outfile.write(s)
    return output
        
def run_sam_to_bam(context, *args, **kwargs):
    
    paramindex, data, fs = get_posix_data_args(0, 'data', context, *args, **kwargs)
    output = get_posix_output_args(paramindex, 'output', fs, data, context, ".bam", *args, **kwargs) if fs.isfile(data) else get_posix_output_folder_args(paramindex, 'output', fs, context, *args, **kwargs)
    
    if fs.isfile(data):
        output = exec_sam_to_bam(fs, data, output)
    else:
        for r, _, f in os.walk(data):
            for datafile in [os.path.join(r, file) for file in f if file.endswith(".sam")]:
                try:
                    output = exec_sam_to_bam(fs, datafile, output)
                except Exception as err:
                    context.err.append(str(err))
    
    stripped_path = fs.strip_root(output)
    if not fs.exists(output):
        raise ValueError("pysam could not generate the file: " + stripped_path)
    
    return FolderItem(stripped_path)