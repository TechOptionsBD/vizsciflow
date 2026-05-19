from .db import *

class GamePointsManager():
    @staticmethod
    def retrieve_cumulative_points(user_id):
        row = (
            GamePoints.query
            .filter_by(user_id = user_id)
            .order_by(GamePoints.record_time.desc())
            .first()
        )
        if not row:
            return 0
        return row.cumulative_points

class GameUsageHistoryManager():
    @staticmethod
    def retrieve_usage_history(user_id):
        rows = (
            GameUsageHistory.query
            .filter_by(user_id = user_id)
            .order_by(GameUsageHistory.record_time.desc())
        )
        return rows.all()

