from web.extensions import db


class Department(db.Model):
    """
    部门类
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(64), comment='部门简称')
    full_name = db.Column(db.VARCHAR(64), comment='部门全称')
    status = db.Column(db.Integer, comment='部门是否启用')

    projects = db.relationship("Project")
