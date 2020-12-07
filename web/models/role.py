from web.extensions import db
from .relation import user_role, role_permission


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), comment='TODO：角色名待删除')
    category = db.Column(db.Integer)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    # 双向建立 即permission会默认有一个roles属性，表示拥有该权限的所有角色
    permissions = db.relationship('Permission', secondary=role_permission, back_populates='roles')
    # 双向建立，表示拥有此角色的用户列表
    users = db.relationship('User', secondary=user_role, back_populates='roles')

    department = db.relationship("Department")

    def __str__(self):
        return '%s %s' % (self.name, self.department_id)

    def __repr__(self):
        return '%s %s' % (self.name, self.department_id)
