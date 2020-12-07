import io
import time
import pandas as pd
from urllib.parse import quote
from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, flash, current_app, send_from_directory, make_response, abort

from web.extensions import db
from web.models.project import Project
from web.utils.url import redirect_back
from web.decorators import permission_required
from web.models.project_result import ProjectResult
from web.service import statistic_input as statistic_input_service

# url_prefix='statistics/input'
statistic_input_bp = Blueprint("statistic_input", __name__)


@statistic_input_bp.route("/")
@statistic_input_bp.route("/index")
@login_required
@permission_required('ALL_STATISTIC_READ')
def index():
    """申报结果上传首页"""
    project_id = request.args.get("project_id", type=int, default=None)
    if project_id is None:
        abort(404)
    project = Project.query.get_or_404(project_id)

    project_name = project.name
    project_result = ProjectResult.query.filter_by(project_id=project_id)
    items = [{
        "id": result.id,
        "ep_name": result.ep_name,
        "project_id": result.project_id,
        "year": result.year,
        "remarks": result.remarks,
        "uploader": result.uploader
    } for result in project_result]
    return render_template("statistic_input.html", project_id=project_id, project_name=project_name, items=items)


@statistic_input_bp.route("/add_record", methods=["POST"])
@login_required
def add_record():
    """添加记录"""
    project_id = request.form.get("project_id")
    ep_name = request.form.get("ep_name")
    remarks = request.form.get("remarks")
    year = request.form.get("year")
    uploader = current_user.name
    gmt_create = time.time()
    if len(project_id) == 0 or len(ep_name) == 0 or len(year) == 0 or len(uploader) == 0:
        flash("请填写完整数据", "danger")
        return redirect_back()
    project_result = ProjectResult(ep_name=ep_name, remarks=remarks, year=year, uploader=uploader, gmt_create=gmt_create,
                                   project_id=project_id)
    db.session.add(project_result)
    db.session.commit()
    return redirect_back()


@statistic_input_bp.route("/delete_record", methods=['POST'])
@login_required
def delete_record():
    """下载记录"""
    record_id = request.form.get("record_id")
    project_result = ProjectResult.query.get(record_id)
    db.session.delete(project_result)
    db.session.commit()
    flash("删除成功", "success")
    return redirect_back()


@statistic_input_bp.route("/download_file", methods=['GET'])
@login_required
def download_file():
    """下载模板"""
    path = current_app.config["PROJECT_RESULT_TEMPLATE_PATH"]
    filename = 'template.xlsx'
    return send_from_directory(path, filename, attachment_filename="模板.xlsx")


@statistic_input_bp.route("/upload_namelist", methods=['POST'])
@login_required
def upload_namelist():
    """上传名单"""
    namelist_file = request.files.get("namelist_file")
    project_id = request.form.get("project_id")
    uploader = current_user.name
    gmt_create = time.time()
    statistic_input_service.upload_namelist(namelist_file, uploader, gmt_create, project_id)
    return redirect_back()


@statistic_input_bp.route("/download_namelist")
@login_required
def download_namelist():
    """下载名单"""
    project_id = request.args.get("project_id")
    project_name = request.args.get("project_name")
    project_result = ProjectResult.query.filter_by(project_id=project_id)
    items = [{
        "企业": result.ep_name,
        "备注": result.remarks,
        "年份": result.year,
        "上传者": result.uploader
    } for result in project_result]
    if len(items) == 0:
        flash("暂无数据", "info")
        return redirect_back()

    data = pd.DataFrame(items)
    out = io.BytesIO()
    writer = pd.ExcelWriter(out, engine='xlsxwriter')
    data.to_excel(excel_writer=writer, index=False, sheet_name='名单')
    writer.save()
    writer.close()

    response = make_response(out.getvalue())
    filename = project_name+".xlsx"
    response.headers['Content-Disposition'] = 'attachment;filename={0};filename*={0}'.format(quote(filename))
    response.headers["Content-type"] = "application/x-xls"

    return response
