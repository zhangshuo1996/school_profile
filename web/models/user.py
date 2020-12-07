from flask_login import UserMixin
from werkzeug.security import check_password_hash

from web.extensions import db
from .relation import user_role
from .permission import Permission
from .department import Department
from .agent import Agent
from .project import Project


class User(db.Model, UserMixin):
    """用户类"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), comment='用户名')
    telephone = db.Column(db.String(11), comment='手机号')
    password_hash = db.Column(db.String(128), comment='加密后的密码')
    open_id = db.Column(db.String(255), comment='微信登录时的唯一标识')
    position = db.Column(db.String(32), comment='职务， 政府用户如 局长/副局长/科长等，中介用户如 经理/职员等')
    org_id = db.Column(db.Integer, comment='中介/政府所属的组织机构')
    avatar = db.Column(db.VARCHAR(128), comment='用户头像')

    is_active = db.Column(db.Integer, comment='是否激活')
    # 外键
    category_id = db.Column(db.Integer, db.ForeignKey('user_category.id'))
    # 双向 多对多
    roles = db.relationship('Role', secondary=user_role, back_populates='users')
    # 用户类型
    category = db.relationship('UserCategory', uselist=False)

    def validate_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)

    def can(self, permission_name):
        """该用户是否有对应的权限"""
        permission = Permission.query.filter_by(name=permission_name).first()
        if permission is None or len(self.roles) == 0:
            return False
        # 是否有该权限
        ret = False
        for role in self.roles:
            if permission in role.permissions:
                ret = True
                break
        return ret

    def can_read(self, category, org_id, project_id=None, department_id=None):
        """
        限定范围，用户是否可以进行操作 读使用此逻辑
        :param category: ACTIVITY DECLARATION POLICY FILE_STORAGE
        :param org_id: 组织机构的id
        :param project_id: 对于某一个project
        :param department_id: 和project_id选其一
        :return: 是否有权限读 0代表没权限读 2代表ALL_*_READ 1代表*_READ
        """
        # 获取权限
        permission = Permission.query.filter(Permission.name == '{}_READ'.format(category)).first()
        all_permission = Permission.query.filter(Permission.name == 'ALL_{}_READ'.format(category)).first()
        # project_id和department_id选则其一，优先使用project_id
        if project_id is not None:
            project = Project.query.get(project_id)
            department_id = project.department_id

        for role in self.roles:
            if role.department_id == department_id:
                # 判断是否存在ALL_*_READ权限
                if all_permission is not None and all_permission in role.permissions:
                    return 2
                # 判断是否存在*_READ权限
                elif self.org_id == org_id and permission is not None and permission in role.permissions:
                    return 1
        return 0

    def can_write(self, category, org_id, project_id):
        """
        判断该用户的角色对应的所有权限中是否有该权限 permission
        :param category: ACTIVITY DECLARATION POLICY
        :param org_id: 组织机构的id
        :param project_id: 对于某一个project
        :return: 是否有权限写
        :return: True or False
        """
        if self.org_id != org_id:
            return False
        permission_name = '{}_WRITE'.format(category)
        permission = Permission.query.filter(Permission.name == permission_name).first()
        project = Project.query.get(project_id)
        if permission is None:
            return False
        for role in self.roles:
            if role.department_id == project.department_id and permission in role.permissions:
                return True
        return False

    def get_projects(self):
        """获取自己关注的project"""
        department_ids = []
        for role in self.roles:
            if role.department_id not in department_ids:
                department_ids.append(role.department_id)
        projects = Project.query.filter(Project.department_id.in_(department_ids))
        return projects

    @property
    def is_authenticated(self):
        return True

    @property
    def is_administrator(self):
        """判断当前用户是否有管理员角色"""
        # 也可使用 role.permissions  判断
        for role in self.roles:
            # if "GOV_ADMINISTRATOR" in role.permissions or "AGENT_ADMINISTRATOR" in role.permissions:
            #     return True
            if role.department_id is None:
                return True
        return False

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        """
        以Unicode形式返回用户的唯一标识符
        :return: str
        """
        return str(self.id)

    @property
    def org_name(self):
        """
        获取该用户对应的组织名
        :return:
        """
        if self.category == 1:
            org = Department.query.filter(Department.id == self.org_id).first()
        else:
            org = Agent.query.filter(Agent.id == self.org_id).first()
        return org.name if org else None

    def get_departments(self):
        """
        根据user id获取所属的角色，以及对应的department
        :return: [Department, ...]
        """
        roles = self.roles
        ids = [role.department_id for role in roles]
        departments = Department.query.filter(Department.id.in_(ids)).all()
        return departments
