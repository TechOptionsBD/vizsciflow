import sys
sys.path.insert(0, '../..') #modules are 2 layers above this location

from celery.contrib.abortable import AbortableTask

import os
import json
import logging
from pyparsing import ParseException
from timeit import time

from . import celery
from dsl.parser import WorkflowParser

from app.objectmodel.common import Status
from app.managers.runmgr import runnablemanager
from app.managers.workflowmgr import workflowmanager
from app.dsl.vizsciflowgrammar import VizSciFlowGrammar
from app.dsl.vizsciflowinterpreter import VizSciFlowInterpreter
from app.dsl.vizsciflowlib import Library

@celery.task(bind=True, base = AbortableTask)
def run_script(self, runnable_id, args, provenance):
    from app import app
    
    ts = time.perf_counter()
    runnable = runnablemanager.first(id=runnable_id)

    machine = VizSciFlowInterpreter()
    context = machine.context

    parserdir = app.config['BIOWL']
    curdir = os.getcwd()
    os.chdir(parserdir) #set dir of this file to current directory

    retval = None
    try:

        context.runnable = runnable.id
        context.user_id = runnable.user_id
        context.provenance = provenance
        
        if self and self.request:
            runnable.celery_id = self.request.id
        runnable.set_status(Status.STARTED, True)

        parser = WorkflowParser(VizSciFlowGrammar())   
        if args:
            args_tokens = parser.parse_subgrammar(parser.grammar.arguments, args)
            if args_tokens:
                machine.args_to_symtab(args_tokens) 
        prog = parser.parse(runnable.script)
        retval = machine.run(prog)

        Library.add_runnable_returns(context, retval, workflowmanager.get_returns_json(runnable.workflow.id))

        runnable.set_status(Status.SUCCESS, False)
    except (ParseException, Exception) as e:
        logging.error(str(e))
        context.err.append(str(e))
        runnable.set_status(Status.FAILURE, False)
        raise
    finally:
        os.chdir(curdir)
        runnable.error = "\n".join(context.err)
        runnable.out = "\n".join(context.out)
        runnable.view = json.dumps(context.view if hasattr(context, 'view') else '')
        runnable.duration = (time.perf_counter() - ts) * 1000
        runnable.update()
        
    return retval

def stop_script(task_id):
#    from celery.contrib.abortable import AbortableAsyncResult
#     abortable_task = AbortableAsyncResult(task_id)
#     abortable_task.abort()
#    from celery import current_app
    celery.control.revoke(task_id, terminate=True)

def sync_task_status_with_db(runnable):
    if runnable.celery_id and not runnable.completed:
        celeryTask = run_script.AsyncResult(runnable.celery_id)
        runnable.set_status(celeryTask.state, False)
        
        if celeryTask.state != 'PENDING':
            if celeryTask.state != 'FAILURE' and celeryTask.state != 'REVOKED':
                runnable.out = "\n".join(celeryTask.info.get('out'))
                runnable.err = "\n".join(celeryTask.info.get('err'))
                runnable.duration = int(celeryTask.info.get('duration'))
            else:
                runnable.err = str(celeryTask.info)
        runnable.update()

    return runnable.status
    
def sync_task_status_with_db_for_user(user_id):
    runnables = runnablemanager.runnables_of_user(user_id)
    for runnable in runnables:
        if not runnable.completed:
            sync_task_status_with_db(runnable)

def generate_graph_from_workflow(workflow_id):

    workflow = workflowmanager.first(id = workflow_id)
    return generate_graph(workflow.id, workflow.name, workflow.script)

def generate_graph(workflow_id, name, script):
    from app.dsl.vizsciflowgraphgen import GraphGenerator
    return GraphGenerator.generate_workflow_graph_json(workflow_id, name, script)