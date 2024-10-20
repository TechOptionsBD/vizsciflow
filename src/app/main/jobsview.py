import logging
import io
import os
import sys
import json
import uuid
import tarfile
import tempfile
import zipfile
import shutil
import pathlib
import mimetypes
import ast

from datetime import timedelta
from datetime import datetime

import regex
regex.DEFAULT_VERSION = regex.VERSION1

from . import main
from .views import Samples
from flask_login import login_required, current_user
from flask import request, jsonify, send_from_directory, make_response, send_file
from werkzeug.utils import secure_filename
import shutil
import uuid

from ..managers.usermgr import usermanager
from ..managers.datamgr import datamanager
from ..managers.workflowmgr import workflowmanager
from ..managers.runmgr import runnablemanager
from app.objectmodel.common import *
from ..managers.modulemgr import modulemanager
from ..managers.activitymgr import activitymanager

basedir = os.path.dirname(os.path.abspath(__file__))

def load_args(args):
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
    return argsjson

def run_biowl_internal(workflow_id, user_id, script, args, provenance = False):
    from ..jobs import run_script

    argsjson = load_args(args)
    workflow = workflowmanager.first(id=workflow_id)
    runnable = runnablemanager.create_runnable(user_id, workflow, script if script else workflow.script, provenance, argsjson)
           
    if isinstance(args, dict):
        argsparse = []
        for k,v in args.items():
            if isinstance(v, str):
                argsparse.append(k + '=' + f'"{v}"')
            else:
                argsparse.append(k + '=' + str(v))

        args = ",".join(argsparse)
    return run_script(runnable.id, args, provenance)

def run_biowl(workflow_id, script, args, immediate = True, provenance = False):
    try:
        from ..jobs import run_script
        argsjson = load_args(args)
        workflow = workflowmanager.first(id=workflow_id)
        runnable = runnablemanager.create_runnable(current_user.id, workflow, script if script else workflow.script, provenance, argsjson)

        args = ','.join([a["name"] + "=" + a["value"] for a in argsjson if a["value"]])
        run_script(runnable.id, args, provenance) if immediate else run_script.delay(runnable.id, args, provenance)
        
        return runnable
    except:
        if runnable:
            runnable.update_status(Status.FAILURE)
        raise

def save_and_run_workflow(script, args, immediate = True, provenance = False):
    workflow = Samples.update_workflow(current_user.id, 0, script)
    run_biowl(workflow.id, script, args, immediate, provenance)

def build_graph(workflow_id):
    try:
        from ..jobs import generate_graph_from_workflow
        return json.dumps(generate_graph_from_workflow(workflow_id))
    except Exception as e:
        logging.error(str(e))
        return make_response(jsonify(err=str(e)), 500)

def make_fn(path, prefix, ext, suffix):
    path = os.path.join(path, f"{prefix if prefix else ''}")
    path += f"_{suffix}"  if suffix else ''
    return path + f".{ext}" if ext else path
    
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
                pipvenv = request.form.get('pipvenv') if request.form.get('pipvenv') else ''
                if request.form.get('pippkgs'):
                    pippkgs = request.form.get('pippkgs')
                    pippkgs = pippkgs.split(",")
                    pippkgsdb = ''
                    for pkg in pippkgs:
                        try:
                            pip_install(pipvenv, pkg)
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
        logging.error(str(e))
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
        
def toggle_publish_service(request):
    service_id = request.args.get("service_id")
    modulemanager.toggle_publish(current_user.id, service_id)
    return json.dumps({'return':'publish toggled'})
    
def delete_service(request):
    service_id = request.args.get("service_id")
    if request.args.get("delete") == "true":
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

def add_demo_service(moduleName):
    from app import app
    import os
    import json

    demoservice = {'script':'', 'mapper': ''}
    base = os.path.join(app.config['MODULE_DIR'], 'demos', moduleName)
    if not os.path.isdir(base):
        base = os.path.join(app.config['MODULE_DIR'], 'demos', 'adapter')
    with open(os.path.join(base, 'adapter.py'), 'r') as f:
        demoservice['script'] = f.read()
    with open(os.path.join(base, 'funcdefs.json'), 'r') as f:
        demoservice['mapper'] = json.load(f)
    return jsonify(demoservice=demoservice)

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
    funcname = request.args.get('name')
    package = request.args.get('package')
    if modulemanager.check_function(funcname, package):
        return json.dumps({'error': f'The service {package + "." if package else ""}{funcname} already exists. Please change the package and/or service name.'})
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
                    return json.dumps({'error': f"{internal} internal name is not found in the code. Check your code in Python Adapter tab."})
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

