import os
import sys
import json
import tarfile
import tempfile
import zipfile
import shutil
import pathlib
import mimetypes
import pip
import regex
regex.DEFAULT_VERSION = regex.VERSION1

from ..jobs import run_script, stop_script, sync_task_status_with_db, sync_task_status_with_db_for_user, generate_graph
from ..models import Runnable, Workflow, AccessType
from . import main
from .views import Samples
from flask_login import login_required, current_user
from flask import request, jsonify, current_app, send_from_directory, make_response
from werkzeug.utils import secure_filename

from ..biowl.dsl.func_resolver import Library

basedir = os.path.dirname(os.path.abspath(__file__))

class LibraryHelper():
    librariesdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../biowl/libraries')

    def __init__(self):
        self.funcs = []
        self.library = Library()
        self.reload()
    
    def reload(self):
        self.funcs.clear()
        self.library = Library.load(LibraryHelper.librariesdir)
        funclist = []
        for f in self.library.funcs.values():
            funclist.extend(f)
        
        funclist.sort(key=lambda x: (x.group, x.name))
        for f in funclist:
            example = f.example if f.example else f.example2 if f.example2 else ""
            example2 = f.example2 if f.example2 else example
            self.funcs.append({"package_name": f.package if f.package else "", "name": f.name, "internal": f.internal, "example": example, "example2": example2, "desc": f.desc if f.desc else "", "runmode": f.runmode if f.runmode else "", "level": f.level, "group": f.group if f.group else "", "user": f.user if f.user else "", "access": str(f.access) if f.access else "0", "returns": f.returns if f.returns else "", "href": f.href if f.href else ""}) 

library = LibraryHelper()

def update_workflow(user_id, workflow_id, script):
    try:
        if workflow_id:
            workflow = Workflow.query.get(workflow_id)
            if workflow.temp:
                workflow.update_script(script)
            else:
                workflow = Samples.create_workflow(user_id, workflow.name, workflow.desc, script, AccessType.PRIVATE, '', True, workflow.id)
        else:
            workflow = Samples.create_workflow(user_id, "No Name", "No Description", script, AccessType.PRIVATE, '', True)
                
        return jsonify(workflowId = workflow.id)
    except Exception as e:
        return make_response(jsonify(err=str(e)), 500)
    
def run_biowl(workflow_id, script, args, immediate = True):
    try:
        workflow = Workflow.query.get(workflow_id)
                
        if immediate:
            return json.dumps(run_script(library.library, workflow.id, script, args))
        else:
            run_script.delay(library.library, workflow.id, script, args)
            return json.dumps({})
    except Exception as e:
        return make_response(jsonify(err=str(e)), 500)

def build_graph(workflow_id):
    try:
        return generate_graph(library.library, workflow_id)
    except Exception as e:
        return make_response(jsonify(err=str(e)), 500)

def make_fn(path, prefix, ext, suffix):
    path = os.path.join(path, '{0}'.format(prefix))
    if suffix:
        path = '{0}_{1}'.format(path, suffix)
    if ext:
        path = '{0}.{1}'.format(path, ext)
    return path
    
def unique_filename(path, prefix, ext):
    uni_fn = make_fn(path, prefix, ext, '')
    if not os.path.exists(uni_fn):
        return uni_fn
    for i in range(1, sys.maxsize):
        uni_fn = make_fn(path, prefix, ext, i)
        if not os.path.exists(uni_fn):
            return uni_fn

def install(package):
    pip.main(['install', package])
                    
