from flask import Blueprint, redirect, flash, render_template, request, url_for
from flask_login import login_required
from werkzeug.security import generate_password_hash

from web.models import User, Role, Department, Agent
from web.extensions import db
from web.decorators import permission_required

# 地址前缀/admin/gov
gov_bp = Blueprint("gov", __name__)


@gov_bp.route("/")
@gov_bp.route("/member/", methods=['GET'])
@permission_required("GOV_ADMINISTRATOR")
@login_required
def gov_member():
    """政府成员列表"""
    departments = Department.query.filter_by(status=1).all()
    department_data = [{'id': 0, 'name': '全部部门'}]
    for department in departments:
        department_data.append(
            {
                'id': department.id,
                'name': department.name
            }
        )

    name = request.args.get('name', "")
    phone = request.args.get('phone', "")
    org = int(request.args.get('org', 0))
    page = int(request.args.get('page', 1))
    per_page = 10

    user_query = User.query.filter(User.category_id == 1).filter(User.is_active == 1)
    if name:
        user_query = user_query.filter(User.name.contains(name))
    if phone:
        user_query = user_query.filter(User.telephone.contains(phone))
    if org != 0:
        user_query = user_query.filter(User.org_id == org)

    paginate = user_query.order_by(User.id).paginate(page, per_page, error_out=False)
    members = paginate.items

    member_data = []
    for member in members:
        member_info = {}
        member_info['id'] = member.id
        member_info['telephone'] = member.telephone
        member_info['name'] = member.name
        member_info['avatar'] = member.avatar
        member_info['position'] = member.position

        department = Department.query.filter(Department.id == member.org_id).first()
        if department:
            member_info['department'] = department.name
        else:
            member_info['department'] = "暂无部门"
        member_data.append(member_info)
    return render_template('admin/gov/member_list.html', gov_data=member_data, department_data=department_data,
                           name=name, phone=phone, org=org, paginate=paginate,)


@gov_bp.route("/member/add/", methods=['POST', 'GET'])
@permission_required("GOV_ADMINISTRATOR")
@login_required
def gov_member_add():
    """新建政府人员"""
    if request.method == 'GET':
        departments = Department.query.filter_by(status=1).all()
        departments = [{'id': 0, 'name': "无"}] + departments
        roles = Role.query.filter_by(category=1).all()
        return render_template("admin/gov/new_member.html", departments=departments, roles=roles)
    elif request.method == 'POST':
        telephone = request.form.get('telephone')
        if User.query.filter_by(telephone=telephone).first():
            flash("该电话号码已被使用", "danger")
            return redirect(url_for('gov.gov_member_add'))
        else:
            name = request.form.get('name')
            password_hash = generate_password_hash(request.form.get('password'))
            org_id = int(request.form.get('department'))
            position = request.form.get('position')
            avatar = "default.jpg"
            roles = request.form.getlist('roles[]')
            user = User(
                name=name,
                telephone=telephone,
                category_id=1,
                password_hash=password_hash,
                org_id=org_id if org_id != 0 else None,
                position=position,
                avatar=avatar,
                is_active=1
            )
            try:
                db.session.add(user)
                db.session.commit()
                user = User.query.filter(User.telephone == telephone).first()
                for role in roles:
                    role = int(role)
                    role_obj = Role.query.filter(Role.id == role).first()
                    user.roles.append(role_obj)
                db.session.commit()
                flash("添加成员成功", 'success')
                return redirect(url_for('gov.gov_member'))
            except:
                flash("添加成员失败", 'danger')
                return redirect(url_for('gov.gov_member_add'))


@gov_bp.route("/member/modify/<int:member_id>/", methods=['POST', 'GET'])
@permission_required("GOV_ADMINISTRATOR")
@login_required
def gov_member_modify(member_id):
    """修改政府人员信息"""
    if request.method == 'GET':
        departments = Department.query.filter_by(status=1).all()
        departments = [{'id': 0, 'name': "无"}] + departments
        role_list = Role.query.filter_by(category=1).all()

        user = User.query.filter(User.id == member_id).first()
        user_info = {}
        user_info['id'] = user.id
        user_info['name'] = user.name
        user_info['telephone'] = user.telephone
        user_info['org_id'] = user.org_id
        user_info['position'] = user.position
        user_info['roles'] = [item.id for item in user.roles]

        return render_template('admin/gov/edit_member.html', user=user_info, departments=departments,
                               role_list=role_list)
    elif request.method == 'POST':
        user = User.query.filter_by(id=member_id).first()
        new_telephone = request.form.get('telephone')

        if new_telephone != user.telephone and User.query.filter_by(telephone=new_telephone).first():
            flash("该电话号码已被使用", 'danger')
            return redirect(url_for('gov.gov_member_modify', member_id=member_id))
        else:
            user.name = request.form.get('name')
            user.telephone = request.form.get('telephone')
            depart = int(request.form.get('department'))
            user.org_id = depart if depart != 0 else None
            user.position = request.form.get('position')
            roles = request.form.getlist('roles[]')

            user.roles = []
            print(roles)
            for role in roles:
                role = int(role)
                role_obj = Role.query.filter(Role.id == role).first()
                user.roles.append(role_obj)
            try:
                db.session.commit()
                flash("修改人员信息成功", 'success')
                return redirect(url_for('gov.gov_member'))
            except:
                flash("修改人员信息失败", 'danger')
                return redirect(url_for('gov.gov_member_modify', member_id=member_id))