def get_pip_req_activity(activity, path, req):
    activity.add_log(log="Move requirements file to tool folder ...")
    filename = secure_filename(req.filename)
    temppath = os.path.join(path, filename)
    if os.path.exists(temppath):
        reqFileName = pathlib.Path(filename)
        suffix = reqFileName.suffix
        if suffix:
            suffix = suffix[1]
        temppath = unique_filename(os.path.dirname(path), reqFileName.stem, reqFileName.suffix)
    req.save(temppath)
    return str(pathlib.Path(temppath).relative_to(path))

def download_service(service_id):
    from app import app

    module = modulemanager.first(id=service_id)
    modpath = module.value["module"]
    tooldir = os.path.join(app.config['MODULE_DIR'], (os.path.sep).join(modpath.split('.')[2:-1])) # remove plugins/modules from front and adapter from back
    
    temppath = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()), os.path.basename(tooldir))
    temppath = shutil.make_archive(temppath, 'zip', tooldir)
    mime = mimetypes.guess_type(temppath)[0]
    return send_from_directory(os.path.dirname(temppath), os.path.basename(temppath), mimetype=mime, as_attachment = mime is None)

@staticmethod 
def upload_data_file(user_id, request, fullpath): 
    files = request.files
    is_exist = False 
    existed_file = "" 
    for _, each_file in files.items(): 
        each_filename = each_file.filename 
        if os.path.exists(os.path.join(fullpath, each_filename)): 
            existed_file = "'" + each_filename + "'" if existed_file == "" else existed_file + ", " + "'" + each_filename + "'" 
            is_exist = True
    if is_exist: 
        return {"error_msg": "File already exists", 'error_message': 400}

    all_data=[] 
    for _, eachFile in files.items(): # Uploading each file in the data directory 
        saved_path, file_path = fs.save_upload(eachFile, fullpath) 
        each_data = data.to_json_allocation(fullpath, mime) 
        all_data.append(each_data) 
    return all_data
      
def upload_chunk_data(request, folder):
    try:
        if not request.files.get("file"):
            raise ValueError("No file found for chunk upload.")

        file = request.files['file'] 
        file_uuid = request.form['dzuuid'] 
        current_chunk = int(request.form['dzchunkindex']) 
        total_chunks = int(request.form['dztotalchunkcount']) 
        offset = int(request.form['dzchunkbyteoffset']) 
        total_filesize = int(request.form['dztotalfilesize'])
        
        folder = os.path.join(folder, file_uuid)
        chunkinfo = datamanager.upload_chunk_data(current_user.id, file, file_uuid, current_chunk, total_chunks, offset, total_filesize, folder)
        return chunkinfo['path'], 200
    except Exception as e:
        logging.error(f"Chunk upload error: {str(e)}")
        return str(e), 400

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    return upload_chunk_data(request, tempfile.gettempdir())

@main.route('/dockerupload', methods=['GET', 'POST'])
@login_required
def docker_upload():
    from app import app
    return upload_chunk_data(request, app.config['DOCKER_IMAGE_DIR'])

def load_run_docker_container(activity, path, containername):
    import docker

    activity.add_log(log="Creating container for new tool...")
    client = docker.from_env()
    images = client.images.load(path)
    if not images:
        raise ValueError("Docker image not found")

    imagename = images[0].attrs['Config']['Image']
    command = 'sh -c "tail -F anything"'
    container = client.containers.run(imagename, command=command, detach=True, name=containername)
    if container:
        runnablemanager.add_docker_image_container(current_user.id, imagename, containername, command)

