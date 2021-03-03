from . import login_manager
from flask_login import AnonymousUserMixin

class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    WRITE_WORKFLOWS = 0x08
    MODERATE_COMMENTS = 0x10
    MODERATE_WORKFLOWS = 0x20
    ADMINISTER = 0x80

class AccessRights:
    NotSet = 0x00
    Read = 0x01
    Write = 0x02
    Owner = 0x07
    Request = 0x8
    
    @staticmethod
    def hasRight(rights, checkRight):
        if checkRight == 0:
            return rights == 0
        return (rights & checkRight) == checkRight
    
    @staticmethod
    def requested(rights):
        return AccessRights.Requested(rights, AccessRights.Request)
    
    @staticmethod
    def readRequested(rights):
        return AccessRights.Requested(rights) and (AccessRights.Requested(rights, AccessRights.Read) or AccessRights.Requested(rights, AccessRights.Write))
    
    @staticmethod
    def writeRequested(rights):
        return AccessRights.Requested(rights) and AccessRights.Requested(rights, AccessRights.Write)
    
    @staticmethod
    def rights_to_string(checkRights):
        if checkRights & AccessRights.Owner:
            return "Owner"
        
        rightStr = ""
        if checkRights & AccessRights.Request:
            rightStr = "Request"
        else:
            if checkRights & AccessRights.Read:
                rightStr = "Read"
            if checkRights & AccessRights.Write:
                rightStr += "Write"
            
        return rightStr

class AccessType:
    PUBLIC = 0
    SHARED = 1
    PRIVATE = 2

class Status:
    PENDING = 'PENDING'
    RECEIVED = 'RECEIVED'
    STARTED = 'STARTED'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    REVOKED = 'REVOKED'
    RETRY = 'RETRY'

class LogType:
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    from .managers.usermgr import usermanager
    if user_id and user_id.isdecimal() and user_id.isascii():
        return usermanager.get(id = int(user_id))