@main.route('/functions', methods=['GET', 'POST'])
@login_required
def functions():
    if request.method == "POST":
        if request.form.get('workflowId'):
            workflowId = request.form.get('workflowId') if int(request.form.get('workflowId')) else 0
            if request.form.get('script'):
                return update_workflow(current_user.id, workflowId, request.form.get('script'));
            
            # Here we must have a valid workflow id
            if not workflowId:
                return make_response(jsonify(err="Invalid workflow to run. Check if the workflow is already saved."), 500)
            
            args = request.form.get('args') if request.form.get('args') else ''
            immediate = request.form.get('immediate') == 'true'.lower() if request.form.get('immediate') else False
            return run_biowl(workflowId, None, args, immediate)
        
        elif request.form.get('mapper'):
            result = {"out": [], "err": []}
            try:
                if request.form.get('pippkgs'):
                    pippkgs = request.form.get('pippkgs')
                    pippkgs = pippkgs.split(",")
                    for pkg in pippkgs:
                        try:
                            install(pkg)
                        except Exception as e:
                            result['err'].append(str(e))
                                    
                # Get the name of the uploaded file
                file = request.files['library'] if len(request.files) > 0 else None
                # Check if the file is one of the allowed types/extensions
                
                package = request.form.get('package')
                this_path = os.path.dirname(os.path.abspath(__file__))
                #os.chdir(this_path) #set dir of this file to current directory
                app_path = os.path.dirname(this_path)
                librariesdir = os.path.normpath(os.path.join(app_path, 'biowl/libraries'))

                user_package_dir = os.path.normpath(os.path.join(librariesdir, 'users', current_user.username))
                if not os.path.isdir(user_package_dir):
                    os.makedirs(user_package_dir)
                
                pkg_or_default = package if package else 'mylib'
                path = unique_filename(user_package_dir, pkg_or_default, '')
                if not os.path.isdir(path):
                    os.makedirs(path)
                
                filename = ''
                if file:
                    # Make the filename safe, remove unsupported chars
                    filename = secure_filename(file.filename)
                    temppath = os.path.join(tempfile.gettempdir(), filename)
                    if os.path.exists(temppath):
                        import uuid
                        temppath = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
                        os.makedirs(temppath)
                        temppath = os.path.join(temppath, filename)
                    file.save(temppath)
                    
                    if zipfile.is_zipfile(temppath):
                        with zipfile.ZipFile(temppath,"r") as zip_ref:
                            zip_ref.extractall(path)
                    elif tarfile.is_tarfile(temppath):
                        with tarfile.open(temppath,"r") as tar_ref:
                            tar_ref.extractall(path)
                    else:
                        shutil.move(temppath, path)
                elif request.form.get('script'):
                    filename = unique_filename(path, pkg_or_default, 'py')
                    
                base = unique_filename(path, pkg_or_default, 'json')
                with open(base, 'w') as mapper:
                    mapper.write(request.form.get('mapper'))
                
                org = request.form.get('org')
                pkgpath = str(pathlib.Path(path).relative_to(os.path.dirname(app_path)))
                pkgpath = os.path.join(pkgpath, os.path.basename(filename))
                pkgpath = pkgpath.replace(os.sep, '.').rstrip('.py')
                
                if request.form.get('script'):
                    with open(filename, 'a+') as script:
                        script.write(request.form.get('script'))
                
                initpath = os.path.join(path, "__init__.py")
                if not os.path.exists(initpath):
                    with open(initpath, 'a'):
                        pass
                    
                access = 1 if request.form.get('access') and request.form.get('access').lower() == 'true'  else 2 
                with open(base, 'r') as json_data:
                    data = json.load(json_data)
                    libraries = data["functions"]
                    for f in libraries:
                        if 'internal' in f and f['internal']:
                            if not 'name' in f:
                                f['name'] = f['internal']
                        elif 'name' in f and f['name']:
                            if not 'internal' in f:
                                f['internal'] = f['name']
                        if not f['internal'] and not f['name']:
                            continue
                        f['access'] = access
                        f['module'] = pkgpath
                        if package:
                            f['package'] = package
                        if org:
                            f['org'] = org
                            
                os.remove(base)
                with open(base, 'w') as f:
                    f.write(json.dumps(data, indent=4))
                library.reload()
                
                result['out'].append("Library successfully added.")
            except Exception as e:
                result['err'].append(str(e))
            return json.dumps(result)
        elif request.form.get('provenance'):
            fullpath = os.path.join(os.path.dirname(os.path.dirname(basedir)), "workflow.log")
            mime = mimetypes.guess_type(fullpath)[0]
            return send_from_directory(os.path.dirname(fullpath), os.path.basename(fullpath), mimetype=mime, as_attachment = mime is None )
    elif 'codecompletion' in request.args:
        keywords = [{"package_name": "built-in", "name": "if", "example": "if True:", "group":"keywords"}, {"package_name": "built-in", "name": "for", "example": "for i in range(1, 100):", "group":"keywords"},{"package_name": "built-in", "name": "parallel", "example": "parallel:\r\nwith:", "group":"keywords"},{"package_name": "built-in", "name": "task", "example": "task task_name(param1, param2=''):", "group":"keywords"}]
        funcs = []
        codecompletion = request.args.get('codecompletion')
        for func in library.funcs:
            if int(func['access']) < 2 or (func['user'] and func['user'] == current_user.username):
                if codecompletion:
                    if not regex.match(codecompletion, func['name'], regex.IGNORECASE):
                        continue
                funcs.append({"package_name": func['package_name'], "name": func['name'], "example": func['example'], "group": func['group']})
        if not codecompletion:
            funcs.extend(keywords)
        else:
            for keyword in keywords:
                if regex.match(codecompletion, keyword['name'], regex.IGNORECASE):
                    funcs.append(keyword)
                    
        return json.dumps({'functions':  funcs})
    elif 'demoserviceadd' in request.args:
        demoservice = {'script':'', 'mapper': ''}
        base = os.path.join(os.path.dirname(basedir), 'biowl')
        with open(os.path.join(base, 'demoservice.py'), 'r') as f:
            demoservice['script'] = f.read()
        with open(os.path.join(base, 'demoservice.json'), 'r') as f:
            demoservice['mapper'] = f.read()
        return jsonify(demoservice= demoservice)
    else:
        level = int(request.args.get('level')) if request.args.get('level') else 0
        access = int(request.args.get('access')) if request.args.get('access') else 0
        return get_functions(level, access)

