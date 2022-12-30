import logging
import io
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

from . import main
from .views import Samples
from flask_login import login_required, current_user
from flask import request, jsonify, current_app, send_from_directory, make_response, send_file
from werkzeug.utils import secure_filename

from ..managers.usermgr import usermanager
from ..managers.workflowmgr import workflowmanager
from ..managers.runmgr import runnablemanager
from app.objectmodel.common import *
from ..managers.modulemgr import modulemanager
from app.system.exechelper import run_script

basedir = os.path.dirname(os.path.abspath(__file__))

def update_workflow(user_id, workflow_id, script, params, returns):
    if workflow_id:
        workflow = workflowmanager.first(id=workflow_id)
        kwargs = {}
        if script is not None:
            kwargs['script'] = script
        if params is not None:
            kwargs['params'] = params
        if returns is not None:
            kwargs['returns'] = returns

        if workflow.isEqual(**kwargs):
            return workflow
        
        writeaccess = workflow.temp
        
        if not writeaccess:
            if workflow.public:
                writeaccess = user_id == workflow.user_id
                if not writeaccess:
                    permissions = workflow.user.role.permissions if workflow.user and workflow.user.role else Permission.NOTSET
                    writeaccess = permissions & Permission.ADMINISTER or permissions & Permission.MODERATE_WORKFLOWS
            if not writeaccess:
                accesses = workflow.accesses#.query.filter(user_id = WorkflowAccess.user_id)
                for access in accesses:
                    if access.user_id == user_id and access.rights == AccessRights.Write or access.rights == AccessRights.Owner:
                        writeaccess = True
        
        if writeaccess:
            workflow.update_script(script)
        else:
            workflow = Samples.create_workflow(user_id, 0, workflow.name, workflow.desc, script, params, returns, AccessType.PRIVATE, '', True, workflow.id)
    else:
        workflow = Samples.create_workflow(user_id, 0, "No Name", "No Description", script, params, returns, AccessType.PRIVATE, '', True)
    return workflow

def run_biowl_internal(workflow_id, user_id, script, args, provenance = False):
    from ..jobs import run_script

    argsjson = {}
    if args:
        if not isinstance(args, dict):
            try:
                argsjson = json.loads(args)
            except:
                argslist = args.split(',')
                for a in argslist:
                    keyval = a.split('=')
                    argsjson[keyval[0]] = keyval[1]
        else:
            argsjson = args

    workflow = workflowmanager.first(id=workflow_id)
    runnable = runnablemanager.create_runnable(user_id, workflow, script if script else workflow.script, provenance, argsjson)
           
    if isinstance(args, dict):
        argsparse = []
        for k,v in args.items():
            argsparse.append(k + '=' + f'"{v}"' if isinstance(v, str) else str(v))
        args = ",".join(argsparse)
    return run_script(runnable.id, args, provenance)

def run_biowl(workflow_id, script, args, immediate = True, provenance = False):
    try:
        from ..jobs import run_script
        argsjson = {}
        if args:
            if not isinstance(args, dict):
                try:
                    argsjson = json.loads(args)
                except:
                    argslist = args.split(',')
                    for a in argslist:
                        keyval = a.split('=')
                        argsjson[keyval[0]] = keyval[1]
            else:
                argsjson = args

        workflow = workflowmanager.first(id=workflow_id)
        runnable = runnablemanager.create_runnable(current_user.id, workflow, script if script else workflow.script, provenance, argsjson)

        args = ','.join([a["name"] + "=" + f'"{a["value"]}"' for a in argsjson])
        run_script(runnable.id, args, provenance) if immediate else run_script.delay(runnable.id, args, provenance)
        
        return runnable
    except:
        if runnable:
            runnable.update_status(Status.FAILURE)
        raise

def save_and_run_workflow(script, args, immediate = True, provenance = False):
    workflow = update_workflow(current_user.id, 0, script)
    run_biowl(workflow.id, script, args, immediate, provenance)
    
