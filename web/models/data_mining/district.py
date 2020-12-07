from web.extensions import db


class District(db.Model):
    """行政划分"""
    __bind_key__ = 'data_mining'
    id = db.Column(db.Integer, primary_key=True)
    province = db.Column(db.String(32), comment='省份')
    city = db.Column(db.String(32), comment='市')
    country = db.Column(db.String(32), comment='县')
    town = db.Column(db.String(32), comment='区/镇')
