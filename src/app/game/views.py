from . import game
from flask import render_template
from flask_login import login_required, current_user
from .fetch import points_entry_latest, user_level, streak

@game.route('/dashboard')
@login_required
def dashboard():
    user = current_user.username
    return render_template(
        'dashboard.html',
        user=user,
        points_entry_latest=points_entry_latest(user),
        user_level=user_level(),
        streak=streak()
    )

