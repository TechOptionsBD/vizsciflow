import os
from os import path

from ....util import Utility
from ...exechelper import func_exec_run


def run_demux(*args, **kwargs):
    paramindex = 0
    barcode = ''
    if 'barcode' in kwargs.keys():
        barcode = kwargs['data']
    else:
        if len(args) > paramindex:
            barcode = args[paramindex]
            paramindex +=1
        
    datas = []
    if 'data' in kwargs.keys():
        datas.append(kwargs['data'])
    else:
        if len(args) == paramindex:
            raise ValueError("Argument missing error in demux.")
        if type(args[paramindex]) is list:
            datas.extend(args[paramindex])
        else:
            datas.append(args[paramindex])
        paramindex +=1
       
    fs = Utility.fs_by_prefix_or_default(datas[0])
    datas = [fs.normalize_path(data) for data in datas]
    
    outdir = ''
    if 'outdir' in kwargs.keys():
        outdir = kwargs['outdir']
    else:
        if len(args) > paramindex:
            outdir = args[paramindex]
            paramindex +=1
    
    if outdir:
        outdir = fs.normalize_path(outdir)
        if not fs.exists(outdir):
            fs.makedirs(outdir)
    else:
        outdir = fs.make_unique_dir(path.dirname(datas[0]) if fs.isfile(datas[0]) else datas[0])
    
    cmdargs = ['-m', 'demux']
    if barcode:
        cmdargs.append(fs.normalize_path(barcode))
                          
    cmdargs.extend(datas)
    olddir = ''
    _err = ''
    try:
        if outdir:
            olddir = os.getcwd()
            os.chdir(outdir)
        _,err = func_exec_run('demultiplex', *cmdargs)
    finally:
        if olddir:
            os.chdir(olddir)
            
    stripped_path = fs.strip_root(outdir)
    if not fs.get_files(outdir):
        raise ValueError("Demultiplexer could not generate the file " + stripped_path + " due to error " + err)
    
    return stripped_path
    