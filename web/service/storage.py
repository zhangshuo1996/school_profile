from sqlalchemy import and_
from flask_login import current_user

from web.models import Department, Project, ProjectDeclaration, Activity, UploadFile


def get_breadcrumbs(level, **kwargs):
    """
    :param level: 1 不需要参数; 2需要department_id; 3 需要project; 4 如果有declaration_id 表示申报，否则是活动
    :param kwargs:
    :return:
    """
    # 第一级
    breadcrumbs = []
    idx = 1
    while idx <= level:
        # 第二级 获取到department
        if idx == 1:
            department_id = kwargs.get('department_id')
            department = Department.query.get_or_404(department_id)
            breadcrumbs.append({'name': department.name,
                                'link': '.show_projects',
                                'args': {'department_id': department.id}})
        # 第三级 获取到project
        elif idx == 2:
            project_id = kwargs.get('project_id')
            project = Project.query.get_or_404(project_id)
            breadcrumbs.append({'name': project.name,
                                'link': 'storage.show_contents_of_project',
                                'args': {'project_id': project.id}})
        # 显示政策申报
        elif idx == 3 and 'declaration_id' in kwargs:
            declaration_id = kwargs.get('declaration_id')
            declaration = ProjectDeclaration.query.get_or_404(declaration_id)
            breadcrumbs.append({'name': declaration.ep_name})
        # 显示活动
        elif idx == 3:
            third_name = kwargs['third'] if 'third' in kwargs else '无'
            breadcrumbs.append({'name': third_name})
        idx += 1
    return breadcrumbs


def get_project_directories(department: Department, endpoint):
    """
    根据department.projects 构造dict，以供前端展示
    :param department: Department的对象
    :param endpoint: 点击后的回调函数
    :return:
    """
    # 构造目录
    directories = []
    for project in department.projects:
        directories.append({
            'name': project.name,
            'link': endpoint,
            'args': {'project_id': project.id}
        })
    return directories


def get_contents_of_project(project: Project, can_read):
    """
    根据project构造project下所展示的内容
    :param project: Project的对象
    :param can_read: 0 1 2
    :return:
    """
    # 活动和政策
    args = {'project_id': project.id}
    # can_read = 1 直接显示单位对应的活动 =2 先显示举办过活动的中介和department，然后再展示活动文件
    activity_links = {1: '.show_activity_files', 2: '.show_activity_directories'}
    directories = [
        {'name': '政策', 'link': '.show_policies', 'args': args, 'category': 'green'},
        {'name': '活动', 'link': activity_links[can_read], 'args': args, 'category': 'remind'}
    ]
    # 政策申报
    if can_read == 1:
        declarations = ProjectDeclaration.query.filter(ProjectDeclaration.project_id == project.id,
                                                       ProjectDeclaration.agent_id == current_user.org_id)
    elif can_read == 2:
        declarations = ProjectDeclaration.query.filter_by(project_id=project.id)
    else:
        return directories
    declarations = declarations.order_by(ProjectDeclaration.gmt_create.desc()).all()
    # 政策申报
    status = ['进行中', '已完成', '已终止']
    for declaration in declarations:
        badge = status[declaration.status]
        directories.append({
            'name': declaration.ep_name,
            'link': '.show_project_declaration_files',
            'args': {'declaration_id': declaration.id},
            'badge': badge,
            'uploader': declaration.uploader if can_read == 1 else declaration.agent_name,
            'gmt_create': declaration.gmt_create,
        })
    return directories


def get_contents_of_activities(project_id):
    """
    获取在此project_id下的活动，并按照单位进行排序
    :param project_id:
    :return:
    """
    # 获取所有活动
    activities = Activity.query.filter_by(project_id=project_id).all()
    directories = []
    sponsor_id_set = set()
    for activity in activities:
        if activity.sponsor_id in sponsor_id_set:
            continue
        sponsor_id_set.add(activity.sponsor_id)
        directories.append({
            'name': activity.sponsor_name,
            'link': '.show_activity_files_of_sponsor',
            'args': {'org_id': activity.sponsor_id, 'project_id': project_id},
            'category': 'remind'})
    return directories


def get_policy_files(project_id):
    """
    获取跟项目有关的政策文件
    :param project_id: project_id下的政策
    :return: UploadFile数组
    """
    files = UploadFile.query.filter(UploadFile.category == 3, UploadFile.match_id == project_id).all()
    return files


def get_activity_files_by_project(org_id, project_id):
    """
    :param org_id: 活动的创办的所属机构
    :param project_id: 活动对应的项目id
    :return: UploadFile数组, sponsor_name
    """
    # 获取一组文件
    activities = Activity.query.filter(Activity.project_id == project_id, Activity.sponsor_id == org_id).all()
    if len(activities) > 0:
        sponsor_name = activities[0].sponsor_name
        array = [activity.id for activity in activities]
        files = UploadFile.query.filter(UploadFile.category == 2, UploadFile.match_id.in_(array)).all()
        return files, sponsor_name
    return [], None


def get_declaration_files(declaration_id):
    """
    获取某个政策申报下的所有文件
    :param declaration_id: 政策申报id
    :return: UploadFile数组
    """
    files = UploadFile.query.filter(UploadFile.category == 1, UploadFile.match_id == declaration_id).all()
    return files
