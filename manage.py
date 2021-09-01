#!/usr/bin/env python
import os
import json
from flask_restful import Api
from flask_restful.utils import cors
from flask_httpauth import HTTPBasicAuth
from flask import jsonify, request, make_response

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

from app import app, db
from flask_script import Manager, Server
from flask_migrate import Migrate

manager = Manager(app)
migrate = Migrate(app, db)

from app.objectmodel.common import Permission, convert_to_safe_json
from flask_script import Shell
from flask_migrate import MigrateCommand
from flask_login import login_user, logout_user, current_user
from app.main.views import load_data_sources_biowl
from app.main.jobsview import run_biowl, get_user_status, get_task_status, get_functions, save_and_run_workflow
from flask_cors import cross_origin

from app.managers.usermgr import usermanager
from app.managers.workflowmgr import workflowmanager

api = Api(app)
api.decorators=[cors.crossdomain(origin='*')]
auth = HTTPBasicAuth()

@app.teardown_appcontext
def close_db(error):
    from app.managers.dbmgr import dbmanager
    dbmanager.close()

@app.after_request
def after_request(response):
#    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@auth.verify_password
def verify_password(username, password):
    user = usermanager.get_by_email(username)
    if user is not None and user.verify_password(password):
        login_user(user)
        return True
    return False

@app.route('/api/datasources')
@cross_origin(supports_credentials=True)
@auth.login_required
def get_datasources():
    return jsonify({'datasources': load_data_sources_biowl(True) })

@app.route('/api/script', methods=['POST'])
@cross_origin(supports_credentials=True)
@auth.login_required
def run_script_api():
    try:
        script = request.json.get('script')
        args = request.json.get('args') if request.json.get('args') else ''
        immediate = request.json.get('immediate') == 'true'.lower() if request.json.get('immediate') else False
        return save_and_run_workflow(script, args, immediate)
    except Exception as e:
        return make_response(jsonify(err=str(e)), 500)
    finally:
        logout_user()
        
@app.route('/api/functions', methods=['GET'])
@cross_origin(supports_credentials=True)
@auth.login_required
def get_functions_api():
    try:
        return get_functions(0)
    finally:
        logout_user()

@app.route('/api/workflow', methods=['GET'])
@cross_origin(supports_credentials=True)
@auth.login_required
def get_workflows_api():
    '''
    Usage:
    /api/workflow?access=0&tags=curation
    '''
    try:
        tags = request.args.get('tags') if request.args.get('tags') else ''
        tags = tags.split(',') if tags else []
        access = request.args.get('access') if request.args.get('access') else ''
        return json.dumps({'samples': convert_to_safe_json(workflowmanager.get_workflows_as_list(int(access), *tags))})
    finally:
        logout_user()       
         
@app.route('/api/ver2/workflow', methods=['GET'])
@cross_origin(supports_credentials=True)
@auth.login_required
def get_workflows():
    '''
    written_by: Moksedul Islam
    Usage:
    This api returns workflow with it's property according to requested param(props).
    So it can be use for multi purpose.
    /api/workflow?info=<workflow_id>&props=id;name;desc&access=0
    '''
    try:
        props = request.args.get('props')
        props = props.split(",")
        if request.args.get('info'):
            workflow = workflowmanager.first(id = request.args.get('info'))
            workflow_list = (workflowmanager.get_a_workflow_details(workflow, props))
            return json.dumps(workflow_list)
        else:
            workflow_id = ''
            access = request.args.get('access') if request.args.get('access') else ''
            return workflowmanager.get_workflow_list(workflow_id, props, int(access))
    finally:
        logout_user()

@app.route('/api/run', methods=['GET'])
@cross_origin(supports_credentials=True)
@auth.login_required
def run_workflow_api():
    '''
    Usage:
    curl -H 'Content-Type: application/json'  -u mainulhossain@gmail.com:aaa -X GET -d '{"id":"332", "args":"data='/storage',data2='/storag22'"}' http://127.0.0.1:5000/api/run
    '''
    try:
        args = request.args.get('args') if request.args.get("args") else ''
        workflow_id = request.args.get('id')
        args = args.split(',')
        args = [arg for arg in args if arg]
                
        immediate = request.args.get('immediate').lower() == 'true' if request.args.get('immediate') else False
        runnable = run_biowl(workflow_id, None, args, immediate)
        return jsonify(runnableId = runnable.id)
    except Exception as e:
        return make_response(jsonify(err=str(e)), 500)
    finally:
        logout_user()
        
