from flask import current_app
from ..graphutil import GraphManager
from ..elasticutil import ElasticManager
from ..models import RelationalManager

class DBManager():
    def __init__(self):
        if current_app.config["DATA_MODE"] == 0:
            self.persistance = RelationalManager()
        elif current_app.config["DATA_MODE"] == 1 or current_app.config["DATA_MODE"] == 2:
            self.persistance = GraphManager()
        elif current_app.config["DATA_MODE"] == 3:
            self.persistance = ElasticManager()
    def clear(self):
        self.persistance.clear()
    def close(self):
        self.persistance.close()


dbmanager = DBManager()
