import os
import stat
import subprocess

def func_exec_stdout(app, *args):
    cmd = app
    if args:
        cmd += ' ' + ' '.join(args)
    
    if not os.access(app, os.X_OK):
        st = os.stat(app)
        os.chmod(app, st.st_mode | stat.S_IEXEC) #  st.st_mode | 0111 for all
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return p.stdout, p.stderr

def func_exec_bash_stdout(app, *args):
    cmd = ["/bin/bash", app]
    if not os.access(app, os.X_OK):
        st = os.stat(app)
        os.chmod(app, st.st_mode | stat.S_IEXEC) #  st.st_mode | 0111 for all
    if args:
        cmd.append(' '.join(args))
    out, err = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    return out.decode('utf-8'), err.decode('utf-8')
    

def func_exec_run(app, *args):
    out, err = func_exec_stdout(app, *args)
    return out.decode('utf-8'), err.decode('utf-8')