@app.route('/api/status', methods=['GET'])
@cross_origin(supports_credentials=True)
@auth.login_required
def get_status_api():
    '''
    Usage:
    curl -u mainulhossain@gmail.com:aaa -X GET  http://127.0.0.1:5000/api/status?id=7
    wget --user mainulhossain@gmail.com --password aaa "http://127.0.0.1:5000/api/status?id=7"
    '''
    runid = request.args.get('id') if request.args.get('id') else ''
    status = get_task_status(int(runid)) if runid else get_user_status(current_user.id)
    return status


def make_shell_context():
    return dict(app=app, db=db, User=usermanager.get_cls('user'), Follow=usermanager.get_cls('follow'), Role=usermanager.get_cls('role'),
                Permission=Permission, Post=usermanager.get_cls('post'), Comment=usermanager.get_cls('comment'))
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()

@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade

    # migrate database to latest revision
    upgrade()

    # create user roles
    usermanager.insert_roles()

    # create self-follows for all users
    usermanager.add_self_follows()

@manager.command
def createdb():
    db.drop_all()
    db.create_all()
    db.session.commit()

@manager.command
def deploydb():
    from app.managers.modulemgr import modulemanager
    from app.managers.datamgr import datamanager
    from app.managers.usermgr import usermanager
    from app.managers.usermgr import usermanager
    from app.managers.workflowmgr import workflowmanager
    from app.managers.dbmgr import dbmanager

    import logging
    logging.basicConfig(level = logging.INFO)

    # clear the database
    logging.info("Clearing the database...")
    dbmanager.clear()

    #create datasources
    logging.info("Inserting data sources...")
    datamanager.insert_datasources()

    #create user roles
    logging.info("Inserting roles...")
    usermanager.insert_roles()

    # insert test user
    logging.info("Creating users:...")
    usermanager.create_user(email="testuser@usask.ca", username="testuser", password="aaa")
    logging.info("testuser")
    # usermanager.create_user(email="mainulhossain@gmail.com", username="mainulhossain", password="aaa")
    # logging.info("mainulhossain")
    usermanager.create_user(email="admin@gmail.com", username="admin", password="Admin_1")
    logging.info("admin")
    
    # insert modules
    logging.info("Inserting modules from directory: {0} ...".format(app.config['MODULE_DIR']))
    modules = modulemanager.insert_modules(app.config['MODULE_DIR'])
    logging.info("{0} module(s) added:".format(len(modules)))
    for module in modules:
        package = module.package if module.package else "" # package name is optional
        logging.info(package + "." + module.name)

    # insert workflows
    logging.info("Inserting workflows from directory: {0} ...".format(app.config['WORKFLOW_DIR']))
    workflows = workflowmanager.insert_workflows(app.config['WORKFLOW_DIR'])
    logging.info("{0} workflows(s) added:".format(len(workflows)))
    for workflow in workflows:
        logging.info(workflow.name)

@manager.command
def insertmodules(path):
    from app.managers.modulemgr import modulemanager
    import logging
    
    logging.basicConfig(level = logging.INFO)
    logging.info("Inserting modules from directory: {0} ...".format(path))
    if not os.path.exists(path):
        logging.error("Path {0} doesn't exist".format(path))
        raise ValueError("Path {0} doesn't exist".format(path))
    
    modules = modulemanager.insert_modules(path)
    logging.info("{0} module(s) added:".format(len(modules)))
    for module in modules:
        logging.info(module.package + "." + module.name)

@manager.command
def insertworkflows(path):
    from app.managers.workflowmgr import workflowmanager
    import logging
    
    logging.basicConfig(level = logging.INFO)
    logging.info("Inserting workflows from directory: {0} ...".format(path))
    if not os.path.exists(path):
        logging.error("Path {0} doesn't exist".format(path))
        raise ValueError("Directory {0} doesn't exist".format(path))
    
    workflows = workflowmanager.insert_workflows(path)
    logging.info("{0} workflows(s) added:".format(len(workflows)))
    for workflow in workflows:
        logging.info(workflow.name)

if __name__ == '__main__':
##    written by: Moksedul Islam 
##    To run vizsciflow in different port as debugger mode. 
#    manager.add_command("runserver", Server(
#    use_debugger = True,
#    use_reloader = True,
#    host = '0.0.0.0',
#    port = 8080) )
    manager.run()
