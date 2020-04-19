import os
import sys
import json
import tarfile
import tempfile
import zipfile
import shutil
import pathlib
import mimetypes
import ast
#I have improted subprocess and sys to active alternative install fuction
import subprocess

from datetime import timedelta
from datetime import datetime

import regex
regex.DEFAULT_VERSION = regex.VERSION1

from ..jobs import run_script, stop_script, sync_task_status_with_db, sync_task_status_with_db_for_user, generate_graph
from ..models import Workflow, AccessType, Service, ServiceAccess, User
from . import main
from .views import Samples, AlchemyEncoder
from flask_login import login_required, current_user
from flask import request, jsonify, current_app, send_from_directory, make_response
from werkzeug.utils import secure_filename
from ..runmgr import runnableManager


basedir = os.path.dirname(os.path.abspath(__file__))

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
        runnable = runnableManager.create_runnable(current_user.id, workflow_id, script if script else workflow.script, args)
                
        if immediate:
            run_script(runnable.id, args)
        else:
            run_script.delay(runnable.id, args)
            
        return jsonify(runnableId = runnable.id)
    except Exception as e:
        return make_response(jsonify(err=str(e)), 500)

def build_graph(workflow_id):
    try:
        return generate_graph(workflow_id)
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
'''
def install(package):
    pip.main(['install', package])
'''
     

#Previous function did not work for pip version greater then 10
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                          
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
            return run_biowl(int(workflowId), None, args, immediate)
        
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
                scriptname = ''
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
                if request.form.get('script'):
                    scriptname = unique_filename(path, pkg_or_default, 'py')
                    with open(scriptname, 'a+') as script:
                        script.write(request.form.get('script'))
                    
                base = unique_filename(path, pkg_or_default, 'json')
                with open(base, 'w') as mapper:
                    mapper.write(request.form.get('mapper'))
                
                org = request.form.get('org')
                pkgpath = str(pathlib.Path(path).relative_to(os.path.dirname(app_path)))
                pkgpath = os.path.join(pkgpath, os.path.basename(filename))
                pkgpath = pkgpath.replace(os.sep, '.').rstrip('.py')

                # create an empty __init__.py to make the directory a module                
                initpath = os.path.join(path, "__init__.py")
                if not os.path.exists(initpath):
                    with open(initpath, 'a'):
                        pass
                    
#                access = 1 if request.form.get('access') and request.form.get('access').lower() == 'true'  else 2
                if request.form.get('publicaccess') and request.form.get('publicaccess').lower() == 'true':
                    access = 0
                    sharedusers = False 
                else:
                    if request.form.get('sharedusers'):
                        sharedusers = request.form.get('sharedusers')
                        access = 1
                    else:
                        access = 2
                        sharedusers = False              
                               
                with open(base, 'r') as json_data:
                    data = json.load(json_data)
                    libraries = data["functions"] if "functions" in data else [data]
                    
                    for f in libraries:
                        try:
                            # if internal not given, parse the code and use the first function name as internal (adaptor name) 
                            if not 'internal' in f:
                                if scriptname:
                                    tree = ast.parse(request.form.get('script'))
                                    funcDefs = [x.name for x in ast.walk(tree) if isinstance(x, ast.FunctionDef)]
                                    if funcDefs:
                                        f['internal'] = funcDefs[0]
                                        
                                if not 'internal' in f and not filename:        
                                    with open(filename, 'r') as r:
                                        tree = ast.parse(r.read())
                                        funcDefs = [x.name for x in ast.walk(tree) if isinstance(x, ast.FunctionDef)]
                                        if funcDefs:
                                            f['internal'] = funcDefs[0]
                        except:
                            pass
                                
                        if 'internal' in f and f['internal']:
                            if not 'name' in f:
                                f['name'] = f['internal']
                        elif 'name' in f and f['name']:
                            if not 'internal' in f:
                                f['internal'] = f['name']
                        if not f['internal'] and not f['name']:
                            continue
                        #f['access'] = access
