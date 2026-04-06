from . import game
from flask import render_template
from flask_login import login_required, current_user
from .fetch import points_entry_latest, user_level, streak

@game.route('/dashboard')
@login_required
def dashboard():
    return render_template(
        'dashboard.html',
        user=current_user.username,
        points_entry_latest=points_entry_latest(),
        user_level=user_level(),
        streak=streak()
    )

