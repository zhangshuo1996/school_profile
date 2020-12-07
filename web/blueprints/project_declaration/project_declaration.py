"""
项目申报
by zhang
"""
import time
from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from web.extensions import db
from web.forms import UploadFileForm
from web.models import Project, ProjectDeclaration, Enterprise, Agent, UploadFile
from web.utils.url import redirect_back
from web.service.project_declaration import get_iur_declaration_num
from web.utils import date2timestamp
from web.service import project_declaration as project_declaration_service
from sqlalchemy import func

project_declaration_bp = Blueprint("project_declaration", __name__)


@project_declaration_bp.route("/")
@project_declaration_bp.route("/index")
def index():
    return redirect(url_for("project_declaration.manage_project"))


@project_declaration_bp.route("/manage_project")
@login_required
def manage_project():
    """
    显示该用户下有权限的项目类型
    by zhang
    :return:
    """
    department_id = request.args.get("department_id", type=int)
    # 获取该中介所管辖的项目, 以及该项目下的进行数量以及完成数量
    iur_contract_count = get_iur_declaration_num(category=2, agent_id=current_user.org_id)
    projects = Project.query.filter(Project.department_id == department_id)
    breadcrumbs = project_declaration_service.get_breadcrumbs(1, department_id=department_id)
    return render_template("project_declaration/manage_project.html", projects=projects,
                           iur_contract_count=iur_contract_count, breadcrumbs=breadcrumbs)


@project_declaration_bp.route("/show_project_list/<int:project_id>/<project_name>")
@login_required
def show_project_list(project_id, project_name):
    """
    展示某一申报类别下具体的申报项目列表
    """
    agent_id = current_user.org_id
    can_read = current_user.can_read(current_app.config["DECLARATION"], agent_id, project_id=project_id)
    if not can_read:
        # TODO:
        pass
    can_write = current_user.can_write(current_app.config["DECLARATION"], agent_id, project_id)

    if current_user.category_id == 1:  # 政府类型，部分中介，查看这个项目下所有的申报
        declaration_projects = ProjectDeclaration.query.filter(ProjectDeclaration.project_id == project_id,
                                                               ProjectDeclaration.status != 2).all()
    else:
        # 获取该中介下关于该项目类型的所有申报项目数据
        declaration_projects = ProjectDeclaration.query.filter(ProjectDeclaration.agent_id == agent_id,
                                                               ProjectDeclaration.project_id == project_id,
                                                               ProjectDeclaration.status != 2).all()
    # 获取该中介下的所有企业
    eps = Enterprise.query.filter(Enterprise.agent_id == agent_id).all()
    res_declaration_projects = [
        {
            "ep_name": declaration_project.ep_name,
            "project_name": project_name,
            "status": declaration_project.status,
            "company": current_user.org_name,
            "distribute_id": declaration_project.id,
            "start_time": declaration_project.get_start_time(),
            "gmt_deadline": declaration_project.get_gmt_deadline(),
            "ep_id": declaration_project.ep_id,
            "project_id": project_id,
            "progress": format(float(declaration_project.complete_num * 100) / float(declaration_project.task_num),
                               '.0f') if declaration_project.task_num != 0 else 0,
            "task_num": declaration_project.task_num,
            "complete_num": declaration_project.complete_num
        }
        for declaration_project in declaration_projects
    ]
    project = Project.query.get_or_404(project_id)
    breadcrumbs = project_declaration_service.get_breadcrumbs(2, department_id=project.department_id, project_id=project_id)
    return render_template("project_declaration/show_project_list.html", distribute_projects=res_declaration_projects,
                           all_ep_in_company=eps, project_name=project_name, project_id=project_id,
                           can_write=can_write, breadcrumbs=breadcrumbs)


@project_declaration_bp.route("/add_declaration_project", methods=["POST"])
def add_declaration_project():
    """
    新增项目申报
    # TODO: 有的新增项目申报时会同时增加两个项目， 问题未知
    :return:
    """
    form = request.form
    ep_id = form.get("ep_id", default=None, type=int)
    project_id = form.get("project_id", default=None, type=int)
    gmt_deadline = form.get("gmt_deadline")

    if ep_id is None or project_id is None or len(gmt_deadline) == 0:
        flash('请输入完整数据', 'danger')
        return redirect_back()
    # 添加新的项目申报
    project_declaration = ProjectDeclaration(
        agent_id=current_user.org_id, ep_id=ep_id, project_id=project_id,
        start_time=time.time(), gmt_deadline=date2timestamp(gmt_deadline),
        status=0, progress=20, task_num=0, complete_num=0, uploader=current_user.name
    )
    db.session.add(project_declaration)
    db.session.commit()

    # 获取该中介的此项目的任务模板，将任务模板中的任务加到任务表
    task_num = project_declaration_service.add_template_task_to_task(agent_id=current_user.org_id,
                                                                     project_id=project_id,
                                                                     ep_id=ep_id, distribute_id=project_declaration.id)
    # 更新此项目申报的任务数量
    project_declaration.task_num = task_num
    db.session.commit()

    flash('创建成功', 'success')
    return redirect_back()


