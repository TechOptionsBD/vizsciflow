from .. import db

def get_user_id(username):
    command = "SELECT * FROM public.users WHERE username = %(username)s"
    result = db.engine.execute(command, {"username": username})
    rows = result.mappings()
    row = rows.first()
    user_id = row["id"]
    return user_id

def points_entry_latest(username):
    user_id = get_user_id(username)
    command = "SELECT * FROM game_points WHERE user_id = %(id)s ORDER BY record_time DESC LIMIT 1;"
    result = db.engine.execute(command, {"id": user_id})
    rows = result.mappings()
    row = rows.first()
    points = row["points"]
    return points

def points_entry_all():
    return

def user_level():
    return "Novice"

def usage_history():
    return

def streak():
    return 7