def build_graph(workflow_id):
    try:
        from ..jobs import generate_graph_from_workflow
        return json.dumps(generate_graph_from_workflow(workflow_id))
    except Exception as e:
        current_app.logger.error(str(e))
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
def install(pipenv, package):
    if not pipenv:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    else:
        if not pipenv in python_venvs:
            raise ValueError("Python virtual environment {pipvenv} does not exist.")
        
        run_script(os.path.join(basedir, "pipinstall.sh"), os.path.join(python_venvs["pipenv"], 'bin/activate'), package)

def create_pkg_dir(user_package_dir, create_init = True):
    if not os.path.isdir(user_package_dir):
        os.makedirs(user_package_dir)
    initpath = os.path.join(user_package_dir, '__init__.py')
    if not os.path.isfile(initpath):
        with open(initpath, 'a'):
            pass
    return user_package_dir

@main.route('/provenance', methods=['GET', 'POST'])
@login_required
def provenance():
    from app import app
    from app.objectmodel.provmod.pluginmgr import PluginManager

    try:
        if 'users' in request.args:
            return get_users()        
        elif 'delete' in request.args:
            return PluginManager.instance().delete(request.args.get("delete"), 'confirm' in request.args and request.args.get("confirm").lower() == "true")
        elif 'demoprovenanceadd' in request.args:
            return PluginManager.instance().load_demo()
        elif request.method == "POST" and request.form.get('html'):
            result = {"out": [], "err": []}
            try:
                pippkgsdb = ''
                pipenv = request.form.get('pipenv') if request.form.get('pipenv') else ''
                if request.form.get('pippkgs'):
                    pippkgs = request.form.get('pippkgs')
                    pippkgs = pippkgs.split(",")
                    pippkgsdb = ''
                    for pkg in pippkgs:
                        try:
                            install(pipenv, pkg)
                            pippkgsdb = pippkgsdb + ',' + pkg if pippkgsdb else pkg
                        except Exception as e:
                            result['err'].append(str(e))
                # Get the name of the uploaded file
                file = request.files['library'] if len(request.files) > 0 else None
                #user_package_dir = os.path.normpath(os.path.join(pluginsdir, 'users', current_user.username))

                scriptname = PluginManager.instance().get_script_name(request.form.get('script'))
                if not scriptname:
                    raise ValueError("No plugin is defined in the script.")
                
                user_package_dir = create_pkg_dir(os.path.join(app.config['PROVENANCE_DIR'], 'users'))
                user_package_dir = create_pkg_dir(os.path.join(user_package_dir, current_user.username))
                user_package_dir = create_pkg_dir(os.path.join(user_package_dir, scriptname))

                # save provenance plugin coming as python script    
                with open(os.path.join(user_package_dir,  scriptname + ".py"), 'w') as script:
                    script.write(request.form.get('script'))
                        
                PluginManager.instance().walk_package("{0}.users.{1}.{2}.{3}".format(app.config['PROVENANCE_PACKAGE'], current_user.username, scriptname, scriptname))

                # save view plugin coming as html                    
                if request.form.get('html'):
                    user_template_dir = create_pkg_dir(os.path.join(app.config['HTML_DIR'], 'users', current_user.username, scriptname), False)
                    with open(os.path.join(user_template_dir, scriptname + ".html"), 'w') as html:
                        html.write(request.form.get('html'))
                
                if file:
                    # Make the filename safe, remove unsupported chars
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(user_package_dir, filename)
                    file.save(filepath)
                    if zipfile.is_zipfile(filepath):
                        with zipfile.ZipFile(filepath, "r") as zip_ref:
                            zip_ref.extractall(filepath)
                    elif tarfile.is_tarfile(filepath):
                        with tarfile.open(filepath,"r") as tar_ref:
                            tar_ref.extractall(filepath)             
                result['out'].append("Provenance plugin {0} successfully added.".format(scriptname))
            except Exception as e:
                logging.error(str(e))
                result['err'].append(str(e))
            return json.dumps(result)            
        else:
            return PluginManager.instance().get_json_info()
    
    except Exception as e:
        current_app.logger.error(str(e))
        return make_response(jsonify(err=str(e)), 500)
    