@main.route('/graphs', methods=['GET', 'POST'])
@login_required
def graphs():
    if request.method == "POST":
#        if request.form.get('script'):
        workflowId = request.form.get('workflowId') if int(request.form.get('workflowId')) else 0
        if not workflowId:
            return make_response(jsonify(err="Invalid workflow to run. Check if the workflow is already saved."), 500)
        else:
            return build_graph(workflowId)
    return json.dumps({})

def get_user_status(user_id):
    return jsonify(runnables =[i.to_json_info() for i in Runnable.query.join(Workflow).filter(Workflow.user_id == user_id).order_by(Runnable.id)])

def get_task_status(task_id):
    runnable = Runnable.query.get(task_id)
    return json.dumps(runnable.to_json_log())

def get_task_full_status(task_id):
    runnable = Runnable.query.get(task_id)
    return json.dumps(runnable.to_json_tooltip())
    
@main.route('/runnables', methods=['GET', 'POST'])
@login_required
def runnables():
    try:
        if request.args.get('tooltip'):
            return get_task_full_status(int(request.args.get('tooltip')))
        elif request.args.get('id'):
            return get_task_status(int(request.args.get('id')))
        elif request.args.get('stop'):
            ids = request.args.get('stop')
            ids = ids.split(",")
            new_status = []
            for runnable_id in ids:
                runnable = Runnable.query.get(int(runnable_id))
                if runnable:
                    stop_script(runnable.celery_id)
                    new_status.append(runnable)
                    sync_task_status_with_db(runnable)
            return jsonify(runnables =[i.to_json_log() for i in new_status])
        elif request.args.get('restart'):
            ids = request.args.get('restart')
            ids = ids.split(",")
            new_status = []
            for runnable_id in ids:
                runnable = Runnable.query.get(int(runnable_id))
                if runnable:
                    if not runnable.completed():
                        stop_script(runnable.celery_id)
                        sync_task_status_with_db(runnable)
                    run_biowl(current_user.id, runnable.workflow_id, runnable.script, runnable.arguments, False, False)    
            return jsonify(runnables =[i.to_json_log() for i in new_status])
        
        sync_task_status_with_db_for_user(current_user.id)
    #     runnables_db = Runnable.query.filter(Runnable.user_id == current_user.id)
    #     rs = []
    #     for r in runnables_db:
    #       rs.append(r.to_json())
    #     return jsonify(runnables = rs)
        return get_user_status(current_user.id)
    except Exception as e:
        current_app.logger.error("Unhandled Exception at executables: {0}".format(e))
        return json.dumps({})

def get_functions(level, access):
    funcs = []
    for func in library.funcs:
        if int(func['level']) <= level and func['access'] == str(access) and (access < 2 or (func['user'] and func['user'] == current_user.username)):
            funcs.append(func)
            
    return json.dumps({'functions':  funcs})