@gov_bp.route("/member/delete/<int:member_id>", methods=['POST'])
@permission_required("GOV_ADMINISTRATOR")
@login_required
def gov_member_delete(member_id):
    """删除政府人员"""
    user = User.query.filter_by(id=member_id).first()
    user.is_active = 0
    try:
        db.session.commit()
        flash("删除成员成功", 'success')
        return redirect(url_for('gov.gov_member'))
    except:
        flash("删除成员失败", "danger")
        return redirect(url_for('gov.gov_member'))


@gov_bp.route("/agent/", methods=['GET'])
@permission_required("GOV_ADMINISTRATOR")
@login_required
def gov_agent():
    name = request.args.get('name', "")
    company = request.args.get('company', "")
    town = request.args.get('town', "")
    contact_name = request.args.get('contact_name', "")
    page = int(request.args.get('page', 1))
    per_page = 10

    agent_obj = Agent.query
    if name:
        agent_obj = agent_obj.filter(Agent.name.contains(name))
    if company:
        agent_obj = agent_obj.filter(Agent.company.contains(company))
    if town:
        agent_obj = agent_obj.filter(Agent.town.contains(town))
    if contact_name:
        agent_obj = agent_obj.filter(Agent.contact_name.contains(contact_name))
    paginate = agent_obj.order_by(Agent.id).paginate(page, per_page, error_out=False)

    agents = paginate.items
    return render_template('admin/gov/organization_list.html', paginate=paginate, gov_agent_data=agents, name=name,
                           company=company, town=town, contact_name=contact_name)


@gov_bp.route("/agent/add", methods=['POST', 'GET'])
@permission_required("GOV_ADMINISTRATOR")
@login_required
def gov_agent_add():
    """新建政府中介"""
    if request.method == 'GET':
        agent_pattern = ['', '官办官营', '官办民营', '民办民营', '示范活跃']
        agent_level = ['', '国家级', '省级', '县级']
        category_list = [
            {'id': 0, 'name': "数据平台"},
            {'id': 1, 'name': "孵化器"},
            {'id': 2, 'name': "众创空间"},
        ]
        return render_template('admin/gov/new_organization.html', patterns=agent_pattern, levels=agent_level,
                               category_list=category_list)
    elif request.method == 'POST':
        name = request.form.get('name')
        full_name = request.form.get('full_name')
        company = request.form.get('company')
        pattern = request.form.get('pattern')
        town = request.form.get('town')
        try:
            gmt_create = int(request.form.get('gmt_create'))
        except:
            gmt_create = None
        try:
            area = int(request.form.get('area'))
        except:
            area = None
        category = request.form.get('category', '')
        level = request.form.get('level', '')
        address = request.form.get('address', '')
        contact = request.form.get('contact')
        phone = request.form.get('telephone')
        is_active = 1
        if request.form.get('avatar'):
            avatar = request.form.get('avatar')
        else:
            avatar = "default.png"
        agent = Agent(
            name=name,
            full_name=full_name,
            company=company,
            pattern=pattern,
            town=town,
            gmt_create=gmt_create,
            category=category,
            level=level,
            area=area,
            address=address,
            is_active=is_active,
            avatar=avatar,
            contact_name=contact,
            contact_telephone=phone
        )
        try:
            db.session.add(agent)
            db.session.commit()
            agent_id = Agent.query.filter_by(name=name).first().id
            contact = User(
                name=contact,
                telephone=phone,
                category_id=2,
                org_id=agent_id,
                position="联系人",
                is_active=1,
                avatar="default.jpg"
            )
            db.session.add(contact)
            db.session.commit()
            new_contact = User.query.filter_by(telephone=phone).first()
            new_contact.roles.append(Role.query.filter_by(name="中介-管理员").first())
            db.session.commit()
            flash("新建中介成功", "success")
            return redirect(url_for("gov.gov_agent"))
        except:
            flash("新建中介失败", "danger")
            return redirect(url_for("gov.gov_agent_add"))


