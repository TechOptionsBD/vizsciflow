from app.managers.mgrutil import ManagerUtility
from app.objectmodel.common import ActivityType

class ActivityManager:
    def __init__(self):
        self.persistance = ManagerUtility.Manage('activity')

    def get(self, **kwargs):
        return self.persistance.get(**kwargs)
    
    def first(self, **kwargs):
        return self.persistance.first(**kwargs)

    def get_last_modified_n(self, n, **kwargs):
        return self.persistance.get_last_modified_n(n, **kwargs)

    def create(self, user_id, type):
        return self.persistance.create(user_id, type = type)
        
activitymanager = ActivityManager()