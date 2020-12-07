from web.extensions import db


class ActivityParticipate:
    engineer_id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, primary_key=True)