@project_declaration_bp.route("/project_task_info/<int:distribute_id>")
@login_required
def project_task_info(distribute_id):
    """
    update by: xiaoniu, zhang
    展示某个具体项目下的甘特图，以及所有文件
    :param distribute_id:
    """
    declaration_project = ProjectDeclaration.query.get(distribute_id)
    # 判断该具体申报项目此用户是否有权限可读
    can_read = current_user.can_read(current_app.config["DECLARATION"], declaration_project.agent_id,
                                     project_id=declaration_project.project_id)
    if not can_read:
        # TODO:没有权限读
        pass
    detail = {
        "id": declaration_project.id,
        "project_id": declaration_project.project_id,
        "project_name": declaration_project.project_name,
        "ep_id": declaration_project.ep_id,
        "ep_name": declaration_project.ep_name,
        "deadline": declaration_project.get_gmt_deadline()
    }

    # 判断该用户是否有权限操作
    can_write = current_user.can_write(current_app.config["DECLARATION"], declaration_project.agent_id,
                                       declaration_project.project_id)
    # 获取该中介下所有的服务商
    all_sp = []
    if can_write:  # TODO：改成 该用户是否有操作权限来
        agent = Agent.query.get(current_user.org_id)
        all_sp = agent.service_providers
    project_id = declaration_project.project_id
    project = Project.query.get_or_404(project_id)
    breadcrumbs = project_declaration_service.get_breadcrumbs(3, department_id=project.department_id, project_id=project_id, declaration_id=distribute_id)
    return render_template("project_declaration/project_task_info.html", detail=detail, all_sp=all_sp,
                           can_write=can_write, breadcrumbs=breadcrumbs)


@project_declaration_bp.route("/project_file_info/<int:distribute_id>")
@login_required
def project_file_info(distribute_id):
    """
    update by: xiaoniu zhang
    查看材料和上传材料
    :param distribute_id:
    """
    declaration_project = ProjectDeclaration.query.get(distribute_id)
    form = UploadFileForm(category=1, match_id=distribute_id)
    detail = {
        "id": declaration_project.id,
        "project_id": declaration_project.project_id,
        "project_name": declaration_project.project_name,
        "ep_id": declaration_project.ep_id,
        "ep_name": declaration_project.ep_name
    }
    files = UploadFile.query.filter(UploadFile.match_id == distribute_id).all()
    can_write = current_user.can_write(category="DECLARATION", org_id=current_user.org_id, project_id=declaration_project.project_id)

    project_id = declaration_project.project_id
    project = Project.query.get_or_404(project_id)
    breadcrumbs = project_declaration_service.get_breadcrumbs(3, department_id=project.department_id,
                                                              project_id=project_id, declaration_id=distribute_id)
    return render_template("project_declaration/show_files.html", files=files, form=form,
                           detail=detail, can_write=can_write, can_read=True, breadcrumbs=breadcrumbs)


@project_declaration_bp.route("/update_status_to_delete", methods=['POST'])
@login_required
def update_status_to_delete():
    """
    更新中介下分配的项目为 删除 状态， 同时将该项目归档
    by zhang
    :return:
    """
    distribute_id = request.form.get('distribute_id', type=int, default=None)
    declaration_project = ProjectDeclaration.query.get(distribute_id)
    # 更新状态为删除状态，归档状态（删除自动归档）
    declaration_project.status = 2
    db.session.commit()
    flash("操作成功", "success")
    return redirect_back()


@project_declaration_bp.route("/update_status_to_complete", methods=['POST'])
@login_required
def update_status_to_complete():
    """
    更新中介下分配的项目为 完成 状态
    by zhang
    """
    distribute_id = request.form.get('distribute_id', type=int, default=None)
    declaration_project = ProjectDeclaration.query.get(distribute_id)
    task_num = declaration_project.task_num
    complete_num = declaration_project.complete_num
    if task_num == 0:
        flash("请先为该申报添加任务", "danger")
        return redirect_back()
    if complete_num < task_num:
        flash("请先完成所有任务", "danger")
        return redirect_back()

    # 更新状态为完成状态
    declaration_project.status = 1
    db.session.commit()
    flash("操作成功", "success")
    return redirect_back()
