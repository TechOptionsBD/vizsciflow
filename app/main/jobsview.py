import os
import json

from ..jobs import run_script, stop_script, sync_task_status_with_db, sync_task_status_with_db_for_user
from ..models import Runnable
from . import main
from flask_login import login_required, current_user
from flask import request, jsonify, current_app

from ..biowl.dsl.func_resolver import Library

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
            self.funcs.append({"package_name": f.package if f.package else "", "name": f.name, "internal": f.internal, "example": example, "example2": example2, "desc": f.desc if f.desc else "", "runmode": f.runmode if f.runmode else "", "level": f.level, "group": f.group if f.group else "", "user": f.user if f.user else "", "access": str(f.access) if f.access else "0"}) 

library = LibraryHelper()

def run_biowl(user_id, script, args, immediate = True, pygen = False):
    if immediate:
        try:
            result = run_script(user_id, library.library, script, args)
        except:
            result = {}            
        return json.dumps(result)
    else:
        run_script.delay(user_id, library.library, script, args)
        return json.dumps({})

@main.route('/functions', methods=['GET', 'POST'])
@login_required
def functions():
    if request.method == "POST":
        if request.form.get('script') or request.form.get('code'):
            script = request.form.get('script') if request.form.get('script') else request.form.get('code')
            args = request.form.get('args') if request.form.get('args') else ''
            immediate = request.form.get('immediate') == 'true'.lower() if request.form.get('immediate') else False
            pygen = True if request.form.get('code') else False
            return run_biowl(current_user.id, script, args, immediate, pygen)
        
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
                if file:
                    package = request.form.get('package')
                    this_path = os.path.dirname(os.path.abspath(__file__))
                    #os.chdir(this_path) #set dir of this file to current directory
                    app_path = os.path.dirname(this_path)
                    librariesdir = os.path.normpath(os.path.join(app_path, 'biowl/libraries'))
    
                    user_package_dir = os.path.normpath(os.path.join(librariesdir, 'users', current_user.username))
                    if not os.path.isdir(user_package_dir):
                        os.makedirs(user_package_dir)
                    
                    pkg_or_default = package if package else 'mylib'
                    path = Samples.unique_filename(user_package_dir, pkg_or_default, '')
                    if not os.path.isdir(path):
                        os.makedirs(path)

                    # Make the filename safe, remove unsupported chars
                    filename = secure_filename(file.filename)
                    temppath = os.path.join(tempfile.gettempdir(), filename)
                    if os.path.exists(temppath):
                        import uuid
                        temppath = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()), filename)
                    file.save(temppath)
                    
                    if zipfile.is_zipfile(temppath):
                        with zipfile.ZipFile(temppath,"r") as zip_ref:
                            zip_ref.extractall(path)
                    elif tarfile.is_tarfile(temppath):
                        with tarfile.open(temppath,"r") as tar_ref:
                            tar_ref.extractall(path)
                    else:
                        shutil.move(temppath, path)
                                        
                    base = Samples.unique_filename(path, pkg_or_default, 'json')
                    with open(base, 'w') as mapper:
                        mapper.write(request.form.get('mapper'))
                    
                    org = request.form.get('org')
                    pkgpath = str(pathlib.Path(path).relative_to(os.path.dirname(app_path)))
                    pkgpath = os.path.join(pkgpath, filename)
                    pkgpath = pkgpath.replace(os.sep, '.').rstrip('.py')
                    
                    access = 1 if request.form.get('access') and request.form.get('access').lower() == 'true'  else 2 
                    with open(base, 'r') as json_data:
                        data = json.load(json_data)
                        libraries = data["functions"]
                        for f in libraries:
                            if 'internal' in f and f['internal']:
                                if 'name' not in f:
                                    f['name'] = f['internal']
                            elif 'name' in f and f['name']:
                                if 'internal' not in f:
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
                        json.dump(data, f, indent=4)
                    library.reload()
                    
                    result['out'].append("Library successfully added.")
            except Exception as e:
                result['err'].append(str(e))
            return json.dumps(result)
        elif request.form.get('provenance'):
            fullpath = os.path.join(os.path.dirname(os.path.dirname(basedir)), "workflow.log")
            mime = mimetypes.guess_type(fullpath)[0]
            return send_from_directory(os.path.dirname(fullpath), os.path.basename(fullpath), mimetype=mime, as_attachment = mime is None )
    else:
        level = int(request.args.get('level')) if request.args.get('level') else 0
        access = int(request.args.get('access')) if request.args.get('access') else 0
        return get_functions(level, access)

def get_user_status(user_id):
    return jsonify(runnables =[i.to_json_info() for i in Runnable.query.filter(Runnable.user_id == user_id).order_by(Runnable.id)])

def get_task_status(task_id):
    runnable = Runnable.query.get(task_id)
    return json.dumps(runnable.to_json_log())
    
@main.route('/runnables', methods=['GET', 'POST'])
@login_required
def runnables():
    try:
        if request.args.get('id'):
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
                    run_biowl(current_user.id, runnable.script, runnable.arguments, False, False)    
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

def get_functions(level, access):
    funcs = []
    for func in library.funcs:
        if int(func['level']) <= level and func['access'] == str(access) and (access < 2 or (func['user'] and func['user'] == current_user.username)):
            funcs.append(func)
            
    return json.dumps({'functions':  funcs})