import os

from celery import Celery
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_pagedown import PageDown
import flask_sijax
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from config import config, Config


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
celery = Celery(__name__, broker=Config.broker_url, backend=Config.result_backend)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.debug = True
    
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    celery.conf.update(app.config)
    
    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    app.config['SIJAX_STATIC_PATH'] = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
    app.config['SIJAX_JSON_URI'] = '/static/js/sijax/json2.js'
    flask_sijax.Sijax(app)

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