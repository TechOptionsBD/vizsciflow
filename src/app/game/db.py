from app import db

class GamePoints(db.Model):
    __tablename__ = 'game_points'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    mission_id = db.Column(db.Integer, nullable=False)
    cumulative_points = db.Column(db.Integer, nullable=False)
    record_time = db.Column(db.DateTime)

class GameUsageHistory(db.Model):
    __tablename__ = 'game_usage_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    record_time = db.Column(db.DateTime)