def share_service(share_service):
    service_id, access = share_service["serviceID"], share_service["access"]
    string = modulemanager.get_access(service_id=service_id)
    share_list = string.strip('][').split(', ') if string != '[]' else None#.replace("'", "") 
    if access:
        if share_list:
            for user in share_list:
                modulemanager.remove_user_access(service_id, user)
        modulemanager.update_access(service_id, access)
        return json.dumps({'return':'public'})         
    else:
        sharing_with = share_service["sharedWith"] if "sharedWith" in share_service.keys() else []
        if share_list:
            for user in share_list:
                if int(user) not in sharing_with:
                    modulemanager.remove_user_access(service_id, user)
                else:
                    sharing_with.remove(int(user))
        modulemanager.update_access(service_id, access) 
        if sharing_with: 
            modulemanager.add_user_access(service_id, sharing_with)
            return json.dumps({'return':'shared'})
        else:
            return json.dumps({'return':'private'})
        
        
def delete_service(service_id):
    if 'confirm' in request.args:
        if request.args.get("confirm") == "true":
            modulemanager.remove(current_user.id, service_id)       
            return json.dumps({'return':'deleted'})
    else:
        shared_service_check = modulemanager.check_access(service_id) 
        if shared_service_check:  
            return json.dumps({'return':'shared'})
        else:
            return json.dumps({'return':'not_shared'})
    return json.dumps({'return':'error'})

def get_users():
    result = usermanager.get_other_users_with_entities(current_user.id, "id", "username")
    return jsonify(result)

def add_demo_service():
    from app import app

    demoservice = {'script':'', 'mapper': ''}
    base = os.path.join(app.config['MODULE_DIR'], 'demo')
    with open(os.path.join(base, 'service.py'), 'r') as f:
        demoservice['script'] = f.read()
    with open(os.path.join(base, 'service.json'), 'r') as f:
        demoservice['mapper'] = json.load(f)
    return jsonify(demoservice= demoservice)

def code_completion(codecompletion):
        keywords = [{"package": "built-in", "name": "if", "example": "if True:", "group":"keywords"}, {"package": "built-in", "name": "for", "example": "for i in range(1, 100):", "group":"keywords"},{"package": "built-in", "name": "parallel", "example": "parallel:\r\nwith:", "group":"keywords"},{"package": "built-in", "name": "task", "example": "task task_name(param1, param2=''):", "group":"keywords"}]
        funcs = []
        for func in modulemanager.get_by_id(current_user.id):
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
    
def check_service_function(request):
    if modulemanager.check_function(request.args.get('name'), request.args.get('package')):
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
                    return json.dumps({'error': "{0} internal name is not found in the code. Check your code in Python Adapter tab.".format(internal)})
        except json.decoder.JSONDecodeError as e:
            return json.dumps({'error': str(e)})
        except Exception as e:
            return json.dumps({'error': str(e)})
    return json.dumps("")

def get_datatypes():
    datatypes = []
    for t in known_types:
        datatypes.append(t)
        datatypes.append(t + "[]")
    return jsonify(datatypes = datatypes)

def get_pyvenvs():
    pyvenvs = []
    for t in python_venvs:
        pyvenvs.append(t)
    return jsonify(pyvenvs = pyvenvs)

