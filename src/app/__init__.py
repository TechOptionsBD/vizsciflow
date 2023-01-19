import os

import click
from celery import Celery
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from config import config

##----2. Importing Global variables from the enviornment file.----
basedir = os.path.dirname(os.path.abspath(__file__))

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
migrate = Migrate()
pagedown = PageDown()
celery = Celery(__name__)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config.from_object(config[config_name])
    app.debug = app.config['DEBUG']

    envfile = os.path.join(os.path.dirname(basedir), '../.env') # now load the secret and system specific settings
    app.config.from_pyfile(envfile, silent=True)
    config[config_name].init_app(app)

    celery.conf.broker_url = app.config["CELERY_BROKER_URL"]
    celery.conf.result_backend = app.config["CELERY_RESULT_BACKEND"]

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    
    # if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
    #     from flask_sslify import SSLify
    #     sslify = SSLify(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

from werkzeug.utils import import_string
from celery.signals import worker_process_init, celeryd_init

def get_celery_conf():
    config = import_string('src.settings')
    config = {k: getattr(config, k) for k in dir(config) if k.isupper()}
    config['BROKER_URL'] = config['CELERY_BROKER_URL']
    return config

@celeryd_init.connect
def init_celeryd(conf=None, **kwargs):
    conf.update(get_celery_conf())

@worker_process_init.connect
def init_celery_flask_app(**kwargs):
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    app.app_context().push()