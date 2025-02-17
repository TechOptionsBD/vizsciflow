import os
import sys
import stat
import logging
import subprocess
from pathlib import Path
from itertools import chain
from collections.abc import Iterable

def flatten(coll):
    for i in coll:
            if isinstance(i, Iterable) and not isinstance(i, str):
                for subc in flatten(i):
                    yield subc
            else:
                yield i

def func_exec_stdout(app, *args):
    try:
        if not os.access(app, os.X_OK):
            st = os.stat(app)
            os.chmod(app, st.st_mode | stat.S_IEXEC) #  st.st_mode | 0111 for all
    except:
        pass
    # cmd = app
    # if args:
    #     cmd += ' ' + ' '.join(str(arg) for arg in args)
    #p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #return p.stdout, p.stderr
    args = flatten(args)
    cmd = [str(arg) for arg in args]
    out, err = subprocess.Popen([app, *cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    return out, err

def py_exec_out_err_exit(app, *args):
    if not os.access(app, os.X_OK):
        st = os.stat(app)
        os.chmod(app, st.st_mode | stat.S_IEXEC) #  st.st_mode | 0111 for all
    # cmd = app
    # if args:
    #     cmd += ' ' + ' '.join(str(arg) for arg in args)
    #p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #return p.stdout, p.stderr
    args = flatten(args)
    cmd = [str(arg) for arg in args]
    proc = subprocess.run(['python', app, *cmd],  capture_output=True, text = True)
    return proc.stdout, proc.stderr, proc.returncode

def func_exec_bash_out_err_exit(app, *args):
    if not os.access(app, os.X_OK):
        st = os.stat(app)
        os.chmod(app, st.st_mode | stat.S_IEXEC) #  st.st_mode | 0111 for all

    args = flatten(args)
    cmd = [str(arg) for arg in args]
    proc = subprocess.run(["/bin/bash", app, *cmd], capture_output=True, text = True)
    return proc.stdout, proc.stderr, proc.returncode

def func_exec_bash_stdout(app, *args):
    if not os.access(app, os.X_OK):
        st = os.stat(app)
        os.chmod(app, st.st_mode | stat.S_IEXEC) #  st.st_mode | 0111 for all

    args = flatten(args)
    cmd = [str(arg) for arg in args]
    out, err = subprocess.Popen(["/bin/bash", app, *cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    return out.decode('utf-8'), err.decode('utf-8')

def run_script(script, *args):
    if os.path.exists(script) and not os.access(script, os.X_OK):
        st = os.stat(script)
        os.chmod(script, st.st_mode | stat.S_IEXEC) #  st.st_mode | 0111 for all

    # Mainul: we may need to use subprocess.run here for long running operation
    # args = list(chain.from_iterable(args))
    args = flatten(args)
    cmd = [str(arg) for arg in args]
    out, err = subprocess.Popen(["/bin/bash", script, *cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True).communicate()
    return out, err
    
def pyvenv_run(toolpath, app, *args):
    script = os.path.join(toolpath, Path(app).stem + '.sh')
    if not os.path.exists(script):
        with open(script, 'w') as f:
            f.write('#!/bin/bash')
            f.write('\n')
            venvpath = os.path.join(os.path.dirname(sys.executable), 'activate')
            f.write('source {0}'.format(venvpath))
            f.write('\n')
            f.write(os.path.basename(app))
            if args:
                for  i in range(0, len(args)):
                    f.write(" ${0}".format(i + 1))
        st = os.stat(script)
        os.chmod(script, st.st_mode | stat.S_IEXEC) #  st.st_mode | 0111 for all
    
    return run_script(script, *args)

def pyvenv_run_venv_args(toolpath, app, *args):
    script = os.path.join(toolpath, Path(app).stem + '.sh')
    if not os.path.exists(script):
        with open(script, 'w') as f:
            f.write('#!/bin/bash')
            f.write('\n')
            f.write('source $1')
            f.write('\n')
            f.write('shift')
            f.write('\n')
            f.write(f'{app} "$@"')
            
        st = os.stat(script)
        os.chmod(script, st.st_mode | stat.S_IEXEC) #  st.st_mode | 0111 for all
    
    return run_script(script, *args)

def func_exec_run(app, *args):
    out, err = func_exec_stdout(app, *args)
    return out.decode('utf-8'), err.decode('utf-8')

def py_run(app, *args):
    import traceback
    import runpy #https://www.tutorialspoint.com/locating-and-executing-python-modules-runpy
    try:
        sys.argv = ['']
        if args:
            sys.argv.extend(*args)
        runpy.run_path(app, run_name='__main__')
    except Exception as e:
        logging.error(f"Error occurred during execution: {str(e)}" )
        logging.error(traceback.format_exc())
        raise

def docker_exec_out_exit(container, app, *args, **kwargs):
    import docker
    client = docker.from_env()
    container = client.containers.get(container)
    if not container:
        raise ValueError(f"{container} container not found.")

    chdir = f"cd {kwargs['cwd']} && " if 'cwd' in kwargs else ""

    cmd = chdir + app
    args = flatten(args)
    args = [str(arg) for arg in args]
    if args:
        cmd += ' ' + ' '.join(str(arg) for arg in args)
    exec_results = container.exec_run(f"sh -c '{cmd}'")
    return exec_results.output.decode('utf-8'), exec_results.exit_code
