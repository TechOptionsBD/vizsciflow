from config import Config

def graph_session():
    from py2neo import Graph
    from flask import g
    
    try:
        if 'graph' not in g:
            g.graph = Graph(Config.GRAPHDB, username=Config.GRAPHDB_USER, password=Config.GRAPHDB_PASSWORD)
    #        g.graph.schema.create_uniqueness_constraint('Workflow', 'workflow_id')
        return g.graph
    except:
        return Graph(Config.GRAPHDB, username=Config.GRAPHDB_USER, password=Config.GRAPHDB_PASSWORD)

class SessionManager():
    @staticmethod
    def session():
        if Config.DATA_MODE == 0:
            pass
        else:
            return graph_session()
    
    @staticmethod
    def clear_graphdb():
        if Config.DATA_MODE == 1:
            graph = SessionManager.session()
            graph.run("MATCH (n) DETACH DELETE n")