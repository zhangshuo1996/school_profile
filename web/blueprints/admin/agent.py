from flask import Blueprint, redirect, flash, render_template, request, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from web.models import User, Role, Agent
from web.extensions import db
from web.decorators import permission_required

# 地址前缀/admin/agent
agent_bp = Blueprint("agent", __name__)


# 中介成员管理
@agent_bp.route("/member/")
@permission_required("AGENT_ADMINISTRATOR")
@login_required
def agent_member():
    agent_member_data = []
    agent_id = current_user.org_id
    agent_name = Agent.query.filter_by(id=agent_id).first().name
    agent_members = User.query.filter_by(org_id=agent_id).filter_by(is_active=1).all()

    for agent_member in agent_members:
        agent_member_data.append(agent_member.__dict__)
    return render_template("admin/agent/agent_member_list.html", agent_name=agent_name, agent_data=agent_member_data)


@agent_bp.route("/member/add", methods=['POST', 'GET'])
@login_required
@permission_required("AGENT_ADMINISTRATOR")
def agent_member_add():
    if request.method == 'GET':
        roles = Role.query.filter_by(category=2).all()
        return render_template("admin/agent/new_agent_member.html", roles=roles)
    elif request.method == 'POST':
        telephone = request.form.get("telephone")
        user = User.query.filter_by(telephone=telephone).first()
        if user:
            flash("该电话号码已被注册，无法新建账号")
            return redirect(url_for('agent.agent_member_add'))
        else:
            roles = request.form.getlist('roles[]')
            agent_member = User(telephone=telephone,
                                org_id=current_user.org_id,
                                category_id=2,
                                name=request.form.get("name"),
                                password_hash=generate_password_hash(request.form.get('password')),
                                position=request.form.get("position"),
                                avatar='default.png',
                                is_active=1
                                )
            try:
                db.session.add(agent_member)
                db.session.commit()
                user = User.query.filter_by(telephone= telephone).first()
                for role in roles:
                    role = int(role)
                    role_obj = Role.query.filter(Role.id == role).first()
                    user.roles.append(role_obj)
                db.session.commit()
                flash("添加中介人员信息成功", "success")
                return redirect(url_for('agent.agent_member'))
            except:
                flash("添加中介人员信息失败", "danger")
                return redirect(url_for('agent.agent_member_add'))


@agent_bp.route("/member/modify/<int:member_id>", methods=['POST', 'GET'])
@permission_required("AGENT_ADMINISTRATOR")
@login_required
def agent_member_modify(member_id):
    if request.method == 'GET':
        role_list = Role.query.filter_by(category=2).all()
        user = User.query.filter(User.id == member_id).first()
        user_info = {}
        user_info['id'] = user.id
        user_info['name'] = user.name
        user_info['telephone'] = user.telephone
        user_info['position'] = user.position
        user_info['roles'] = [item.id for item in user.roles]
        agents = Agent.query.filter_by(is_active=1).all()
        return render_template('admin/agent/edit_agent_member.html', user=user_info, role_list=role_list, agents=agents)
    elif request.method == 'POST':
        user = User.query.filter_by(id=member_id).first()
        user.name = request.form.get('name')
        user.telephone = request.form.get('telephone')
        user.position = request.form.get('position')
        roles = request.form.getlist('roles[]')
        user.roles = []
        for role in roles:
            role = int(role)
            role_obj = Role.query.filter(Role.id == role).first()
            user.roles.append(role_obj)
        try:
            db.session.commit()
            flash("修改人员信息成功", "success")
            return redirect(url_for('agent.agent_member'))
        except:
            flash("修改人员信息失败", "danger")
            return url_for('agent.agent_member_modify', member_id=user.id)


@agent_bp.route("/member/delete/<int:member_id>", methods=['POST', 'GET'])
@permission_required("AGENT_ADMINISTRATOR")
@login_required
def agent_member_delete(member_id):
    user = User.query.filter_by(id=member_id).first()
    try:
        user.is_active = 0
        db.session.commit()
        flash("删除中介成员成功", "success")
        return redirect(url_for('agent.agent_member'))
    except:
        flash("删除中介成员失败", "danger")
        return redirect(url_for('agent.agent_member'))