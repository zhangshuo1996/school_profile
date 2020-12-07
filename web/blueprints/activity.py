import os
import time
from flask import redirect, current_app, abort
from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, jsonify, url_for, send_from_directory

from web.models import Activity, UploadFile, Project
from web.forms import ActivityForm, UploadFileForm
from web.utils.file import save_file
from web.decorators import permission_required
from web.service import activity as activity_service

activity_bp = Blueprint("activity", __name__)
ACTIVITY = 'ACTIVITY'


@activity_bp.route("/")
@activity_bp.route("/index/")
@login_required
def index():
    """日历展示活动"""
    breadcrumbs = activity_service.get_breadcrumbs(1)
    return render_template("activity/index.html", breadcrumbs=breadcrumbs)


@activity_bp.route('/show_base_info/<int:activity_id>')
@login_required
def show_base_info(activity_id):
    """展示活动的基本信息"""
    activity = Activity.query.get_or_404(activity_id)

    can_read = current_user.can_read(ACTIVITY, activity.sponsor_id, project_id=activity.project_id)
    can_write = current_user.can_write(ACTIVITY, activity.sponsor_id, activity.project_id)
    breadcrumbs = activity_service.get_breadcrumbs(2, activity_name=activity.title)
    return render_template("activity/show_base_info.html", activity=activity, can_read=can_read, can_write=can_write,
                           now=time.time(), breadcrumbs=breadcrumbs)


@activity_bp.route("/ajax/get_template/<string:temp_name>")
@login_required
def get_template(temp_name):
    """获取活动模板"""
    return render_template("activity/templ/%s" % temp_name)


@activity_bp.route('/new_activity', methods=['GET', 'POST'])
@login_required
@permission_required('ACTIVITY_WRITE')
def new_activity():
    """新建活动"""
    start_time = request.args.get('start_time')
    projects = current_user.get_projects()
    form = ActivityForm(projects, start_time=start_time)
    if form.validate_on_submit():
        activity = form.add_activity(current_user)
        return redirect(url_for('.show_base_info', activity_id=activity.id))
    title = '新建活动'
    breadcrumbs = activity_service.get_breadcrumbs(2, activity_name=title)
    return render_template('activity/new_or_edit_activity.html', form=form, title=title, breadcrumbs=breadcrumbs)


@activity_bp.route('/edit_activity/<int:activity_id>', methods=['GET', 'POST'])
@permission_required('ACTIVITY_WRITE')
def edit_activity(activity_id):
    """编辑活动"""
    activity = Activity.query.get_or_404(activity_id)
    projects = current_user.get_projects()
    # 只有get请求才会使用activity进行构造
    if request.method == 'GET':
        form = ActivityForm(projects, activity=activity)
    else:
        form = ActivityForm(projects)
    # 更新activity
    if form.validate_on_submit():
        activity = form.update_activity(activity)
        return redirect(url_for('.show_base_info', activity_id=activity.id))

    title = '编辑活动'
    breadcrumbs = activity_service.get_breadcrumbs(2, activity_name=title)
    return render_template('activity/new_or_edit_activity.html', form=form, title=title, breadcrumbs=breadcrumbs)


@activity_bp.route("/show_files/<int:activity_id>")
@login_required
def show_files(activity_id):
    """显示某一活动下的文件"""
    activity = Activity.query.get_or_404(activity_id)
    # 是否可以查看文件
    if not current_user.can_read(ACTIVITY, activity.sponsor_id, project_id=activity.project_id):
        abort(403)
    # 获取文件
    files = UploadFile.query.filter(UploadFile.match_id == activity.id).all()
    form = UploadFileForm(category=2, match_id=activity.id)
    # 只有自己才可以编辑文件
    can_write = current_user.can_write(ACTIVITY, activity.sponsor_id, activity.project_id)
    breadcrumbs = activity_service.get_breadcrumbs(2, activity_name=activity.title)
    return render_template("activity/show_files.html", files=files, form=form,
                           # container='container',
                           activity=activity, can_write=can_write, can_read=True, breadcrumbs=breadcrumbs)


@activity_bp.route("/ajax/get_data")
def get_data():
    """
    根据不同的用户类型返回日历显示所需要的数据
    :return: 返回json数据
    """
    from_time = request.args.get("from", type=int)
    to_time = request.args.get("to", type=int)
    from_time, to_time = from_time / 1000, to_time / 1000
    # 按照时间获取活动
    results = activity_service.get_activities_by_time(from_time, to_time)
    return jsonify({"success": 1, "result": results})


@activity_bp.route('/ajax/upload_image', methods=['POST'])
@login_required
def upload_image():
    """活动：上传图片"""
    file = request.files.get('upload')
    filename = save_file('images', file, is_random=True)
    return jsonify({'uploaded': True, 'url': url_for('.get_image', filename=filename)})


@activity_bp.route('/ajax/get_image/<filename>')
@login_required
def get_image(filename):
    """活动：下载图片"""
    full_path = os.path.join(current_app.config["FILE_UPLOAD_PATH"], 'images')
    return send_from_directory(full_path, filename)
