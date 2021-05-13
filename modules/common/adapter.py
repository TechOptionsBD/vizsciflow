from app.util import Utility

def raw_print(context, data):
    context.out.append(str(data))

def raw_len(context, data):
    return len(data)

def raw_range(context, start, end):
    return range(start, end)

def raw_read(context, data):
    fs = Utility.fs_type_by_prefix_or_default(data)
    return fs.read(data)

def raw_write(context, data, content):
    fs = Utility.fs_type_by_prefix_or_default(data)
    fs.write(data, content)

def raw_get_files(context, data):
    fs = Utility.fs_type_by_prefix_or_default(data)
    return fs.get_files(data)

def raw_get_folders(context, data):
    fs = Utility.fs_type_by_prefix_or_default(data)
    return fs.get_folders(data)

def raw_remove(context, data):
    fs = Utility.fs_type_by_prefix_or_default(data)
    return fs.remove(data)

def raw_makedirs(context, data):
    fs = Utility.fs_type_by_prefix_or_default(data)
    return fs.makedirs(data)

def raw_isfile(context, data):
    fs = Utility.fs_type_by_prefix_or_default(data)
    return fs.isfile(data)

def raw_dirname(context, data):
    fs = Utility.fs_type_by_prefix_or_default(data)
    return fs.dirname(data)

def raw_getdatatype(context, data):
    fs = Utility.fs_type_by_prefix_or_default(data)
    return fs.getdatatype(data)