@main.route('/functions', methods=['GET', 'POST'])
@login_required
def functions():
    from app import app

    try:
        if request.method == "GET":
            if 'datatypes' in request.args:
                return get_datatypes()
            if 'pyenvs' in request.args:
                return get_pyvenvs()
            if 'check_function' in request.args:
                return check_service_function(request)
            elif 'codecompletion' in request.args:
                return code_completion(request.args.get('codecompletion'))
            elif 'share_service' in request.args:
                return share_service(json.loads(request.args.get("share_service")))
            elif request.args.get("service_id"):
                return delete_service(request.args.get("service_id"))
            elif 'demoserviceadd' in request.args:
                return add_demo_service()
            elif 'tooltip' in request.args:
                func = modulemanager.get_module_by_name_package_for_user_access(current_user.id, request.args.get('name'), request.args.get('package'))
                return json.dumps(convert_to_safe_json(func) if func else "")
            elif 'users' in request.args:
                return get_users()
            elif 'reload' in request.args:
                return json.dumps("")
            else:
                return get_functions(int(request.args.get('access')) if request.args.get('access') else 0)
    
        if request.method == "POST":
            if request.form.get('workflowId'):
                workflowId = int(request.form.get('workflowId')) if int(request.form.get('workflowId')) else 0
                if request.form.get('script'):
                    workflow = update_workflow(current_user.id, workflowId, request.form.get('script'), request.form.get('args'), request.form.get('returns'))
                    return jsonify(workflowId = workflow.id)

                # Here we must have a valid workflow id
                if not workflowId:
                    err="Invalid workflow to run. Check if the workflow is already saved."
                    logging.error(err)
                    return make_response(jsonify(err=err), 500)
                
                args = request.form.get('args') if request.form.get('args') else ''
                immediate = request.form.get('immediate').lower() == 'true' if request.form.get('immediate') else False
                provenance = request.form.get('provenance').lower() == 'true' if request.form.get('provenance') else False
                runnable = run_biowl(workflowId, None, args, immediate, provenance)
                return jsonify(runnableId = runnable.id)

            elif request.form.get('mapper'):
                result = {"out": [], "err": []}
                try:
                    pippkgsdb = ''
                    pipenv = request.form.get('pipenv') if request.form.get('pipenv') else ''
                    if request.form.get('pippkgs'):
                        pippkgs = request.form.get('pippkgs')
                        pippkgs = pippkgs.split(",")
                        for pkg in pippkgs:
                            try:
                                install(pipenv, pkg)
                                pippkgsdb = pippkgsdb + ',' + pkg if pippkgsdb else pkg
                            except Exception as e:
                                result['err'].append(str(e))
                    # Get the name of the uploaded file
                    file = request.files['library'] if len(request.files) > 0 else None
                    # Check if the file is one of the allowed types/extensions
                    package = request.form.get('package')
                    #os.chdir(this_path) #set dir of this file to current directory
                    user_package_dir = os.path.join(app.config['MODULE_DIR'], 'users', current_user.username)
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
                            #create a unique temppath if it already exists
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
                        filename = os.path.join(path, 'adapter.py')
                        with open(filename, 'a+') as script:
                            script.write(request.form.get('script'))
                    base = os.path.join(path, 'funcdefs.json')
                    with open(base, 'w') as mapper:
                        mapper.write(request.form.get('mapper'))
                    org = request.form.get('org')
                    # create '.' based module path
                    pkgpath = str(pathlib.Path(path).relative_to(os.path.dirname(app.config['PLUGIN_DIR'])))
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
                        sharedusers = ''
                    else:
                        if request.form.get('sharedusers'):
                            sharedusers = request.form.get('sharedusers')
                            access = 1
                        else:
                            access = 2
                            sharedusers = ''
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
                            if sharedusers:
                                sharedusers = ast.literal_eval(sharedusers)
                            modulemanager.add(user_id = current_user.id, value = f, access=access, users=sharedusers, pipenv=pipenv, pippkgs=pippkgsdb)
    ## save code to a file
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

    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify(err=str(e))


@main.route('/graphs', methods=['GET', 'POST'])
@login_required
def graphs():
    try:    
        if request.method == "POST":
            if (request.form.get('workflowId')):
                workflowId = request.form.get('workflowId') if int(request.form.get('workflowId')) else 0
                if not workflowId:
                    return make_response(jsonify(err="Invalid workflow to run. Check if the workflow is already saved."), 500)
                else:
                    return build_graph(workflowId)               
            elif request.form.get('monitor'):
                from app.objectmodel.provmod.provobj import Monitor, Run, View
                
                if request.form.get('duration'):
                    return jsonify(duration=Monitor.time(request.form.get('duration')))
                else:
                    runid = request.form.get('monitor')
                    run = Run.get(id = runid)
                    return json.dumps(View.graph(run))
            elif request.form.get('workflow'):
                from app.dsl.wfdsl import Workflow
                
                wfid = request.form.get('workflow')
                wf = Workflow.get(id = wfid)
                return json.dumps(View.graph(wf))
            elif request.form.get('nodeinfo'):
                # from ..graphutil import NodeItem
                # node = NodeItem.load(request.form.get('nodeinfo'))
                return json.dumps(node.json())
        return json.dumps({})
    except Exception as e:
        logging.error(str(e))
        return make_response(jsonify(err=str(e)), 500)

