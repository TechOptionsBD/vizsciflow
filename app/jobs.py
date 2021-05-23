from app.main.jobsview import provenance
import sys
sys.path.insert(0, '../..') #modules are 2 layers above this location

from celery.contrib.abortable import AbortableTask

import os
import json
import logging
from pyparsing import ParseException

from config import Config

from . import celery
from dsl.grammar import PythonGrammar
from dsl.parser import WorkflowParser
from dsl.wftimer import Timer

from app.objectmodel.common import Status
from .managers.runmgr import runnablemanager
from .managers.workflowmgr import workflowmanager
from .biowl.dsl.vizsciflowinterpreter import VizSciFlowInterpreter
            
@celery.task(bind=True, base = AbortableTask)
def run_script(self, runnable_id, args, provenance):
    
    runnable = runnablemanager.first(id=runnable_id)

    machine = VizSciFlowInterpreter()
    context = machine.context

    parserdir = Config.BIOWL
    curdir = os.getcwd()
    os.chdir(parserdir) #set dir of this file to current directory

    try:

        context.runnable = runnable.id
        context.user_id = runnable.user_id
        context.provenance = provenance
        
        if self and self.request:
            runnable.celery_id = self.request.id
        runnable.set_status(Status.STARTED, True)

        with Timer() as t:
            parser = WorkflowParser(PythonGrammar())   
            if args:
                args_tokens = parser.parse_subgrammar(parser.grammar.arguments, args)
                if args_tokens:
                    machine.args_to_symtab(args_tokens) 
            prog = parser.parse(runnable.script)
            machine.run(prog)
                            
        runnable.set_status(Status.SUCCESS, False)
    except (ParseException, Exception) as e:
        logging.error(str(e))
        context.err.append(str(e))
        runnable.set_status(Status.FAILURE, False)
    finally:
        os.chdir(curdir)
        runnable.error = "\n".join(context.err)
        runnable.out = "\n".join(context.out)
        runnable.view = json.dumps(context.view if hasattr(context, 'view') else '')
        runnable.update()
        
    return runnable.to_json_log()

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
    from app.biowl.dsl.vizsciflowgraphgen import GraphGenerator
    return GraphGenerator.generate_workflow_graph_json(workflow_id, name, script)