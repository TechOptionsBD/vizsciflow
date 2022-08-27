from app.managers.mgrutil import ManagerUtility

class FilterManager():
    def __init__(self):
        self.persistance = ManagerUtility.Manage('filter')
    
    def first(self, **kwargs):
        return self.persistance.first(**kwargs)

    def get(self, **kwargs):
        return self.persistance.get(**kwargs)

    def add(self, **kwargs):
        return self.persistance.add(**kwargs)

    def remove(self, id):
        self.persistance.remove(id)
    
    def make_script(self, id, path):
        filterjson = self.get(id = id).value
        filterjson = [f for f in filterjson if f["selected"] ]
        return  "data = GetFiles('{0}', {1})".format(path, filterjson)
    
    def get_first_history(self, **kwargs):
        return self.persistance.get_history(**kwargs).first()

    def get_history(self, **kwargs):
        return self.persistance.get_history(**kwargs)
    
filtermanager = FilterManager()