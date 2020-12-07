import os

from flask import Blueprint, render_template, request, redirect, current_app, send_from_directory, url_for, flash, jsonify
from flask_login import login_required, current_user
from web.service import user as user_service
from werkzeug.security import check_password_hash, generate_password_hash
from web.models import User, Agent, Department
from web.settings import AGENT_PATTERN, AGENT_LEVEL
from web.utils.url import redirect_back, is_valid_telephone
from web.extensions import db

user_bp = Blueprint("user", __name__)


@user_bp.route("/personal")
@login_required
def personal():
    """
    用户账号设置
    by：df
    """
    category = current_user.category_id
    if category == 1:
        return redirect(url_for("user.gov_personal"))
    else:
        return redirect(url_for("user.agent_personal"))


@user_bp.route("/gov_personal")
@login_required
def gov_personal():
    """
    政府人员账号设置
    by:df
    """
    department = Department.query.get(current_user.org_id)
    return render_template("user/gov_personal.html", user=current_user, department=department)


@user_bp.route("/agent_personal")
@login_required
def agent_personal():
    """
    中介人员账号设置
    by:df
    """
    company = Agent.query.get(current_user.org_id)
    return render_template("user/agent_personal.html", user=current_user, company=company)


@user_bp.route("/agent_base")
@login_required
def agent_base():
    """
    展示中介信息
    """
    agent_info = Agent.query.get(current_user.org_id)
    return render_template("user/agent_base_info.html", agent_info=agent_info, patterns=AGENT_PATTERN,
                           levels=AGENT_LEVEL)


@user_bp.route("/modify_password", methods=['POST'])
@login_required
def update_password():
    """
    修改政府人员和中介的登录密码
    by:df
    """
    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")
    if check_password_hash(current_user.password_hash, old_password) is False:
        return jsonify({"status": False, "errorMsg": "旧密码错误"})
    else:
        current_user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({"status": True})


@user_bp.route("/update_avatar", methods=['POST'])
@login_required
def update_avatar():
    """
    修改用户头像
    """
    avatar_file = request.files.get("avatar")
    if avatar_file is None:
        return {"error": True}
    upload_path = current_app.config["AVATAR_UPLOAD_PATH"]
    avatar_name = user_service.update_agent_avatar(upload_path, avatar_file)
    if avatar_name is None:
        return {"error": True}
    current_user.avatar = avatar_name
    db.session.commit()
    return {"error": False}


@user_bp.route("/update_agent_avatar", methods=['POST'])
@login_required
def update_agent_avatar():
    """
    修改中介机构头像
    """
    avatar_file = request.files.get("avatar")
    if avatar_file is None:
        return {"error": True}
    upload_path = current_app.config["AVATAR_UPLOAD_PATH"]
    avatar_name = user_service.update_agent_avatar(upload_path, avatar_file)
    if avatar_name is None:
        return {"error": True}
    agent = Agent.query.get(current_user.org_id)
    agent.avatar = avatar_name
    db.session.commit()
    return {"error": False}


@user_bp.route("/avatar/<filename>")
@login_required
def avatar(filename):
    """
    寻找头像
    """
    upload_path = current_app.config["AVATAR_UPLOAD_PATH"]
    return send_from_directory(upload_path, filename)


@user_bp.route("/modify_name", methods=['POST'])
@login_required
def modify_name():
    """修改姓名"""
    name = request.form.get("name")
    if name is None or len(name) == 0:
        return {"status": False, "errorMsg": "请输入姓名"}
    current_user.name = name
    db.session.commit()
    return {"status": True}


@user_bp.route("/modify_telephone", methods=['POST'])
@login_required
def modify_telephone():
    """修改电话号码"""
    telephone = request.form.get("telephone")
    if telephone is None or is_valid_telephone(telephone) is False:
        return {"status": True, "errorMsg": "请输入正确的电话格式！"}
    current_user.telephone = telephone
    db.session.commit()
    return {"status": True}


@user_bp.route("/modify_agent", methods=['POST'])
@login_required
def modify_agent():
    agent_id = request.form.get("agent_id", default=None, type=int)
    agent_full_name = request.form.get("agent_full_name")
    agent_company = request.form.get("agent_company")
    agent_pattern = request.form.get("agent_pattern")
    agent_level = request.form.get("agent_level")
    agent_address = request.form.get("agent_address")
    if agent_full_name.strip() == "" or agent_company.strip() == "" or agent_address.strip() == "":
        flash("请填写完整", "danger")
        return redirect_back()
    agent = Agent.query.get(agent_id)
    agent.full_name = agent_full_name
    agent.company = agent_company
    agent.pattern = agent_pattern
    agent.level = agent_level
    agent.address = agent_address
    db.session.commit()
    flash("修改成功", "success")
    return redirect_back()
