"""
项目申报部分的业务逻辑处理
"""
from web.models.project_declaration_task import ProjectDeclarationTask
from sqlalchemy import or_, and_
from web.models.project_declaration import ProjectDeclaration
from web.models.project_task_template import ProjectTaskTemplate
from web.models.upload_file import UploadFile
from web.models.department import Department
from web.models.project import Project
from web.extensions import db
import time
from web.utils import date2timestamp
from web.utils.file import save_file


def cal_project_declaration_progress(tasks):
    """
    计算某一个具体申报项目的进度：所有子任务的进度平均值
    :param tasks:
    :return:
    """
    sum_progress = 0
    for task in tasks:
        sum_progress += task.progress
    return sum_progress / len(tasks)


def update_or_add_task_template(agent_id, project_id, task_name, executor):
    """
    更新或增加任务模板
    :return:
    """
    # 判断该任务是否来自于模板表
    cnt = ProjectTaskTemplate.query.filter(ProjectTaskTemplate.agent_id == agent_id,
                                           ProjectTaskTemplate.project_id == project_id,
                                           ProjectTaskTemplate.task_name == task_name).count()

    if cnt > 0:  # 如果模板表中存在该任务， 则更新模板表
        template = ProjectTaskTemplate.query.filter_by(agent_id == agent_id, project_id == project_id)
        template.task_name = task_name
        template.executor = executor
        # db.session.commit()
    else:  # 如果 模板表中不存在该任务， 则向模板表中增加数据
        template = ProjectTaskTemplate(agent_id=agent_id, project_id=project_id,
                                       task_name=task_name, default_executor=executor)
        db.session.add(template)
    db.session.commit()
    return True


def get_iur_declaration_num(category=1, agent_id=0):
    """

    :param category: 为1：获取所有中介的产学研申报项目， 为2：根据agent_id获取某个中介的产学研项目
    :param agent_id:
    :return:
    """
    if category == 1:
        declaration_projects = ProjectDeclaration.query.filter(
            ProjectDeclaration.project_id == 82
        )
    else:
        declaration_projects = ProjectDeclaration.query.filter(
            ProjectDeclaration.project_id == 82, ProjectDeclaration.agent_id == agent_id
        )
    return declaration_projects.count()


def add_template_task_to_task(agent_id, project_id, ep_id, distribute_id):
    """
    新增项目申报时，将该项目对应的模板任务增加到任务表
    :return: 新增模板任务的数量
    """
    # 获取项目id == project_id和（中介id == agent_id 或中介id == null）的模板
    templates = ProjectTaskTemplate.query.filter(and_(ProjectTaskTemplate.project_id == project_id,
                                                      or_(ProjectTaskTemplate.agent_id.is_(None),
                                                          ProjectTaskTemplate.agent_id == agent_id)))

    for template in templates:
        task_name = template.task_name
        default_executor = template.default_executor

        task_template = ProjectDeclarationTask(
            agent_id=agent_id, ep_id=ep_id, distribute_id=distribute_id, task_name=task_name, executor=default_executor,
            gmt_create=time.time(),
            gmt_deadline=time.time(), status=0
        )

        db.session.add(task_template)
        db.session.commit()

    return templates.count()


def add_task_template(agent_id, project_id, add_task_name, add_task_executor):
    """
    增加任务模板
    :return:
    """
    template = ProjectTaskTemplate(agent_id=agent_id, project_id=project_id, task_name=add_task_name,
                                   default_executor=add_task_executor)
    db.session.add(template)
    db.session.commit()
    return {"error": False}


