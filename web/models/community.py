from web.extensions import db


class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer)
    patent_num = db.Column(db.Integer)
    engineer_num = db.Column(db.Integer)
    industry = db.Column(db.String(255))