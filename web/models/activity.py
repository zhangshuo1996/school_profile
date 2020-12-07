import time
from web.extensions import db
from web.utils import timestamp2day
from .project import Project


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(32), comment='负责人名称')
    sponsor_id = db.Column(db.Integer, comment='主办方id')
    sponsor_name = db.Column(db.String(32), comment='主办方名称')
    title = db.Column(db.String(255), comment='活动名称')
    gmt_create = db.Column(db.Integer, default=time.time, comment='创建时间')
    gmt_start = db.Column(db.Integer, comment='活动开始时间')
    gmt_end = db.Column(db.Integer, comment='活动结束时间')
    address = db.Column(db.String(255), comment='活动地址')
    description = db.Column(db.Text, comment='活动简介')

    project_id = db.Column(db.Integer, comment='活动对应的项目id')
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def create_time(self):
        return timestamp2day(self.gmt_create)

    @property
    def project_name(self):
        project = Project.query.get(self.project_id)
        return project.name