def add_declaration_task(agent_id, ep_id, add_task_name, distribute_project_id, add_task_executor, add_task_start,
                         add_task_end, add_task_file, uploader):
    """
    新增某一具体项目申报下的任务, 以及任务对应的文件
    1. 将任务数据增加至任务表
    2. 存储任务对应的文件
    3. 文件记录入库
    4. 更新任务表中的file_id
    by zhang
    :return:
    """
    # 1. 将该任务增加至任务表
    task = ProjectDeclarationTask(agent_id=agent_id, ep_id=ep_id, task_name=add_task_name,
                                  distribute_id=distribute_project_id,
                                  executor=add_task_executor, gmt_create=date2timestamp(add_task_start),
                                  gmt_deadline=date2timestamp(add_task_end), progress=20, status=0)
    db.session.add(task)

    if add_task_file is not None:  # 当上传的文件不为None时， 存储并记录
        # 2. 存储文件至文件系统
        filename_hash = store_file(add_task_file)

        # 3. 文件记录入库
        path = "files"
        file_id = store_file_record(distribute_project_id, uploader, add_task_file.filename, filename_hash, path)

        # 4. 更新任务中的file_id
        task.file_id = file_id

    db.session.commit()
    return {"success": True}


def store_file(add_task_file, path="files"):
    """
    存储文件至文件系统
    :return:
    """
    filename_hash = save_file(path, add_task_file)  # 保存文件至文件系统，并获取文件名的哈希值
    return filename_hash


def store_file_record(distribute_project_id, uploader, filename, filename_hash, path="files"):
    """
    存储文件记录至数据库
    :return:
    """
    upload_file = UploadFile(category=1, match_id=distribute_project_id, uploader=uploader, filename=filename,
                             # 存储文件记录至数据库
                             path=path, filename_hash=filename_hash)
    db.session.add(upload_file)
    db.session.commit()
    file_id = upload_file.id
    return file_id


def update_task_status(distribute_project_id, task_id, task_status):
    """
    更新任务的状态， 同时根据任务的状态更新项目中任务的完成量
    1. 任务状态未改变，直接返回
    2. 任务状态改变为已完成， 更新状态的同时，更新申报表中的完成数量
    :param distribute_project_id:
    :param task_id:
    :param task_status:
    :return:
    """
    task = ProjectDeclarationTask.query.get(task_id)
    old_status = str(task.status)
    if old_status == task_status:
        return True

    projectDeclaration = ProjectDeclaration.query.get(distribute_project_id)
    if old_status == '2':  # 任务原来的状态就是已完成，完成数量-1
        projectDeclaration.complete_num = projectDeclaration.complete_num - 1
    if task_status == '2':  # 任务先在状态为已完成，完成状态+1
        projectDeclaration.complete_num = projectDeclaration.complete_num + 1

    # 更新任务状态
    task.status = task_status
    db.session.commit()


def delete_task(task_id):
    """
    删除任务， 该申报的任务数量-1， 如果该任务已完成， 完成数量-1
    :param task_id:
    :return:
    """
    task = ProjectDeclarationTask.query.get(task_id)
    distribute_project_id = task.distribute_id
    projectDeclaration = ProjectDeclaration.query.get(distribute_project_id)
    projectDeclaration.task_num -= 1
    old_status = str(task.status)
    if old_status == '2':
        projectDeclaration.complete_num -= 1
    db.session.delete(task)
    db.session.commit()


def get_breadcrumbs(level, **kwargs):
    """
    :param level: 1 不需要参数 2需要department_id 3 需要project 4 如果有declaration_id 表示申报，否则是活动
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
                                'link': '.manage_project',
                                'args': {'department_id': department.id}})
        # 第三级 获取到project
        elif idx == 2:
            project_id = kwargs.get('project_id')
            project = Project.query.get_or_404(project_id)
            breadcrumbs.append({'name': project.name,
                                'link': '.show_project_list',
                                'args': {'project_id': project.id, "project_name": project.name}})
        # 显示企业
        elif idx == 3:
            declaration_id = kwargs.get('declaration_id')
            declaration = ProjectDeclaration.query.get_or_404(declaration_id)
            breadcrumbs.append({'name': declaration.ep_name})
        # 显示活动
        # elif idx == 3:
        #     breadcrumbs.append({'name': '活动'})
        idx += 1
    return breadcrumbs
