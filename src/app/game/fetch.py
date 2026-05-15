from .. import db
from datetime import datetime

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
    try:
        points = row["cumulative_points"]
    except TypeError:
        points = 0
    return points

def points_entry_all():
    return

def user_level(points):
    if points < 100:
        return "Novice"
    elif points < 200:
        return "Intermediate"
    else:
        return "Advanced"

def usage_history(username):
    user_id = get_user_id(username)
    command = "SELECT * FROM game_usage_history WHERE user_id = %(id)s ORDER BY record_time DESC;"
    result = db.engine.execute(command, {"id": user_id})
    rows = result.mappings().all()
    return rows

def consecutive(d1, d2):
    d1 = d1["record_time"].toordinal()
    d2 = d2["record_time"].toordinal()
    return d2 - d1 == 1

def streak(rows):
    i = 1
    while i < len(rows):
        if not consecutive(rows[i], rows[i - 1]):
            break
        i += 1
    return i

def max_streak(rows):
    max_streak_days = 0
    streak = 1
    i = 1
    for i in range(len(rows)):
        if not consecutive(rows[i], rows[i - 1]):
            streak = 1
        else:
            streak += 1
        if streak > max_streak_days:
            max_streak_days = streak
    return max_streak_days

def get_missions():
    missions_tmp = [{
        "id": 1,
        "completed": True,
        "title": "sample title 1",
        "description": "sample description 1",
        "tutorial": "sample tutorial 1",
        "points": 5
    }, {
        "id": 2,
        "completed": False,
        "title": "sample title 2",
        "description": "sample description 2",
        "tutorial": "sample tutorial 2",
        "points": 5
    }]
    return missions_tmp

