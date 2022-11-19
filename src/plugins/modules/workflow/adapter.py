import os
from app.main.jobsview import run_biowl_internal

def run_workflow(context, *args, **kwargs):
    id = kwargs.pop('id', None)
    if not id:
        id = args[0]
    if not id:
        raise ValueError("No valid workflow.")
    
    return run_biowl_internal(id, context.user_id, None, kwargs)