def get_user_status(user_id):
    logs = []
    runnables = runnablemanager.runnables_of_user(user_id)
    for r in runnables:
        log = r.to_json_info()
        if (r.created_on + timedelta(minutes=5) > datetime.utcnow()):
            log['recent'] = 'true'
        logs.append(log)
        
    return jsonify(runnables = logs)

def get_run(runnable_id):
    runnable = runnablemanager.first(id=runnable_id)
    return json.dumps(runnable.json())

def get_task_status(runnable_id):
    runnable = runnablemanager.first(id=runnable_id)
    return json.dumps(runnable.to_json_log())

def get_task_full_status(runnable_id):
    runnable = runnablemanager.first(id=runnable_id)
    return json.dumps(runnable.to_json_tooltip())
# def get_task_output(path):
#      remotepath = os.path.join('/home/mishuk/biowl/storage/', path)
#      file_extension = os.path.splitext(file_path)
#      with open(remotepath, "rb") as data:
#          b64_text = base64.b64encode(data.read())
#      return json.dumps( { "payload": b64_text, "extention": file_extension} )

def get_task_logs(task_id):
    return runnablemanager.get_task_logs(task_id)

def get_tasklogs_as_filecontent(task_id):
    logs = get_task_logs(task_id)
    mime = 'text/plain'
    return send_file(io.BytesIO(json.dumps(logs).encode()), mimetype=mime, as_attachment=True, attachment_filename=str(task_id))
    
@main.route('/runnables', methods=['GET', 'POST'])
@login_required
def runnables():
    from ..jobs import stop_script, sync_task_status_with_db, sync_task_status_with_db_for_user
    try:
        if 'tasklogs' in request.args:
            # json text with 'stderr'/'stdout'
            # return jsonify(logs = get_task_logs(int(request.args.get('tasklogs'))))

            # download as file data
            return get_tasklogs_as_filecontent(int(request.args.get('tasklogs')))
        if request.args.get('tooltip'):
            return get_task_full_status(int(request.args.get('tooltip')))
        elif request.args.get('id'):
            return get_run(int(request.args.get('id')))
        elif request.args.get('status'):
            return get_task_status(int(request.args.get('status')))
#          elif request.args.get('path'):
#              return get_task_output(int(request.args.get('path')))
        elif request.args.get('stop'):
            ids = request.args.get('stop')
            ids = ids.split(",")
            new_status = []
            for runnable_id in ids:
                runnable = runnablemanager.first(id=int(runnable_id))
                if runnable:
                    stop_script(runnable.celery_id)
                    new_status.append(runnable)
                    sync_task_status_with_db(runnable)
            return jsonify(runnables =[i.to_json_log() for i in new_status])
        if request.args.get('compare'):
            run_id1 = int(request.args.get('compare'))
            run_id2 = int(request.args.get('with'))
            view = {}
            view['compare'] = [View.compare(Run(id = run_id1), Run(id = run_id2))]
            return json.dumps({"view": view})
        elif request.args.get('restart'):
            ids = request.args.get('restart')
            ids = ids.split(",")
            new_status = []
            for runnable_id in ids:
                runnable = runnablemanager.get(id=int(runnable_id))
                if runnable:
                    if not runnable.completed:
                        stop_script(runnable.celery_id)
                        sync_task_status_with_db(runnable)
                    run_biowl(runnable.workflow_id, runnable.script, runnable.args, False, False)    
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
        return make_response(jsonify(err=str(e)), 500)

def get_functions(access):
    return json.dumps({'functions':  convert_to_safe_json(modulemanager.get_all_by_user_access(current_user.id, access))})
