from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from werkzeug.security import generate_password_hash

from web.decorators import permission_required
from web.models import Role, UserCategory, Permission, Department, User, Agent
from web.extensions import db

# 地址前缀/admin/system
from web.service.admin import get_user

system_bp = Blueprint("system", __name__)


@system_bp.route("/role_list/")
@permission_required("SYSTEM_ADMINISTRATOR")
@login_required
def role_list():
    roles = Role.query.all()
    categories = UserCategory.query.all()
    data = []
    for role in roles:
        role_info = role.__dict__
        per_list = []
        for item in role.permissions:
            per_list.append(item.name)
        role_info['permission'] = per_list
        data.append(role_info)
    return render_template("/admin/system/role_list.html", data=data, categories=categories)


@system_bp.route("/role_add/", methods=['POST', 'GET'])
@permission_required("SYSTEM_ADMINISTRATOR")
@login_required
def role_add():
    if request.method == 'GET':
        categories = UserCategory.query.all()
        permissions = Permission.query.all()
        departments = [{'id': 0, 'name': "无"}] + Department.query.all()
        return render_template('admin/system/new_role.html', categories=categories, permissions=permissions,
                               departments=departments)
    elif request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        depart = int(request.form.get('department'))
        department = depart if depart != 0 else None

        permissions = request.form.getlist('permissions[]')
        new_role = Role(name=name, category=category, department_id=department)
        try:
            db.session.add(new_role)
            db.session.commit()
            role = Role.query.filter_by(name=name).first()
            for permission in permissions:
                permission = int(permission)
                permission_obj = Permission.query.filter_by(id=permission).first()
                role.permissions.append(permission_obj)
            db.session.commit()
            flash("新建角色成功", "success")
            return redirect(url_for('system.role_list'))
        except:
            flash("新建角色失败", "danger")
            return redirect(url_for('system.role_add'))


@system_bp.route("/role_modify/<int:role_id>", methods=['POST', 'GET'])
@permission_required("SYSTEM_ADMINISTRATOR")
@login_required
def role_modify(role_id):
    if request.method == 'GET':
        categories = UserCategory.query.all()
        permissions = Permission.query.all()
        departments = Department.query.all()
        departments = [{'id': 0, 'name': "无"}]+departments

        role = Role.query.filter_by(id=role_id).first()
        role_info = {}
        role_info['id'] = role_id
        role_info['name'] = role.name
        role_info['category'] = role.category
        role_info['department'] = role.department_id
        role_info['permissions'] = [permission.id for permission in role.permissions]

        return render_template('admin/system/edit_role.html', role=role_info, categories=categories,
                               permissions=permissions, departments=departments)
    elif request.method == 'POST':
        role = Role.query.filter_by(id=role_id).first()
        role.name = request.form.get('name')
        role.category = request.form.get('category')
        depart = int(request.form.get('department'))
        role.department_id = depart if depart != 0 else None
        permissions = request.form.getlist('permissions[]')
        role.permissions = []
        for permission in permissions:
            permission = int(permission)
            permission_obj = Permission.query.filter_by(id=permission).first()
            role.permissions.append(permission_obj)
        try:
            db.session.commit()
            flash("修改角色信息成功", "success")
            return redirect(url_for('system.role_list'))
        except:
            flash("修改角色信息失败", "danger")
            return redirect(url_for('system.role_modify', role_id=role.id))


'''@system_bp.route("/role_delete/<int:role_id>", methods=['POST'])
@permission_required("SYSTEM_ADMINISTRATOR")
@login_required
def role_delete(role_id):
    role = Role.query.filter_by(id=role_id).first()
    try:
        role.permissions = []
        role.users = []
        db.session.delete(role)
        db.session.commit()
        flash("删除角色成功", "success")
        return redirect(url_for('system.role_list'))
    except:
        flash("删除角色失败", "danger")
        return redirect(url_for('system.role_list'))'''


