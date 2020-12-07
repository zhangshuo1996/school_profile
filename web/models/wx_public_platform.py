"""公众号相关的model"""
from web.extensions import db


# 入孵表单
class incubator_project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 申请人姓名
    name = db.Column(db.String(50))
    telephone = db.Column(db.String(20))
    unit = db.Column(db.String(50))
    project_name = db.Column(db.String(100))
    gmt_create = db.Column(db.DateTime)


# 活动或政策报名表
class sign_up(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100))
    name = db.Column(db.String(100))
    telephone = db.Column(db.String(20))
    unit = db.Column(db.String(50))
    category = db.Column(db.Integer)
    gmt_create = db.Column(db.DateTime)