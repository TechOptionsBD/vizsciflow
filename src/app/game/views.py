from . import game
from flask import render_template
from flask_login import login_required, current_user
from .fetch import points_entry_latest, user_level, usage_history, streak, max_streak

@game.route('/dashboard')
@login_required
def dashboard():
    user = current_user.username
    points = points_entry_latest(user)
    level = user_level(points)
    usage_records = usage_history(user)
    streak_days = streak(usage_records)
    max_streak_days = max_streak(usage_records)
    return render_template(
        'dashboard.html',
        user=user,
        points_entry_latest=points,
        user_level=level,
        streak=streak_days,
        max_streak=max_streak_days
    )

