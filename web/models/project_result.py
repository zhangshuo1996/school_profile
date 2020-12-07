from web.extensions import db


class ProjectResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    ep_name = db.Column(db.String(100))
    year = db.Column(db.Integer)
    remarks = db.Column(db.String(64))
    uploader = db.Column(db.String(64))
    gmt_create = db.Column(db.Integer)
