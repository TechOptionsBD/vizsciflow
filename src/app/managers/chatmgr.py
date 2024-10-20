from app.managers.mgrutil import ManagerUtility

class ChatManager():
    def __init__(self):
        self.persistance = ManagerUtility.Manage('chat')
    
    def first(self, **kwargs):
        return self.persistance.first(**kwargs)

    def get(self, **kwargs):
        return self.persistance.get(**kwargs)

    def add(self, **kwargs):
        return self.persistance.add(**kwargs)

    def remove(self, id):
        self.persistance.remove(id)
    
chatmanager = ChatManager()
