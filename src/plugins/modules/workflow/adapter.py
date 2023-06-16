import os
from app.main.jobsview import run_biowl_internal

def run_workflow(context, *args, **kwargs):
    id = kwargs.pop('id', None)
    if not id:
        if not args:
            raise ValueError("No workflow id is given.")
        id = int(args[0])
    return run_biowl_internal(id, context.user_id, None, kwargs)