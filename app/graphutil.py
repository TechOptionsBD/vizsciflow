from config import Config

if Config.DATA_MODE == 1:
    from .py2neo_graphutil import *
else:
    from .neo4j_graphutil import *