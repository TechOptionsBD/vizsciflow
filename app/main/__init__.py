from flask import Blueprint

main = Blueprint('main', __name__)

from config import Config
from . import views, errors, jobsview
from ..common import Permission

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
