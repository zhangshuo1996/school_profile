"""
项目申报ajax异步调用部分
by zhang
"""
from flask_login import current_user
from flask import Blueprint, request
from web.models import ProjectDeclaration, ProjectDeclarationTask, ServiceProvider, ServiceProviderCategory
from web.utils import date2timestamp
from web.extensions import db
from web.service import project_declaration as project_declaration_service

project_declaration_ajax_bp = Blueprint("project_declaration_ajax", __name__)


@project_declaration_ajax_bp.route("/add_task", methods=["POST"])
def add_task():
    """
    用户增加任务
    by zhang
    :return:
    """
    agent_id = current_user.org_id
    ep_id = request.form.get("ep_id", type=int, default=None)
    distribute_project_id = request.form.get("distribute_project_id", type=int, default=None)
    project_id = request.form.get("project_id", type=int, default=None)
    add_task_name = request.form.get("add_task_name")
    add_task_executor = request.form.get("add_task_executor")
    add_task_start = request.form.get("add_task_start")
    add_task_end = request.form.get("add_task_end")
    add_task_default = request.form.get("add_task_default", type=bool)
    # add_task_file = request.files["add_task_file"]
    files = request.files
    if len(files) == 0:
        add_task_file = None
    else:
        add_task_file = files["add_task_file"]

    if add_task_default:  # 将该任务添加至模板
        # TODO：根模板文件的问题？？待解决
        result = project_declaration_service.add_task_template(agent_id, project_id, add_task_name, add_task_executor)
        if result["error"]:
            return result
    # 增加任务以及对应的文件
    result = project_declaration_service.add_declaration_task(agent_id, ep_id, add_task_name, distribute_project_id,
                                                              add_task_executor, add_task_start,
                                                              add_task_end, add_task_file, current_user.name)
    # 更新项目申报表中该申报的任务数量 TODO: 重构该部分
    projectDeclaration = ProjectDeclaration.query.get(distribute_project_id)
    projectDeclaration.task_num = projectDeclaration.task_num + 1
    db.session.commit()
    return result


@project_declaration_ajax_bp.route("/get_distribute_task")
def get_distribute_task():
    """
    获取某一项目下分配的任务
    by zhang
    :return:
    """
    distribute_project_id = request.args.get("distribute_project_id")
    declaration_project = ProjectDeclaration.query.get(distribute_project_id)
    # tasks, start_time, end_time = [], [], []
    tasks = [
        {
            "task_id": task.id,
            "company_id": task.agent_id,
            "ep_id": task.ep_id,
            "distribute_project_id": task.distribute_id,
            "task_name": task.task_name,
            "executor": task.executor,
            "gmt_create": task.get_gmt_create(),
            "gmt_deadline": task.get_gmt_deadline(),
            "status": task.status,
            "file_id": task.file_id
        }
        for task in declaration_project.tasks
    ]
    start_time = [task.gmt_create for task in declaration_project.tasks]
    end_time = [task.gmt_deadline for task in declaration_project.tasks]
    result = {
        "success": True,
        "data": tasks,
        "mode": compute_time_difference_level(start_time=min(start_time) if len(start_time) > 0 else 0,
                                              end_time=max(end_time) if len(end_time) > 0 else 0)
    }
    return result


@project_declaration_ajax_bp.route("/update_task_start_end", methods=['POST'])
def update_task_start_end():
    """
    根据任务id更新该任务的起止时间
    by zhang
    :return:
    """
    task_id = request.form.get("task_id", type=int, default=None)
    start = request.form.get("start")
    end = request.form.get("end")
    task = ProjectDeclarationTask.query.get(task_id)
    task.gmt_create = start
    task.get_gmt_deadline = end
    return {"success": True}


@project_declaration_ajax_bp.route("/update_task_progress", methods=['POST'])
def update_task_progress():
    """
    根据任务id更新该任务的起止时间
    by zhang
    TODO 待删除
    :return:
    """
    task_id = request.form.get("task_id", type=int, default=None)
    progress = request.form.get("progress", type=int, default=None)
    distribute_project_id = request.form.get("distribute_project_id", type=int, default=None)
    task = ProjectDeclarationTask.query.get(task_id)
    task.progress = progress
    db.session.commit()

    declaration_project = ProjectDeclaration.query.get(distribute_project_id)
    tasks = declaration_project.tasks
    avg_progress = project_declaration_service.cal_project_declaration_progress(tasks)
    declaration_project.progress = avg_progress
    db.session.commit()
    return {"success": True}


