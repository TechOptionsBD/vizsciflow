import os
from os import path, rename
from pathlib import Path
from app.util import Utility

thispath = path.abspath(path.dirname(__file__))
nicaddirname = 'bin'
nicad = path.join(thispath, nicaddirname, 'nicad6')
nicadcross = path.join(thispath, nicaddirname, 'nicad6cross')

def get_txldir(context):
    txldir = path.join(context.gettoolsdir('txl'), 'bin', 'bin')
    if not path.exists(txldir):
        raise ValueError(f"TXL bin directory does not exist.")
    return txldir

def get_nicaddir(context):
    nicaddir = path.join(context.gettoolsdir('nicad'), nicaddirname)
    if not path.exists(nicaddir):
        raise ValueError(f"NiCad bin directory does not exist.")
    return nicaddir

def get_gransuffix(granularity):
    return '_' + granularity + '.xml'

def get_scriptpath(context, script):
    scriptdir = path.join(get_nicaddir(context), 'scripts', script)
    if not path.exists(scriptdir):
        raise ValueError(f"NiCad script directory does not exist.")
    return scriptdir

def get_output(data, suffix, out):
    system = Path(data).stem + suffix # + '.xml'
    output = path.join(path.dirname(data), system)

    if not os.path.exists(output):
        raise ValueError("Tool {0} returns error: {1}".format('Nicad', out))
    
    return output

def run_nicad(context, *args, **kwargs):
    arguments = context.parse_args('nicad', 'nicad', *args, **kwargs)

    cmdargs = [arguments['granularity'], arguments['language'], arguments['data'], 'default-report']
    out, err = context.exec_run(nicad, *cmdargs, cwd=get_nicaddir(context), env=get_txldir(context))
    return get_output(arguments['data'], get_gransuffix(arguments['granularity']), out)
    
def run_nicadcross(context, *args, **kwargs):
    arguments = context.parse_args('nicad', 'nicadcross', *args, **kwargs)
    cmdargs = [arguments['granularity'], arguments['language'], arguments['data'], arguments['data2'], 'default-report']

    out, err = context.exec_run(nicadcross, *cmdargs, cwd=get_nicaddir(context), env=get_txldir(context))
    output = get_output(arguments['data'], get_gransuffix(arguments['granularity']), out)
    output2 = path.join(path.dirname(arguments['data2']), Path(arguments['data2']).stem + get_gransuffix(arguments['granularity']))

    return output, output2

def run_extract(context, *args, **kwargs):
    script = get_scriptpath(context, 'Extract')

    arguments = context.parse_args('extract', 'nicad', *args, **kwargs)

    cmdargs = [arguments['granularity'], arguments['language'], arguments['data']]
    if 'select' in arguments.keys() and arguments['select']:
        cmdargs.append(arguments['select'] if arguments['select'] else 'none')
    if 'ignore' in arguments.keys():
        # if 'select' not in arguments.keys():
        #     cmdargs.append("''")
        cmdargs.append(arguments['ignore'] if arguments['ignore'] else 'none')

    out, err, exit_code = context.bash_run_out_err_exit(script, *cmdargs, cwd=get_nicaddir(context), env=get_txldir(context))
    context.save_stdout_stderr(out, err)
    
    if Utility.ValueOrNone(exit_code) >= 99:
        raise ValueError("ERROR: Extraction failed, code {0}".format(out))

    return get_output(arguments['data'], get_gransuffix(arguments['granularity']), out)

def run_transform(context, *args, **kwargs):
    script = get_scriptpath(context, 'Transform')

    arguments = context.parse_args('transform', 'nicad', *args, **kwargs)
    cmdargs = [arguments['granularity'], arguments['language'], arguments['data'], arguments['transform']]
    out, err, exit_code = context.bash_run_out_err_exit(script, *cmdargs, cwd=get_nicaddir(context), env=get_txldir(context))
    
    context.save_stdout_stderr(out, err)
    
    if Utility.ValueOrNone(exit_code) != 0:
        raise ValueError("ERROR: Transformation failed, code {0}".format(out))

    return get_output(arguments['data'], '-transform.xml', out)

