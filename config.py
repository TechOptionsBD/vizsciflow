import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    ROOT_DIR = basedir
    DATA_DIR = os.path.join(ROOT_DIR, 'storage')
    PUBLIC_DIR = 'public'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #for provenance
    PLUGIN_DIR = os.path.join(ROOT_DIR, 'plugins')
    MODULE_DIR = os.path.join(PLUGIN_DIR, 'modules')
    PROVENANCE_DIR = os.path.join(PLUGIN_DIR, 'provs')
    PROVENANCE_PACKAGE = 'plugins.provs'
    MODULE_PACKAGE = 'plugins.modules'
    WORKFLOW_DIR = os.path.join(ROOT_DIR, 'workflows/samples')
    WORKFLOW_VERSIONS_DIR = os.path.join(ROOT_DIR, 'workflows/versions')
    HTML_DIR = os.path.join(ROOT_DIR, 'app/templates/plugins')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    BIOWL = os.path.join(ROOT_DIR, 'app/dsl/')
    PHENOPROC_MAIL_SUBJECT_PREFIX = '[Phenoproc]'
    PHENOPROC_MAIL_SENDER = 'Phenoproc Admin <phenoproc@gmail.com>'
    PHENOPROC_ADMIN = os.environ.get('PHENOPROC_ADMIN')         
    PHENOPROC_POSTS_PER_PAGE = 20
    PHENOPROC_FOLLOWERS_PER_PAGE = 50
    PHENOPROC_COMMENTS_PER_PAGE = 30
    PHENOPROC_SLOW_DB_QUERY_TIME=0.5
    WORKFLOW_MODE_EDIT = False
    ENV_DATABASE_URL = "postgresql+psycopg2://phenodoop:sr-hadoop@localhost:5432/biowl"
    GRAPHDB = 'bolt://localhost:7687'
    GRAPHDB_USER = 'neo4j'
    GRAPHDB_PASSWORD = 'sr-hadoop'
    GRAPHDB_DASTABASE = ''#'vizsciflow'
    GRAPHDB_VERSION = ''
    DATA_MODE = 0 # 0 = DB, 1 = Graph (py2neo), 2 = Graph (neo4j-driver) 3 = Elastic Search
    USE_GIT = False
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('ENV_DATABASE_URL') or Config.ENV_DATABASE_URL
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('ENV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False

class DockerConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('ENV_DATABASE_URL') or "postgresql+psycopg2://phenodoop:sr-hadoop@vizsciflowdb:5432/biowl"
    CELERY_BROKER_URL = 'redis://vizsciflowredis:6379/0'
    CELERY_RESULT_BACKEND = 'redis://vizsciflowredis:6379/0'
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('ENV_DATABASE_URL') or Config.ENV_DATABASE_URL

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.PHENOPROC_MAIL_SENDER,
            toaddrs=[cls.PHENOPROC_ADMIN],
            subject=cls.PHENOPROC_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'unix': UnixConfig,
    'docker': DockerConfig,

    'default': DevelopmentConfig
}
