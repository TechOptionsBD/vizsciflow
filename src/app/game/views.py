from . import game
from flask import render_template
from flask_login import login_required, current_user
from .fetch import points_entry_latest, user_level, streak

@game.route('/dashboard')
@login_required
def dashboard():
    user = current_user.username
    points = points_entry_latest(user)
    level = user_level(points)
    streak_days = streak(user)
    return render_template(
        'dashboard.html',
        user=user,
        points_entry_latest=points,
        user_level=level,
        streak=streak_days
    )