# 管理员模块
@system_bp.route('/user_list/', methods=['GET'])
@permission_required("SYSTEM_ADMINISTRATOR")
@login_required
def user_list():
    # 从数据库获取类别信息
    category_obj = UserCategory.query.all()
    category_data = [{"id": 0, "name": "全部类别"}]
    for category in category_obj:
        category_dict = {}
        category_dict['id'] = category.id
        category_dict['name'] = category.name
        category_data.append(category_dict)
    # 获取筛选条件
    name = request.args.get('name', "")
    phone = request.args.get('phone', "")
    category = int(request.args.get('category', 0))
    org = request.args.get('org', "")
    is_admin = int(request.args.get('is_admin', 1))

    users = get_user(name=name, phone=phone, category=category, org=org, is_admin=is_admin)
    user_list = []
    for user in users:
        user_info = {}
        user_info['id'] = user.id
        user_info['name'] = user.name
        user_info['telephone'] = user.telephone
        user_info['category'] = user.category_id
        user_info['position'] = user.position
        user_info['is_admin'] = "是" if is_admin else "否"
        if user_info['category'] == 2:  # 中介用户
            try:
                user_info['org'] = Agent.query.filter_by(id=user.org_id).first().name
            except:
                user_info['org'] = ""
        elif user_info['category'] == 1:    # 政府用户
            try:
                user_info['org'] = Department.query.filter_by(id=user.org_id).first().name
            except:
                user_info['org'] = ""
        else:   # 系统管理员
            user_info['org'] = ""
        user_list.append(user_info)
    return render_template('admin/system/user_list.html', admins=user_list, category_data=category_data,
                           name=name, phone=phone, category_id=category, org=org, is_admin=is_admin)


@system_bp.route('/assign_admin/<int:user_id>', methods=['POST'])
@permission_required("SYSTEM_ADMINISTRATOR")
@login_required
def assign_admin(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user.category_id == 1:
        gov_admin_role = Role.query.filter_by(name="科技局-管理员").first()
        user.roles.append(gov_admin_role)
    elif user.category_id == 2:
        agent_admin_role = Role.query.filter_by(name="中介-管理员").first()
        user.roles.append(agent_admin_role)
    elif user.category_id == 3:
        system_admin_role = Role.query.filter_by(name="系统管理员").first()
        user.roles.append(system_admin_role)
    try:
        db.session.commit()
        flash("授予管理员权限成功", "success")
    except:
        flash("授予管理员权限失败", "danger")
    return redirect(url_for("system.user_list"))


@system_bp.route('/admin_add/', methods=['GET', 'POST'])
@permission_required("SYSTEM_ADMINISTRATOR")
@login_required
def admin_add():
    if request.method == 'GET':
        departments = Department.query.all()
        department_list = []
        for department in departments:
            department_list.append(department.name)
        return render_template('admin/system/new_administrator.html', department_list=department_list)
    elif request.method == 'POST':
        user = User()
        user.category_id = int(request.form.get('categorization'))

        user.name = request.form.get('name')
        user.telephone = request.form.get('telephone')
        user.password_hash = generate_password_hash(request.form.get('password'))
        user.position = request.form.get('position')
        user.is_active = 1
        user.avatar = "default.jpg"

        if user.category_id == 1:
            if int(request.form.get('department')) != 0:
                user.org_id = int(request.form.get('department'))
        elif user.category_id == 2:
            agent = Agent.query.filter_by(name=request.form.get('agentname')).first()
            try:
                user.org_id = agent.id
            except:
                flash("新建管理员失败", "danger")
                return redirect(url_for('system.admin_add'))
        elif user.category_id == 3:
            user.org_id = 0

        try:
            db.session.add(user)
            db.session.commit()
            new_user = User.query.filter_by(telephone=request.form.get('telephone')).first()
            if user.category_id == 1:
                role_obj = Role.query.filter_by(name="科技局-管理员").first()
            elif user.category_id == 2:
                role_obj = Role.query.filter_by(name="中介-管理员").first()
            elif user.category_id == 3:
                role_obj = Role.query.filter_by(name="系统管理员").first()
            new_user.roles.append(role_obj)
            db.session.commit()
            flash("新建管理员成功", "success")
            return redirect(url_for('system.user_list', is_admin=1))
        except:
            flash("新建管理员失败", "danger")
            return redirect(url_for('system.admin_add'))


@system_bp.route('/admin_delete/<int:id>', methods=['POST'])
@permission_required("SYSTEM_ADMINISTRATOR")
@login_required
def admin_delete(id):
    user = User.query.filter_by(id=id).first()
    for role in user.roles:
        if role.name in ["科技局-管理员", "中介-管理员", "系统管理员"]:
            user.roles.remove(role)
    try:
        db.session.commit()
        flash("收回管理员权限成功", "success")
    except:
        flash("收回管理员权限失败")
    return redirect(url_for('system.user_list', is_admin=0))


@system_bp.route('/telephone_verify/', methods=['GET'])
@login_required
def telephone_verify():
    result = {'code': '1', 'data': '手机号可以使用'}
    telephone = request.args.get('telephone')
    count = User.query.filter_by(telephone=telephone).count()
    if count == 1:
        result["code"] = 0
        result["data"] = '此手机号已存在'
    return result