def create_lib_dir(activity, path):
    from app import app

    activity.add_log(log="Creating folder for new tool...")

    user_package_dir = os.path.join(app.config['MODULE_DIR'], 'users', current_user.username)
    libdir = unique_filename(user_package_dir, 'mylib', '')
    if not os.path.exists(libdir):
        os.makedirs(libdir)

    activity.add_log(log="Extracting tool package in tools directory...", type=LogType.INFO)
    if path:
        if zipfile.is_zipfile(path):
            with zipfile.ZipFile(path,"r") as zip_ref:
                zip_ref.extractall(libdir)
        elif tarfile.is_tarfile(path):
            with tarfile.open(path,"r") as tar_ref:
                tar_ref.extractall(libdir)
        else:
            shutil.copyfile(path, os.path.join(libdir, os.path.basename(path)))
            # activity.add_log(log="Only .zip or .tar is allowed as a tool package.", type=LogType.ERROR)
            # raise ValueError("Only .zip or .tar is allowed as a tool package.")
    
        activity.add_log(log="Deleting tool .zip or .tar from temp directory...")
        os.remove(path)
    return libdir

def create_lib_dir_files(activity, uploadedlib):
    from app import app

    activity.add_log(log="Creating folder for new tool...")

    user_package_dir = os.path.join(app.config['MODULE_DIR'], 'users', current_user.username)
    libdir = unique_filename(user_package_dir, 'mylib', '')
    if not os.path.exists(libdir):
        os.makedirs(libdir)

    if uploadedlib:
        activity.add_log(log="Extracting tool package in tools directory...", type=LogType.INFO)

        filename = secure_filename(uploadedlib.filename)
        tempdir = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        temppath = os.path.join(tempdir, filename)
        os.makedirs(tempdir)
        uploadedlib.save(temppath)
    
        if zipfile.is_zipfile(temppath):
            with zipfile.ZipFile(temppath,"r") as zip_ref:
                zip_ref.extractall(libdir)
        elif tarfile.is_tarfile(temppath):
            with tarfile.open(temppath,"r") as tar_ref:
                tar_ref.extractall(libdir)
        else:
            shutil.copyfile(temppath, os.path.join(libdir, filename))
            # activity.add_log(log="Only .zip or .tar is allowed as a tool package.", type=LogType.ERROR)
            # raise ValueError("Only .zip or .tar is allowed as a tool package.")
        
        activity.add_log(log="Deleting tool .zip or .tar from temp directory...")
        os.remove(temppath)
    return libdir

def get_dockercontainers(user_id):
    containers = runnablemanager.get_dockercontainers()
    return [container.to_json() for container in containers]

def get_dockerimages(user_id):
    images = runnablemanager.get_dockerimages()
    return [image.to_json() for image in images]

def new_dockerenvs(activity, dockerpath, imagename, containername, user_id):
    import docker

    if dockerpath and os.path.exists(dockerpath):
        imagename = load_run_docker_container(activity, dockerpath, containername)
    else:
        # check dockerpath from request to check if docker image is uploaded
        client = docker.from_env()
        container = client.containers.list(all=True, filters={'name': containername})
        if container:
            raise ValueError(f"Container {containername} already exists.")
        images = client.images.list()

        foundimage = None
        for image in images:
            name = image.attrs['Config']['Image']
            if name == imagename:
                foundimage = image
                break

        if not foundimage:
            activity.add_log(log=f"Pulling {imagename} image from docker hub...")
            client.images.pull(imagename)
    
    activity.add_log(log=f"Running {containername} container...")
    command = 'sh -c "tail -F anything"'
    container = client.containers.run(imagename, command=command, detach=True, name=containername)
    if container:
        runnablemanager.add_docker_image_container(user_id, imagename, containername, command)
    return json.dumps({"success": "Container created."})

def parse_string_to_int(s, default = 0):
    try:
        return int(s)
    except ValueError:
        return default

