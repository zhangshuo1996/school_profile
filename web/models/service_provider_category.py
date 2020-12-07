from web.extensions import db


class ServiceProviderCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), comment="服务商类别")
