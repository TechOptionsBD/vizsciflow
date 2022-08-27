from flask_login import AnonymousUserMixin
from . import login_manager

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
        user = usermanager.first(id = int(user_id))
        return user