@main.route('/functions', methods=['GET', 'POST'])
@login_required
def functions():
    from .chat import SendChatMessage
    try:
        if request.method == "GET":
            if 'name' in request.args and 'package' in request.args:
                return get_service(request.args['name'], request.args['package'])
            elif 'datatypes' in request.args:
                return get_datatypes()
            elif 'pyenvs' in request.args:
                pyvenvs = get_pyvenvs(current_user.id)
                return jsonify(pyvenvs = pyvenvs)
            
            elif 'dockercontainers' in request.args:
                dockercontainers = get_dockercontainers(current_user.id)
                return jsonify(dockercontainers = dockercontainers)

            elif 'dockerimages' in request.args:
                dockerimages = get_dockerimages(current_user.id)
                return jsonify(dockerimages = dockerimages)
            
            elif 'newpyvenvs' in request.args:
                return new_pyvenvs(request.args.get('newpyvenvs'), request.args.get('pyversion'), current_user.id)
            
            elif 'newdockerimagename' in request.args or ('docker' in request.args and os.path.exists(request.args.get('docker')) ) :
                return new_dockerenvs(activity, request.args.get('docker'), request.args.get('newdockerimagename'), request.args.get('newdockercontainername'), current_user.id)
            elif request.args.get('chatmsg'):
                return json.dumps(SendChatMessage(request.args.get("workflow_id"), request.args.get('chatmsg')))
            elif 'check_function' in request.args:
                return check_service_function(request)
            elif 'codecompletion' in request.args:
                return code_completion(request.args.get('codecompletion'))
            elif 'share_service' in request.args:
                return share_service(json.loads(request.args.get("share_service")))
            elif request.args.get("delete"):
                return delete_service(request)
            elif request.args.get("toggleactive"):
                return toggle_publish_service(request)
            elif 'demoserviceadd' in request.args:
                return add_demo_service(request.args.get("demoserviceadd"))
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
            if request.form.get("download_service"):
                return download_service(request.form.get("download_service"))
            elif request.form.get('workflowId'):
                workflowId = parse_string_to_int(request.form.get('workflowId')) if request.form.get('workflowId') else 0
                if request.form.get('script'):
                    workflow = Samples.update_workflow(current_user.id, workflowId, request.form.get('script'), request.form.get('args'), request.form.get('returns'))
                    return json.dumps(workflow.to_json())

                # Here we must have a valid workflow id
                if not workflowId:
                    err="Invalid workflow to run. Check if the workflow is already saved."
                    logging.error(err)
                    return make_response(jsonify(err=err), 500)
                
                args = request.form.get('args') if request.form.get('args') else ''
                immediate = request.form.get('immediate').lower() == 'true' if request.form.get('immediate') else False
                
                # uncomment following line for debugging
                # immediate = True

                provenance = request.form.get('provenance').lower() == 'true' if request.form.get('provenance') else False
                runnable = run_biowl(workflowId, None, args, immediate, provenance)
                return jsonify(runnableId = runnable.id)

            elif 'package' in request.form and os.path.exists(request.form['package']):
                '''Add package'''
                activity = None
                try:
                    activity = activitymanager.create(current_user.id, ActivityType.ADDTOOLPACKAGE)
                    activity.status = Status.STARTED
                    activity.add_log(log="Installing tool(s) from tool package...", type=LogType.INFO)
                    activity.add_log(log="Saving tool package to temp directory...", type=LogType.INFO)
                    
                    libdir = create_lib_dir(activity, request.form['package'])

                    # check if update can be made
                    activity.add_log(log="Checking if tool already exists and we are allowed to update...")
                    update = request.form.get("update") and int(request.form.get("update")) == 1
                    from app.objectmodel.models.loader import Loader
                    funcs = Loader.load_funcs_recursive_flat(libdir, True)
                    for func in funcs:
                        module = modulemanager.get_by_value_key(package = func["package"], name = func["name"]).first()
                        if module:
                            if not update or module.user_id != current_user.id:
                                raise ValueError(f"The {func['package']}{'.' if func['package'] else ''}{func['name']} already exists.")
                            activity.add_log(log=f"The {func['package']}{'.' if func['package'] else ''}{func['name']} already exists. It will be updated.")
                        else:
                            activity.add_log(log=f"The {func['package']}{'.' if func['package'] else ''}{func['name']} does not exists. It will be created.")
                    
                    modules = modulemanager.insert_modules(activity, libdir, current_user.id, True, True)
                    if not modules:
                        raise ValueError("No module added.")
                    
                    activity.add_log(log="Tool added successfully from tool package.")
                    activity.status = Status.SUCCESS
                except Exception as e:
                    activity.status = Status.FAILURE
                    activity.add_log(log=f'Error while integrating new tool: {str(e)}', type=LogType.ERROR)
                    logging.error(f'Error while integrating new tool: {str(e)}')
                return json.dumps(activity.to_json())

            elif request.form.get('mapper'):
                activity = None
                try:
                    activity = activitymanager.create(current_user.id, ActivityType.ADDTOOL)
                    activity.add_log(log="Adding tool from Web UI...")

                    libdir = create_lib_dir(activity, request.form['library'] if 'library' in request.form else None)

                    activity.add_log(log="Saving the adapter code...")
                    if request.form.get('script'):
                        filename = os.path.join(libdir, 'adapter.py')
                        with open(filename, 'a+') as script:
                            script.write(request.form.get('script'))

                    mapper = json.loads(request.form.get('mapper'))

                    if 'reqfile' in mapper:
                        if mapper['reqfile'] and len(request.files) > 0 and 'reqfile' in request.files and request.files['reqfile']:
                            mapper['reqfile'] = get_pip_req_activity(activity, libdir, request.files['reqfile'])
                        else:
                            del mapper['reqfile']