@gov_bp.route("/agent/modify/<int:agent_id>", methods=['POST', 'GET'])
@permission_required("GOV_ADMINISTRATOR")
@login_required
def gov_agent_modify(agent_id):
    """修改中介信息"""
    if request.method == 'GET':
        agent_pattern = ['官办官营', '官办民营', '民办民营', '示范活跃']
        agent_level = ['国家级', '省级', '县级']
        category_list = [
            {'id': 0, 'name': "数据平台"},
            {'id': 1, 'name': "孵化器"},
            {'id': 2, 'name': "众创空间"},
        ]
        agent_info = Agent.query.filter_by(id=agent_id).first()
        return render_template('admin/gov/edit_organization.html',
                               agent=agent_info,
                               patterns=agent_pattern,
                               categories=category_list,
                               levels=agent_level)

    elif request.method == 'POST':
        agent = Agent.query.filter_by(id=agent_id).first()

        agent.name = request.form.get('name')
        agent.full_name = request.form.get('full_name', '')
        agent.company = request.form.get('company', '')
        agent.pattern = request.form.get('pattern', '')
        agent.town = request.form.get('town', '')
        try:
            agent.gmt_create = int(request.form.get('gmt_create'))
        except:
            agent.gmt_create = None
        try:
            agent.area = int(request.form.get('area'))
        except:
            agent.area = None
        agent.category = int(request.form.get('category'))
        agent.level = request.form.get('level', '')
        agent.address = request.form.get('address', '')
        # 联系人信息
        contact_name = request.form.get('contact')
        contact_telephone = request.form.get('telephone')
        if contact_telephone:
            user = User.query.filter_by(telephone=contact_telephone).first()
        else:
            db.session.commit()
            flash("修改中介信息成功", "success")
            return redirect(url_for('gov.gov_agent'))
        # 新联系人已存在，则分配中介管理员权限并作为联系人
        if user:
            if user.org_id == agent.id:
                agent.contact_name = contact_name
                agent.contact_telephone = contact_telephone
                if not user.can('AGENT_ADMINISTRATOR'):
                    user.roles.append(Role.query.filter_by(name="中介-管理员").first())
                try:
                    db.session.commit()
                    flash("修改中介信息成功", "success")
                    return redirect(url_for('gov.gov_agent'))
                except:
                    flash("修改中介信息失败", "danger")
                    return redirect(url_for('gov.gov_agent_modify', agent_id=agent_id))
            else:
                flash("该用户属于其他中介，修改失败", "danger")
                return redirect(url_for('gov.gov_agent_modify', agent_id=agent_id))
        # 新联系人账号不存在，新建用户，给予管理员权限并作为联系人
        else:
            new_contact = User(
                name=contact_name,
                telephone=contact_telephone,
                category_id=2,
                org_id=agent_id,
                position="联系人",
                is_active=1,
                avatar="default.jpg"
            )
            db.session.add(new_contact)
            try:
                db.session.commit()
                new_contact.roles.append(Role.query.filter_by(name="中介-管理员").first())
                agent.contact_name = contact_name
                agent.contact_telephone = contact_telephone
                db.session.commit()
                flash("修改中介信息成功", "success")
                return redirect(url_for('gov.gov_agent'))
            except:
                flash("修改中介信息失败", "danger")
                return redirect(url_for('gov.gov_agent_modify', agent_id=agent_id))


@gov_bp.route("/agent/delete/<int:agent_id>", methods=['POST'])
@permission_required("GOV_ADMINISTRATOR")
@login_required
def gov_agent_delete(agent_id):
    """删除中介"""
    agent = Agent.query.filter_by(id=agent_id).first()
    agent.is_active = 0
    users = User.query.filter_by(org_id=agent_id).all()
    for user in users:
        user.is_active = 0
    try:
        db.session.commit()
        flash("删除中介成功", "success")
    except:
        flash("删除中介失败", "danger")
    return redirect(url_for('gov.gov_agent'))


@gov_bp.route("/department/")
@permission_required("GOV_ADMINISTRATOR")
@login_required
def gov_department():
    """政府部门管理"""
    departments = Department.query.filter_by(status=1).all()
    department_info = []
    for item in departments:
        depart = item.__dict__
        department_info.append(depart)
    return render_template('admin/gov/department_list.html', department_data=department_info)


@gov_bp.route("/gov/department/modify/<int:department_id>", methods=['POST'])
@permission_required("GOV_ADMINISTRATOR")
@login_required
def gov_department_modify(department_id):
    if request.method == 'POST':
        department = Department.query.filter_by(id=department_id).first()
        department.name = request.form.get('name')
        try:
            db.session.commit()
            flash("修改成功", "success")
        except:
            flash("修改失败", "danger")
        return redirect(url_for('gov.gov_department'))