#                         if sharedusers:
#                             users = sharedusers.split(";")
#                         else:
#                             users = []
                        f['module'] = pkgpath
                        if package:
                            f['package'] = package
                        if org:
                            f['org'] = org
                        
                        #func = json.dumps(f, indent=4)

                        Service.add(current_user.id, f, access, sharedusers)
                            
#                 os.remove(base)
#                 with open(base, 'w') as f:
#                     f.write(json.dumps(data, indent=4))
                
                result['out'].append("Library successfully added.")
            except Exception as e:
                result['err'].append(str(e))
            return json.dumps(result)
        elif request.form.get('provenance'):
            fullpath = os.path.join(os.path.dirname(os.path.dirname(basedir)), "workflow.log")
            mime = mimetypes.guess_type(fullpath)[0]
            return send_from_directory(os.path.dirname(fullpath), os.path.basename(fullpath), mimetype=mime, as_attachment = mime is None )
            
    elif 'check_function' in request.args:
        if Service.check_function(request.args.get('name'), request.args.get('package')):
            return json.dumps({'error': 'The service already exists. Please change the package and/or service name.'})
        if 'script' in request.args and request.args.get('script') and 'mapper' in request.args and request.args.get('mapper'):
            try:
                mapper = json.loads(request.args.get('mapper'))
                internal = None
                if 'functions' in mapper and 'internal' in mapper['functions'][0]:
                    internal = mapper['functions'][0]['internal'].lower()
                elif 'internal' in mapper:
                    internal = mapper['internal'].lower()
                
                if internal:    
                    tree = ast.parse(request.args.get('script'))
                    funcDefs = [x.name for x in ast.walk(tree) if isinstance(x, ast.FunctionDef)]
                    if not any(s.lower() == internal for s in funcDefs):
                        return json.dumps({'error': "{0} internal name not found in the code.".format(internal)})
            except json.decoder.JSONDecodeError as e:
                return json.dumps({'error': str(e)})
            except Exception as e:
                return json.dumps({'error': str(e)})
        return json.dumps("")
    
    elif 'tooltip' in request.args:
        func = Service.get_first_by_name_package_with_access(current_user.id, request.args.get('name'), request.args.get('package'))
        return json.dumps(func) if func else json.dumps("")

    elif 'service_id' in request.args:
        service_id = request.args.get("service_id")
        if 'confirm' in request.args:
            if request.args.get("confirm") == "true":
                Service.remove(current_user.id, service_id)       
                return json.dumps({'return':'deleted'})
        else:
            shared_service_check = ServiceAccess.check(service_id) 
            if shared_service_check:  
                return json.dumps({'return':'shared'})
            else:
                return json.dumps({'return':'not_shared'})
        return json.dumps({'return':'error'})
    
    elif 'codecompletion' in request.args:
        keywords = [{"package": "built-in", "name": "if", "example": "if True:", "group":"keywords"}, {"package": "built-in", "name": "for", "example": "for i in range(1, 100):", "group":"keywords"},{"package": "built-in", "name": "parallel", "example": "parallel:\r\nwith:", "group":"keywords"},{"package": "built-in", "name": "task", "example": "task task_name(param1, param2=''):", "group":"keywords"}]
        funcs = []
        codecompletion = request.args.get('codecompletion')
        for func in Service.get_by_user(current_user.username):
            if int(func.value['access']) < 2 or (func['user'] and func['user'] == current_user.username):
                if codecompletion:
                    if not regex.match(codecompletion, func['name'], regex.IGNORECASE):
                        continue
                funcs.append({"package": func['package'], "name": func['name'], "example": func['example'], "group": func['group']})
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
    elif 'reload' in request.args:
        #library.reload()
        return json.dumps("")
    
    elif 'users' in request.args:
        result = User.query.filter(current_user.id != User.id).with_entities(User.id, User.username)
        j = json.dumps([r for r in result], cls=AlchemyEncoder)
        return jsonify(j)
    