#                access = 1 if request.form.get('access') and request.form.get('access').lower() == 'true'  else 2
                    if request.form.get('publicaccess') and request.form.get('publicaccess').lower() == 'true':
                        mapper["access"] = 0
                        mapper["sharedusers"] = []
                    else:
                        if request.form.get('sharedusers'):
                            mapper["sharedusers"] = ast.literal_eval(request.form.get('sharedusers'))
                            mapper["access"] = 1
                        else:
                            mapper["access"] = 2
                            mapper["sharedusers"] = []

                    activity.add_log(log="Adding module definition to database...")
                    base = os.path.join(libdir, 'funcdefs.json')
                    if not os.path.exists(base):
                        with open(base, 'w') as mapperfile:
                            mapperfile.write(json.dumps(mapper, indent=2))

                    # create an empty __init__.py to make the directory a module                
                    initpath = os.path.join(libdir, "__init__.py")
                    if not os.path.exists(initpath):
                        with open(initpath, 'a'):
                            pass

                    modules = modulemanager.insert_modules(activity, libdir, current_user.id, True, True)
                    if not modules:
                        raise ValueError("No module added.")
                    
                    # correct funcdefs.json file
                    with open(base, 'w') as mapperfile:
                        mapperfile.write(json.dumps(modules[0].value, indent=2))

                    activity.add_log(log="Library successfully added.")
                    activity.status = Status.SUCCESS
                except Exception as e:
                    if activity:
                        activity.add_log(log=str(e), type=LogType.ERROR)
                        activity.status = Status.FAILURE
                    logging.error(f'Error while integrating new tool: {str(e)}')
                    raise
                return json.dumps(activity.to_json())

            elif request.form.get('provenance'):
                fullpath = os.path.join(os.path.dirname(os.path.dirname(basedir)), "workflow.log")
                mime = mimetypes.guess_type(fullpath)[0]
                return send_from_directory(os.path.dirname(fullpath), os.path.basename(fullpath), mimetype=mime, as_attachment = mime is None)

    except Exception as e:
        logging.error(str(e))
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
    return send_file(io.BytesIO(json.dumps(logs).encode()), mimetype=mime, as_attachment=True, download_name=str(task_id))

def get_datavalue_as_filecontent(data_id):
    datavalue = datamanager.get_task_data_value(data_id)
    mime = 'text/plain'
    return send_file(io.BytesIO(json.dumps(datavalue).encode()), mimetype=mime, as_attachment=True, download_name=str(data_id))

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
        if 'datavalue' in request.args:
            return get_datavalue_as_filecontent(int(request.args.get('datavalue')))
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
        logging.error(f"Unhandled Exception at executables: {str(e)}")
        return make_response(jsonify(err=str(e)), 500)

def get_functions(access):
    return json.dumps({'functions':  convert_to_safe_json(modulemanager.get_all_by_user_access(current_user.id, access))})

def get_service(name, package):
    services = list(modulemanager.get_modules_by_name_package(name=name, package=package))
    if not services or len(services) == 0:
        raise ValueError(f"{package}{'.' if package else ''}{name} service is not found")

    if services[0].value['module'].startswith("http://") or services[0].value['module'].startswith("https://"):
        import requests
        from urllib.parse import urljoin
        return json.dumps(requests.get(urljoin(services[0].value['module'], f'api/service?name={name}&package={package}')).json())
    
    return json.dumps(convert_to_safe_json(services[0].to_json()))
