from config import Config
from .managers.sessionmgr import SessionManager

if Config.DATA_MODE == 1:
    from .py2neo_graphutil import *
else:
    from .neo4j_graphutil import *

class GraphManager():
    @staticmethod
    def clear():
        SessionManager.session().run("MATCH (n) DETACH DELETE n")

    @staticmethod
    def close():
        from flask import g
        from config import Config
        if hasattr(g, 'graph'):
            if Config.DATA_MODE == 2:
                g.graph.close()
            g.pop('graph')