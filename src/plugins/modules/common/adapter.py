from app.util import Utility
from src.dsl.fileop import FolderItem, FilterManager

def raw_print(context, data):
    context.out.append(str(data))

def raw_len(context, data):
    return len(data)

def raw_range(context, start, end):
    return range(start, end)

def raw_read(context, data):
    fs = Utility.fs_by_prefix_or_guess(data)
    return fs.read(data)

def raw_write(context, data, content):
    fs = Utility.fs_by_prefix_or_guess(data)
    fs.write(data, content)

def raw_get_files(context, *args, **kwargs):
    arguments = context.parse_args('GetFiles', 'io', *args, **kwargs)
    fs = Utility.fs_by_prefix_or_guess(arguments["data"])
    return fs.get_files(arguments["data"], arguments["pattern"], arguments["recursive"])

def raw_get_folders(context, *args, **kwargs):
    arguments = context.parse_args('GetFolders', 'io', *args, **kwargs)
    fs = Utility.fs_by_prefix_or_guess(arguments["data"])
    return fs.get_folders(arguments["data"], arguments["pattern"], arguments["recursive"])

def raw_remove(context, data):
    fs = Utility.fs_by_prefix_or_guess(data)
    return fs.remove(data)

def raw_makedirs(context, data):
    fs = Utility.fs_by_prefix_or_guess(data)
    return fs.makedirs(data)

def raw_isfile(context, data):
    fs = Utility.fs_by_prefix_or_guess(data)
    return fs.isfile(data)

def raw_dirname(context, data):
    fs = Utility.fs_by_prefix_or_guess(data)
    return fs.dirname(data)

def raw_getdatatype(context, data):
    fs = Utility.fs_by_prefix_or_guess(data)
    return fs.getdatatype(data)

def raw_int(context, *args, **kwargs):
    return int(args[0])

def raw_str(context, *args, **kwargs):
    return str(args[0])

def raw_float(context, *args, **kwargs):
    return float(args[0])

def raw_extract(context, *args, **kwargs):
    import os
    import uuid
    from os import path
    from app.dsl.argshelper import get_optional_input_from_args, get_posix_data_args

    paramindex, data, fs = get_posix_data_args(0, 'data', context, *args, **kwargs)
    paramindex, lines = get_optional_input_from_args(paramindex, 'lines', *args, **kwargs)
    paramindex, start = get_optional_input_from_args(paramindex, 'start', *args, **kwargs)

    # default values, get from func.params  TODO
    lines = int(lines) if lines else 10
    start = int(start) if start else 0

    outpath = path.join(path.dirname(path.dirname(path.dirname(__file__))), 'storage/output', str(context.task_id))
    if not os.path.exists(outpath):
        os.makedirs(outpath)

    outpath = path.join(outpath, str(uuid.uuid4()))
    with open(data, 'rt') as srcfile:
        if lines < 0:
            start = lines
            while next(srcfile, -1) == -1:
                start += 1
            lines = abs(lines)
            if start < 0:
                lines += start
                start = 0
                
        srcfile.seek(0)
        for _ in range(start):
            next(srcfile)
        with open(outpath, 'w') as outfile:
            for _ in range(start, lines):
                value= next(srcfile, -1)
                if value == -1:
                    break
                outfile.write(value)
                    

    stripped_html_path = fs.strip_root(outpath)
    if not fs.exists(outpath):
        raise ValueError("Extract could not generate the file " + stripped_html_path)

    return outpath

def raw_joinpath(context, *args, **kwargs):
    fs = Utility.fs_by_prefix_or_guess(args[0])
    return fs.join(args[0], args[1])