#     elif 'share_service' in request.args:
#         share_service = request.args.get("share_service")
#         shared_check = ServiceAccess.check(share_service) 
#         if shared_check: 
#             result = ServiceAccess.query.filter(ServiceAccess.service_id == share_service).with_entities(ServiceAccess.user_id)
#             lst = json.dumps([r for r in result], cls=AlchemyEncoder)
#             lst = lst.replace('[', '').replace(']', '').replace(' ', '')
#             user_list = list(lst.split(","))
#             if 'sharing_users' in request.args:
#                 sharing_users = request.args.get("sharing_users")
#                 for user in user_list:
#                     if user not in sharing_users:
#                         ServiceAccess.remove_user(user)
#                     else:
#                         sharing_users.remove(user)
#                  
#                 ServiceAccess.add(share_service, sharing_users)
#                  
#             return jsonify(user_list)
#              
#         else:
#             return json.dumps("")
        
    elif 'share_service' in request.args:
        share_service = json.loads(request.args.get("share_service"))
        service_id, access = share_service["serviceID"], share_service["access"]
        string = ServiceAccess.get_by_service_id(service_id)
        share_list = string.strip('][').split(', ') if string != '[]' else None#.replace("'", "") 
        if access:
            if share_list:
                for user in share_list:
                    ServiceAccess.remove_user(service_id, user)
            Service.update_access(service_id, access)
            return json.dumps({'return':'public'})         
        else:
            sharing_with = share_service["sharedWith"] if "sharedWith" in share_service.keys() else []
            if share_list:
                for user in share_list:
                    if int(user) not in sharing_with:
                        ServiceAccess.remove_user(service_id, user)
                    else:
                        sharing_with.remove(int(user))
            Service.update_access(service_id, access) 
            if sharing_with != []: 
                ServiceAccess.add(service_id, sharing_with)      
                return json.dumps({'return':'shared'})
            else:
                return json.dumps({'return':'private'})
    
        
    else:
        return get_functions(int(request.args.get('access')) if request.args.get('access') else 0)


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
    logs = []
    runnables = runnableManager.runnables_of_user(user_id)
    for r in runnables:
        log = r.to_json_info()
        if (r.created_on + timedelta(minutes=5) > datetime.utcnow()):
            log['recent'] = 'true'
        logs.append(log)
        
    return jsonify(runnables = logs)

def get_task_status(runnable_id):
    runnable = runnableManager.get_runnable(runnable_id)
    return json.dumps(runnable.to_json_log())

def get_task_full_status(runnable_id):
    runnable = runnableManager.get_runnable(runnable_id)
    return json.dumps(runnable.to_json_tooltip())
# def get_task_output(path):
#      remotepath = os.path.join('/home/mishuk/biowl/storage/', path)
#      file_extension = os.path.splitext(file_path)
#      with open(remotepath, "rb") as data:
#          b64_text = base64.b64encode(data.read())
#      return json.dumps( { "payload": b64_text, "extention": file_extension} )
     
@main.route('/runnables', methods=['GET', 'POST'])
@login_required
def runnables():
    try:
        if request.args.get('tooltip'):
            return get_task_full_status(int(request.args.get('tooltip')))
        elif request.args.get('id'):
            return get_task_status(int(request.args.get('id')))
#          elif request.args.get('path'):
#              return get_task_output(int(request.args.get('path')))
        elif request.args.get('stop'):
            ids = request.args.get('stop')
            ids = ids.split(",")
            new_status = []
            for runnable_id in ids:
                runnable = runnableManager.get_runnable(int(runnable_id))
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
                runnable = runnableManager.get_runnable(int(runnable_id))
                if runnable:
                    if not runnable.completed():
                        stop_script(runnable.celery_id)
                        sync_task_status_with_db(runnable)
                    run_biowl(runnable.workflow_id, runnable.script, runnable.arguments, False, False)    
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

def get_functions(access):
    return json.dumps({'functions':  Service.get_by_user(current_user.id, access)})