from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors, jobsview
from app.objectmodel.common import Permission

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
