from sqlalchemy import and_
from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, abort

from web.decorators import permission_required
from web.models import Project, ProjectDeclaration, UploadFile, Activity, Department
from web.service import storage as storage_service
from web.forms import UploadFileForm

storage_bp = Blueprint("storage", __name__)


@storage_bp.route('/')
@login_required
def index():
    # TODO:一般不会跳到这里
    departments = current_user.get_departments()
    if len(departments) == 0:
        abort(404)
    return redirect(url_for('.show_projects', department_id=departments[0].id))


@storage_bp.route('/show_projects/<int:department_id>')
@login_required
def show_projects(department_id):
    """把用户的projects使用目录展示:第1级"""
    # 获取当前用户的projects
    department = Department.query.get_or_404(department_id)
    # 是否存在阅读文件的权限
    can_read = current_user.can_read('FILE_STORAGE', current_user.org_id, department_id=department_id)
    if can_read == 0:
        abort(403)
    # 面包屑
    breadcrumbs = storage_service.get_breadcrumbs(1, department_id=department_id)
    print(breadcrumbs)
    # 构造目录
    directories = storage_service.get_project_directories(department, '.show_contents_of_project')
    return render_template('storage/show_directory.html', breadcrumbs=breadcrumbs, directories=directories)


@storage_bp.route('/show_contents_of_project/<int:project_id>')
@login_required
def show_contents_of_project(project_id):
    """展示特定项目下的活动和相关的企业的政策申报: 第2级"""
    project = Project.query.get_or_404(project_id)
    # 是否存在阅读文件的权限
    can_read = current_user.can_read('FILE_STORAGE', current_user.org_id, department_id=project.department_id)
    if can_read == 0:
        abort(403)
    breadcrumbs = storage_service.get_breadcrumbs(2, department_id=project.department_id, project_id=project_id)
    # 构造目录
    directories = storage_service.get_contents_of_project(project, can_read)
    return render_template('storage/show_directory2.html', breadcrumbs=breadcrumbs, directories=directories)


@storage_bp.route('/show_activity_directories/<int:project_id>')
@login_required
@permission_required('ALL_FILE_STORAGE_READ')
def show_activity_directories(project_id):
    """展示 部门 和 中介在此project下的目录 第三级"""
    project = Project.query.get_or_404(project_id)
    # 面包屑
    breadcrumbs = storage_service.get_breadcrumbs(3, department_id=project.department_id,
                                                  project_id=project_id, third='活动')
    # 目录
    directories = storage_service.get_contents_of_activities(project_id)
    return render_template('storage/show_directory2.html', breadcrumbs=breadcrumbs, directories=directories)


@storage_bp.route('/show_activity_files_of_sponsor/<int:org_id>/<int:project_id>')
@login_required
@permission_required('ALL_FILE_STORAGE_READ')
def show_activity_files_of_sponsor(org_id, project_id):
    """展示活动的所有文件 第4级"""
    project = Project.query.get_or_404(project_id)
    # 面包屑
    breadcrumbs = storage_service.get_breadcrumbs(3, department_id=project.department_id,
                                                  project_id=project_id, third='活动')
    breadcrumbs[-1].update({'link': '.show_activity_directories', 'args': {'project_id': project_id}})
    files, sponsor_name = storage_service.get_activity_files_by_project(org_id, project_id)
    breadcrumbs.append({'name': sponsor_name})
    title = '{}-活动文件'.format(project.name)
    return render_template('storage/show_files.html', files=files, breadcrumbs=breadcrumbs, title=title)


@storage_bp.route('/show_activity_files/<int:project_id>')
@login_required
@permission_required('FILE_STORAGE_READ')
def show_activity_files(project_id):
    """只查看自己的活动的文件 第3级"""
    project = Project.query.get_or_404(project_id)
    breadcrumbs = storage_service.get_breadcrumbs(3, department_id=project.department_id,
                                                  project_id=project_id, third='活动')
    files, sponsor_name = storage_service.get_activity_files_by_project(current_user.org_id, project_id)
    title = '{}-活动文件'.format(project.name)
    return render_template('storage/show_files.html', files=files, breadcrumbs=breadcrumbs, title=title)


@storage_bp.route('/show_project_declaration_files/<int:declaration_id>')
@login_required
def show_project_declaration_files(declaration_id):
    """展示某企业在某项目下的文件: 第3级"""
    declaration = ProjectDeclaration.query.get_or_404(declaration_id)
    project = Project.query.get(declaration.project_id)
    # 是否存在阅读文件的权限
    can_read = current_user.can_read('FILE_STORAGE', current_user.org_id, department_id=project.department_id)
    if can_read == 0:
        abort(403)
    # 面包屑
    breadcrumbs = storage_service.get_breadcrumbs(3, department_id=project.department_id, project_id=project.id,
                                                  declaration_id=declaration_id)
    # 获取这个企业，在这个project下的所有文件
    files = storage_service.get_declaration_files(declaration_id)
    title = '{}-{}'.format(project.name, declaration.ep_name)

    return render_template('storage/show_files.html', files=files, breadcrumbs=breadcrumbs, title=title)


@storage_bp.route('/show_policies/<int:project_id>')
@login_required
@permission_required('ALL_POLICY_READ')
def show_policies(project_id):
    """展示所有政策 第3级"""
    project = Project.query.get_or_404(project_id)
    # 面包屑
    breadcrumbs = storage_service.get_breadcrumbs(3, department_id=project.department_id,
                                                  project_id=project_id, third='政策文件')
    # 政策文件
    files = storage_service.get_policy_files(project.id)
    title = '{}-政策文件'.format(project.name)
    # 是否具有写权限
    can_write = current_user.can_write('POLICY', current_user.org_id, project_id=project_id)
    form = UploadFileForm(category=3, match_id=project.id)
    return render_template('storage/show_files.html', files=files, breadcrumbs=breadcrumbs, title=title,
                           can_write=can_write, form=form)
