from web.extensions import db
from .relation import role_permission


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), comment='权限名:activity:活动 declaration:政策申报 policy:政策')

    # 双向建立 拥有该权限的所有角色
    roles = db.relationship('Role', secondary=role_permission, back_populates='permissions')

    def __repr__(self):
        return '%s' % self.name