def run_rename(context, *args, **kwargs):

    script = get_scriptpath(context, 'Rename')

    arguments = context.parse_args('rename', 'nicad', *args, **kwargs)
    cmdargs = [arguments['granularity'], arguments['language'], arguments['data'], arguments['renaming']]
    
    out, err, exit_code = context.bash_run_out_err_exit(script, *cmdargs, cwd=get_nicaddir(context), env=get_txldir(context))
    context.save_stdout_stderr(out, err)
    
    if Utility.ValueOrNone(exit_code) != 0:
        raise ValueError("ERROR: Renaming failed, code {0}".format(out))

    return get_output(arguments['data'], '-{0}.xml'.format(arguments['renaming']), out)

def run_filter(context, *args, **kwargs):

    script = get_scriptpath(context, 'Filter')

    arguments = context.parse_args('filter', 'nicad', *args, **kwargs)
    cmdargs = [arguments['granularity'], arguments['language'], arguments['data']]
    if 'nonterminals' in arguments.keys():
        cmdargs.append(arguments['nonterminals'])
    
    out, err, exit_code = context.bash_run_out_err_exit(script, *cmdargs, cwd=get_nicaddir(context), env=get_txldir(context))
    context.save_stdout_stderr(out, err)

    if Utility.ValueOrNone(exit_code) != 0:
        raise ValueError("ERROR: Failed failed, code {0}".format(out))

    return get_output(arguments['data'], '-filter.xml', out)

def run_abstract(context, *args, **kwargs):
    script = get_scriptpath(context, 'Abstract')

    arguments = context.parse_args('abstract', 'nicad', *args, **kwargs)
    cmdargs = [arguments['granularity'], arguments['language'], arguments['data']]
    if 'nonterminals' in arguments.keys():
        cmdargs.append(arguments['nonterminals'])
    
    out, err, exit_code = context.bash_run_out_err_exit(script, *cmdargs, cwd=get_nicaddir(context), env=get_txldir(context))
    context.save_stdout_stderr(out, err)

    if Utility.ValueOrNone(exit_code) != 0:
        raise ValueError("ERROR: Abstraction failed, code {0}".format(out))

    return get_output(arguments['data'], '-abstract.xml', out)

def run_normalize(context, *args, **kwargs):

    script = get_scriptpath(context, 'Normalize')

    arguments = context.parse_args('normalize', 'nicad', *args, **kwargs)
    cmdargs = [arguments['granularity'], arguments['language'], arguments['data'], arguments['normalizer']]
    
    out, err, exit_code = context.bash_run_out_err_exit(script, *cmdargs, cwd=get_nicaddir(context), env=get_txldir(context))
    context.save_stdout_stderr(out, err)

    if Utility.ValueOrNone(exit_code) != 0:
        raise ValueError("ERROR: Normalization failed, code {0}".format(out))

    return get_output(arguments['data'], '-normalized.xml', out)


def run_cleanall(context, *args, **kwargs):

    script = get_scriptpath(context, 'CleanAllQuiet')

    arguments = context.parse_args('cleanall', 'nicad', *args, **kwargs)
    cmdargs = [arguments['data']]
    out, err, exit_code = context.bash_run_out_err_exit(script, *cmdargs, cwd=get_nicaddir(context), env=get_txldir(context))
    context.save_stdout_stderr(out, err)

    return arguments['data']

def run_findclonepairs(context, *args, **kwargs):

    script = get_scriptpath(context, 'FindClonePairs')

    arguments = context.parse_args('findclonepairs', 'nicad', *args, **kwargs)
    cmdargs = [arguments['data'], arguments['threshold']]
    
    if 'minclonesize' in arguments.keys():
        cmdargs.append(arguments['minclonesize'])

        if 'maxclonesize' in arguments.keys():
            cmdargs.append(arguments['maxclonesize'])
    
        if 'showsource' in arguments.keys() and arguments['showsource'] and arguments['showsource'].lower() != 'none':
            cmdargs.append('showsource')

    out, err, exit_code = context.bash_run_out_err_exit(script, *cmdargs, cwd=get_nicaddir(context), env=get_txldir(context))
    context.save_stdout_stderr(out, err)

    if Utility.ValueOrNone(exit_code) != 0:
        raise ValueError("ERROR: Clone analysis failed, code {0}".format(out))

    resultdirname = Path(arguments['data']).stem + '-clones' # output saved into this folder
    outname = resultdirname + '-' + str(arguments['threshold']) + '.xml'
    return path.join(path.dirname(arguments['data']), resultdirname, outname)