@project_declaration_ajax_bp.route("/update_task", methods=['POST'])
def update_task():
    """
    更新任务中的字段
    :return:
    """
    # TODO: 政府用户的权限
    agent_id = current_user.org_id
    task_id = request.form.get("task_id", type=int, default=None)
    project_id = request.form.get("project_id", type=int, default=None)
    task_name = request.form.get("task_name")
    executor = request.form.get("executor")
    start = request.form.get("start")
    end = request.form.get("end")
    task_status = request.form.get("task_status")
    default = request.form.get("default")
    files = request.files
    if len(files) == 0:  # 判断是否上传了文件
        task_file = None
    else:
        task_file = request.files["update_task_file"]

    if default == "true":  # 更新或者增加模板表中的数据
        result = project_declaration_service.update_or_add_task_template(agent_id, project_id, task_name, executor)
        if result is False:
            return {"error": True}
    task = ProjectDeclarationTask.query.get(task_id)

    file_id = task.file_id  # 记录旧的file_id
    if task_file is not None:  # 存储文件至文件系统， 存储文件记录至数据库
        filename_hash = project_declaration_service.store_file(task_file)
        distribute_id = task.distribute_id
        # 文件记录入库，记录新的file_id
        file_id = project_declaration_service.store_file_record(distribute_project_id=distribute_id,
                                                                uploader=current_user.name, filename=task_file.filename,
                                                                filename_hash=filename_hash)

    # 更新任务中表中的字段
    task.task_name = task_name
    # task.status = task_status
    task.gmt_create = date2timestamp(start)
    task.gmt_deadline = date2timestamp(end)
    task.executor = executor
    # 替换旧的file_id
    task.file_id = file_id
    db.session.commit()

    # 更新任务的状态， 同时更新任务的完成量
    project_declaration_service.update_task_status(distribute_project_id=task.distribute_id, task_id=task_id,
                                                   task_status=task_status)

    return {"success": True}


@project_declaration_ajax_bp.route("/delete_task", methods=['POST'])
def delete_task():
    """
    删除任务
    :return:
    """
    task_id = request.form.get("task_id", type=int, default=None)
    project_declaration_service.delete_task(task_id)
    return {"success": True}


@project_declaration_ajax_bp.route("/get_sp_info")
def get_sp_info():
    """
    获取服务商的信息
    :return:
    """
    agent_id = current_user.org_id
    service_providers = ServiceProvider.query.filter(ServiceProvider.agent_id == agent_id)
    sps = [
        {
            "sp_id": sp.id,
            "name": sp.name,
            "charger": sp.charger,
            "telephone": sp.telephone
        }
        for sp in service_providers
    ]
    return {"success": True, "data": sps}


def compute_time_difference_level(start_time=0, end_time=0):
    """
    计算两个时间戳（秒级）之间的时间差，返回时间间隔对应的 甘特图展示等级
    1~30天 ： Day 模式
    30~60天 ： Week 模式
    2个月~12个月 ： Month 模式
    > 1年： Year 模式
    """
    day = (end_time - start_time) // (3600 * 24)
    if day < 30:
        return "Day"
    elif day < 30 * 2:
        return "Week"
    elif day < 30 * 12:
        return "Month"
    return "Year"


@project_declaration_ajax_bp.route("/get_all_sp_category")
def get_all_sp_category():
    """
    获取所有的服务商类型
    :return:
    """
    categories = ServiceProviderCategory.query.filter().all()
    data = [
        {
            "id": category.id,
            "name": category.name
        }
        for category in categories
    ]
    return {"success": True, "data": data}


@project_declaration_ajax_bp.route("/add_sp")
def add_sp():
    """
    增加服务商
    :return:
    """
    sp_name = request.args.get("sp_name")
    category_id = request.args.get("category_id")
    charger = request.args.get("charger")
    telephone = request.args.get("telephone")
    sp = ServiceProvider(
        name=sp_name,
        category_id=category_id,
        charger=charger,
        telephone=telephone,
        status=1,
        agent_id=current_user.org_id,
    )
    db.session.add(sp)
    db.session.commit()
    return {"success": True}


@project_declaration_ajax_bp.route("/delete_sp")
def delete_sp():
    """
    删除服务商
    :return:
    """
    sp_id = request.args.get("sp_id")
    sp = ServiceProvider.query.get(sp_id)
    db.session.delete(sp)
    db.session.commit()
    return {"success": True}
