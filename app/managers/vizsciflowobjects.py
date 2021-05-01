from config import Config

if Config.DATA_MODE == 0:
    from ..models import *
elif Config.DATA_MODE == 1:
    from ..py2neo_graphutil import *
elif Config.DATA_MODE == 2:
    from ..neo4j_graphutil import *
elif Config.DATA_MODE == 3:
    from ..elasticutil import *