from celery.contrib.abortable import AbortableTask, AbortableAsyncResult
from celery.states import state, PENDING, SUCCESS

from flask_login import current_user
from flask import has_request_context, g, request, make_response
from datetime import datetime
import os
import random
import time
import json

from config import Config
from . import celery
from .biowl.dsl.parser import PhenoWLParser, PythonGrammar
from .biowl.dsl.interpreter import Interpreter
from .biowl.timer import Timer
from .models import Runnable, Status


class ContextTask(AbortableTask):
    abstract = True
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc)) # log to runnables by task_id
    def __call__(self, *args, **kwargs):
        app = create_app(os.getenv('FLASK_CONFIG') or 'default')
        app.config['CURRENT_USER'] = 'phenoproc' #current_user.username
        with app.app_context():
            return AbortableTask.__call__(self, *args, **kwargs)

# class RequestContextTask(AbortableTask):
#     """Celery task running within Flask test request context.
#     Expects the associated Flask application to be set on the bound
#     Celery application.
#     """
#     abstract = True
#     def __call__(self, *args, **kwargs):
#         """Execute task."""
#         with self.app.flask_app.test_request_context():
#             self.app.flask_app.try_trigger_before_first_request_functions()
#             self.app.flask_app.preprocess_request()
#             res = AbortableTask.__call__(self, *args, **kwargs)
#             self.app.flask_app.process_response(
#                 self.app.flask_app.response_class())
#             return res
   
__all__ = ['RequestContextTask']


class RequestContextTask(AbortableTask):
    """Base class for tasks that originate from Flask request handlers
    and carry over most of the request context data.
    This has an advantage of being able to access all the usual information
    that the HTTP request has and use them within the task. Pontential
    use cases include e.g. formatting URLs for external use in emails sent
    by tasks.
    """
    abstract = True

    #: Name of the additional parameter passed to tasks
    #: that contains information about the original Flask request context.
    CONTEXT_ARG_NAME = '_flask_request_context'
    GLOBALS_ARG_NAME = '_flask_global_proxy'
    GLOBAL_KEYS = ['user']

    def __call__(self, *args, **kwargs):
        """Execute task code with given arguments."""
        call = lambda: super(RequestContextTask, self).__call__(*args, **kwargs)

        # set context
        context = kwargs.pop(self.CONTEXT_ARG_NAME, None)
        gl = kwargs.pop(self.GLOBALS_ARG_NAME, {})

        if context is None or has_request_context():
            return call()

        from app import app
        with app.test_request_context(**context):
            # set globals
            for i in gl:
                setattr(g, i, gl[i])
            # call
            result = call()
            # process a fake "Response" so that
            # ``@after_request`` hooks are executed
            #app.process_response(make_response(result or ''))

        return result

    def apply_async(self, args=None, kwargs=None, **rest):
        self._include_request_context(kwargs)
        self._include_global(kwargs)
        return super(RequestContextTask, self).apply_async(args, kwargs, **rest)

    def apply(self, args=None, kwargs=None, **rest):
        self._include_request_context(kwargs)
        self._include_global(kwargs)
        return super(RequestContextTask, self).apply(args, kwargs, **rest)

    def retry(self, args=None, kwargs=None, **rest):
        self._include_request_context(kwargs)
        self._include_global(kwargs)
        return super(RequestContextTask, self).retry(args, kwargs, **rest)

    def _include_request_context(self, kwargs):
        """Includes all the information about current Flask request context
        as an additional argument to the task.
        """
        if not has_request_context():
            return

        # keys correspond to arguments of :meth:`Flask.test_request_context`
        context = {
            'path': request.path,
            'base_url': request.url_root,
            'method': request.method,
            'headers': dict(request.headers),
        }
        if '?' in request.url:
            context['query_string'] = request.url[(request.url.find('?') + 1):]

        kwargs[self.CONTEXT_ARG_NAME] = context

    def _include_global(self, kwargs):
        d = {}
        for z in self.GLOBAL_KEYS:
            if hasattr(g, z):
                d[z] = getattr(g, z)
        kwargs[self.GLOBALS_ARG_NAME] = d
             
@celery.task(bind=True, base=RequestContextTask)#, base = AbortableTask
def run_script(self, user_id, library, script, args):
    parserdir = Config.BIOWL
    curdir = os.getcwd()
    os.chdir(parserdir) #set dir of this file to current directory
    duration = 0
    
    runnable = Runnable.create_runnable(user_id)
    runnable.script = script
    runnable.name = script[:min(40, len(script))]
    if len(script) > len(runnable.name):
        runnable.name += "..."
    runnable.arguments = args
    runnable.update()

    machine = Interpreter()
    try:
        
        machine.context.library = library
        machine.context.runnable = runnable.id
        
        if self and self.request:
            runnable.celery_id = self.request.id
        runnable.update_status(Status.STARTED)

        parser = PhenoWLParser(PythonGrammar())   
        with Timer() as t:
            if args:
                args_tokens = parser.parse_subgrammar(parser.grammar.arguments, args)
                machine.args_to_symtab(args_tokens) 
            prog = parser.parse(script)
            machine.run(prog)                
        duration = float("{0:.3f}".format(t.secs))

        runnable.status = Status.SUCCESS
    except Exception as e:
        runnable.status = Status.FAILURE
        machine.context.err.append(str(e))
    finally:
        os.chdir(curdir)
        runnable.duration = duration
        runnable.err = "\n".join(machine.context.err)
        runnable.out = "\n".join(machine.context.out)
        runnable.update()
        
    return runnable.to_json_log()

def stop_script(task_id):
#     abortable_task = AbortableAsyncResult(task_id)
#     abortable_task.abort()
    from celery import current_app
    celery.control.revoke(task_id, terminate=True)

def sync_task_status_with_db(task):
    if task.celery_id is not None and task.status != 'FAILURE' and task.status != 'SUCCESS' and task.status != 'REVOKED':
        celeryTask = run_script.AsyncResult(task.celery_id)
        task.status = celeryTask.state
        
        if celeryTask.state != 'PENDING':
            if celeryTask.state != 'FAILURE' and celeryTask.state != 'REVOKED':
                task.out = "\n".join(celeryTask.info.get('out'))
                task.err = "\n".join(celeryTask.info.get('err'))
                task.duration = int(celeryTask.info.get('duration'))
            else:
                task.err = str(celeryTask.info)
        task.update()

    return task.status
    
def sync_task_status_with_db_for_user(user_id):
    tasks = Runnable.query.filter(Runnable.user_id == user_id)
    for task in tasks:
        if not task.completed():
            sync_task_status_with_db(task)