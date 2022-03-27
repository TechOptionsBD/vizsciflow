from flask import current_app
from app.managers.mgrutil import ManagerUtility

class DBManager():
    def __init__(self):
        self.persistance = ManagerUtility.Manage('manager')

    def create(self):
        self.persistance.create()
    def clear(self):
        self.persistance.clear()
    def close(self):
        self.persistance.close()

dbmanager = DBManager()