def run_clusterpairs(context, *args, **kwargs):

    script = get_scriptpath(context, 'ClusterPairs')

    arguments = context.parse_args('clusterpairs', 'nicad', *args, **kwargs)
    cmdargs = [arguments['data']]

    out, err, exit_code = context.bash_run_out_err_exit(script, *cmdargs, cwd=get_nicaddir(context), env=get_txldir(context))
    context.save_stdout_stderr(out, err)

    if Utility.ValueOrNone(exit_code) != 0:
        raise ValueError(f"ERROR: Clustering failed, code {exit_code}")

    return get_output(arguments['data'], '-classes.xml', out)

def run_getsource(context, *args, **kwargs):

    script = get_scriptpath(context, 'GetSource')
    arguments = context.parse_args('getsource', 'nicad', *args, **kwargs)
    cmdargs = [arguments['data']]
    
    out, err, exit_code = context.bash_run_out_err_exit(script, *cmdargs, cwd=get_nicaddir(context), env=get_txldir(context))
    context.save_stdout_stderr(out, err)

    if Utility.ValueOrNone(exit_code) != 0:
        raise ValueError("ERROR: Get sources failed, code {0}".format(out))

    return get_output(arguments['data'], '-withsource.xml', out)

def run_getnormsource(context, *args, **kwargs):

    script = get_scriptpath(context, 'GetNormSource')

    arguments = context.parse_args('getnormsource', 'nicad', *args, **kwargs)
    cmdargs = [arguments['data'], arguments['data2']]
    out, err, exit_code = context.bash_run_out_err_exit(script, *cmdargs, cwd=get_nicaddir(context), env=get_txldir(context))
    context.save_stdout_stderr(out, err)

    if Utility.ValueOrNone(exit_code) != 0:
        raise ValueError("ERROR: Get normalized sources failed, code {0}".format(out))
    return get_output(arguments['data'], '-normsource.xml', out)

def run_makepairhtml(context, *args, **kwargs):

    script = get_scriptpath(context, 'MakePairHTML')
    arguments = context.parse_args('makepairhtml', 'nicad', *args, **kwargs)
    cmdargs = [arguments['data']]
    out, err, exit_code = context.bash_run_out_err_exit(script, *cmdargs, cwd=get_nicaddir(context), env=get_txldir(context))
    context.save_stdout_stderr(out, err)

    if Utility.ValueOrNone(exit_code) != 0:
        raise ValueError("ERROR: Get Make HTML failed, code {0}".format(out))
    return get_output(arguments['data'], '.html', out)

def run_splitclasses(context, *args, **kwargs):

    script = get_scriptpath(context, 'SplitClasses')

    arguments = context.parse_args('splitclasses', 'nicad', *args, **kwargs)
    cmdargs = [arguments['data']]
    
    out, err, exit_code = context.bash_run_out_err_exit(script, *cmdargs, cwd=get_nicaddir(context), env=get_txldir(context))
    context.save_stdout_stderr(out, err)

    if Utility.ValueOrNone(exit_code) != 0:
        raise ValueError("ERROR: Get Make HTML failed, code {0}".format(out))
    return get_output(arguments['data'], '', out)

def run_findclones(context, *args, **kwargs):

    script = get_scriptpath(context, 'FindClones')

    arguments = context.parse_args('findclones', 'nicad', *args, **kwargs)
    cmdargs = [arguments['data'], arguments['threshold']]
    
    if 'minclonesize' in arguments.keys():
        cmdargs.append(arguments['minclonesize'])

        if 'maxclonesize' in arguments.keys():
            cmdargs.append(arguments['maxclonesize'])
    
        if 'showsource' in arguments.keys():
            cmdargs.append('showsource')


    out, err, exit_code = context.bash_run_out_err_exit(script, *cmdargs, cwd=get_nicaddir(context), env=get_txldir(context))
    context.save_stdout_stderr(out, err)

    if Utility.ValueOrNone(exit_code) != 0:
        raise ValueError("ERROR: Find clones failed, code {0}".format(out))

    resultdirname = Path(arguments['data']).stem + '-clones' # output saved into this folder
    outname = resultdirname + '-' + str(arguments['threshold']) + '.xml'
    return path.join(path.dirname(arguments['data']), resultdirname, outname)