from datetime import datetime
from sqlalchemy.sql import func
from flask_login import login_required
from flask import render_template, Blueprint, request, abort, jsonify

from web.extensions import db
from web.decorators import permission_required
from web.utils import yearStart2timestamp
from web.service import statistics as statistics_service
from web.models import ProjectResult, Activity, ProjectDeclaration, Project, Department

statistics_bp = Blueprint("statistics", __name__)


@statistics_bp.route("/")
@login_required
@permission_required('ALL_STATISTIC_READ')
def index():
    """根据项目id，获取 项目评审结果，活动组织数量和政策申报数量"""
    department_id = request.args.get("department_id", default=2, type=int)
    project_id = request.args.get("pid", default=None, type=int)

    # TODO 部门内的项目排序
    projects = Project.query.filter(Project.department_id == department_id).order_by(Project.id.desc()).all()
    if len(projects) == 0:
        abort(404)

    if project_id is None:
        project_id = projects[0].id
    else:
        # project_id 需要和department_id对应
        project = Project.query.get_or_404(project_id)
        if project.department_id != department_id:
            abort(404)

    this_year = datetime.now().year
    total_result = db.session.query(
        func.count(ProjectResult.id)).filter(ProjectResult.project_id == project_id,
                                             ProjectResult.year == this_year).scalar()

    gmt_start = yearStart2timestamp()
    total_activity = db.session.query(func.count(Activity.id)).filter(Activity.project_id == project_id,
                                                                      Activity.gmt_start >= gmt_start).scalar()
    total_project = db.session.query(func.count(ProjectDeclaration.id)).filter(
        ProjectDeclaration.project_id == project_id, ProjectDeclaration.gmt_create >= gmt_start).scalar()

    department = Department.query.get(department_id)
    project = Project.query.get(project_id)
    statistics = [
        {"title": "公示结果", "value": total_result, "icon": "fe fe-award"},
        {"title": "活动组织", "value": "%s场" % total_activity, "icon": "fe fe-activity"},
        {"title": "政策申报", "value": "%s项" % total_project, "icon": "fe fe-compass"}
    ]
    return render_template("statistics/index.html", department=department, project_id=project_id,
                           breadcrumbs=[{"name": project.name}], statistics=statistics, projects=projects)


@statistics_bp.route("/get_agent_comparison")
@login_required
def get_agent_comparison():
    """
    获取本年度中介对比
    category declaration为申报，activity为活动
    project_id 项目id
    """
    project_id = request.args.get('project_id', default=None)
    category = request.args.get('category', default='declaration')
    project = Project.query.get_or_404(project_id)

    agent_list, series = statistics_service.get_agent_rank_new(project, category)
    return jsonify({
        'agent_list': agent_list,
        'series': series
    })


@statistics_bp.route("/get_month_activity_declaration")
@login_required
def get_month_activity_declaration():
    """
    获取今年来某一项目的 每月的活动和申报的数量
    :return:
    """
    project_id = request.args.get("project_id")
    data = statistics_service.get_month_activity_declaration(project_id)
    return {"success": True, 'data': data}


@statistics_bp.route("/get_recent_activities")
def get_recent_activities():
    """
    根据project_id 获取近期的活动
    """
    project_id = request.args.get("project_id")
    data = statistics_service.get_recent_activities(project_id)
    return {"data": data}


@statistics_bp.route("/get_complete_num")
def get_complete_num():
    """
    获取某一项目下各中介的完成数量
    :return:
    """
    project_id = request.args.get("project_id")
    result = statistics_service.get_complete_num(project_id)
    return result
