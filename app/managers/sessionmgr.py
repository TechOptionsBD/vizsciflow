from config import Config

def py2neo_graph_session():
    from py2neo import Graph
    from flask import g
    
    try:
        if not hasattr(g, 'graph'):
            g.graph = Graph(Config.GRAPHDB, username=Config.GRAPHDB_USER, password=Config.GRAPHDB_PASSWORD)
    #        g.graph.schema.create_uniqueness_constraint('Workflow', 'workflow_id')
        return g.graph
    except:
        return Graph(Config.GRAPHDB, username=Config.GRAPHDB_USER, password=Config.GRAPHDB_PASSWORD)

def get_neo4j_session(driver):
    return driver.session(database=Config.GRAPHDB_DASTABASE) if Config.GRAPHDB_VERSION.startswith("4") else driver.session()

def neo4j_graph_session():
    from neo4j import GraphDatabase
    from flask import g
    
    driver = GraphDatabase.driver(Config.GRAPHDB, auth=(Config.GRAPHDB_USER, Config.GRAPHDB_PASSWORD))
    
    try:
        if not hasattr(g, 'graph'):
            g.graph = get_neo4j_session(driver)
    #        g.graph.schema.create_uniqueness_constraint('Workflow', 'workflow_id')
        return g.graph
    except:
        return get_neo4j_session(driver)

def elasticsearch_session():
    from elasticsearch import Elasticsearch
    from flask import g
    
    try:
        if hasattr(g, 'es'):
            g.es = Elasticsearch()
        return g.es
    except:
        return Elasticsearch()

class SessionManager():
    @staticmethod
    def session():
        if Config.DATA_MODE == 0:
            pass
        elif Config.DATA_MODE == 1:
            return py2neo_graph_session()
        elif Config.DATA_MODE == 2:
            return neo4j_graph_session()
        elif Config.DATA_MODE == 3:
            return elasticsearch_session()
