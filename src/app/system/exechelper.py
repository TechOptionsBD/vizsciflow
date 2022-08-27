import os
import sys
import stat
import subprocess
from pathlib import Path

def func_exec_stdout(app, *args):
    if not os.access(app, os.X_OK):
        st = os.stat(app)
        os.chmod(app, st.st_mode | stat.S_IEXEC) #  st.st_mode | 0111 for all
    # cmd = app
    # if args:
    #     cmd += ' ' + ' '.join(str(arg) for arg in args)
    #p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #return p.stdout, p.stderr
    cmd = [str(arg) for arg in args]
    out, err = subprocess.Popen([app, *cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    return out, err

def func_exec_bash_stdout(app, *args):
    if not os.access(app, os.X_OK):
        st = os.stat(app)
        os.chmod(app, st.st_mode | stat.S_IEXEC) #  st.st_mode | 0111 for all

    cmd = [str(arg) for arg in args]
    out, err = subprocess.Popen(["/bin/bash", app, *cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    return out.decode('utf-8'), err.decode('utf-8')
    
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

    if os.path.exists(script) and not os.access(script, os.X_OK):
        st = os.stat(script)
        os.chmod(script, st.st_mode | stat.S_IEXEC) #  st.st_mode | 0111 for all

    # Mainul: we may need to use subprocess.run here for long running operation
    cmd = [str(arg) for arg in args]
    out, err = subprocess.Popen(["/bin/bash", script, *cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    return out.decode('utf-8'), err.decode('utf-8')

def func_exec_run(app, *args):
    out, err = func_exec_stdout(app, *args)
    return out.decode('utf-8'), err.decode('utf-8')