from config import Config

if Config.DATA_MODE == 1:
    from app.objectmodel.models.py2neo_graphutil import *
elif Config.DATA_MODE == 2:
    from app.objectmodel.models.neo4j_graphutil import *

class Manager():
    @staticmethod
    def clear():
        graph().run("MATCH (n) DETACH DELETE n")

    @staticmethod
    def close():
        from flask import g
        from config import Config
        if hasattr(g, 'graph'):
            if Config.DATA_MODE == 2:
                g.graph.close()
            g.pop('graph')