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

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import app, db
from flask_script import Manager
from flask_migrate import Migrate

manager = Manager(app)
migrate = Migrate(app, db)

from app.models import User, Follow, Role, Permission, Post, Comment
from flask_script import Shell
from flask_migrate import MigrateCommand
from flask_login import login_user, logout_user, current_user
from app.main.views import Samples, load_data_sources_biowl
from app.main.jobsview import run_biowl, get_user_status, get_task_status, get_functions, save_and_run_workflow
from flask_cors import cross_origin

api = Api(app)
api.decorators=[cors.crossdomain(origin='*')]
auth = HTTPBasicAuth()

@app.after_request
def after_request(response):
#    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(email=username).first()
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
        return Samples.get_samples_as_list(int(access), *tags)
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
        runnable = run_biowl(workflow_id, '', args, immediate)
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
    return dict(app=app, db=db, User=User, Follow=Follow, Role=Role,
                Permission=Permission, Post=Post, Comment=Comment)
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
    from app.models import Role, User

    # migrate database to latest revision
    upgrade()

    # create user roles
    Role.insert_roles()

    # create self-follows for all users
    User.add_self_follows()


if __name__ == '__main__':
    manager.run()