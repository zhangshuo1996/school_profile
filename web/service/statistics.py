from sqlalchemy import func
from datetime import datetime

from web.extensions import db
from web.dao import statistics as statistics_dao
from web.utils import timestamp2day, timestamp2month, yearStart2timestamp
from web.models import ProjectDeclaration, Activity, Agent, ProjectResult, UploadFile, Project

cur_year = str(datetime.now().year)


def get_month_activity_declaration(project_id):
    """
    获取今年来 各月份 关于 某一项目的 活动和申报的 各月份 数量
    :param project_id:
    :return:
    """
    activity_list = get_month_activity_num(project_id)
    declaration_list = get_month_declaration_num(project_id)
    return {
        "activity": activity_list,
        "declaration": declaration_list,
    }


def get_month_activity_num(project_id):
    """
    获取今年来 各月份 关于 某一项目的 活动的 各月份 数量
    :param project_id:
    :return:
    """
    # 获取今年间的所有活动
    activities = Activity.query.filter(Activity.project_id == project_id, Activity.gmt_create >= yearStart2timestamp(),
                                       Activity.gmt_create < yearStart2timestamp(next_year=1))
    return format_month_activity_and_declaration_data(activities)


def get_month_declaration_num(project_id):
    """
    获取今年来 各月份 关于 某一项目的 申报的 各月份 数量
    :param project_id:
    :return:
    """
    # 获取
    declarations = ProjectDeclaration.query.filter(ProjectDeclaration.project_id == project_id,
                                                   ProjectDeclaration.gmt_create >= yearStart2timestamp(),
                                                   ProjectDeclaration.gmt_create < yearStart2timestamp(next_year=1))
    return format_month_activity_and_declaration_data(declarations)


def format_month_activity_and_declaration_data(data):
    """
    格式化截止到每个月的活动及申报总量
    """
    cur_month = datetime.now().month
    monthly_total_num = [0 for i in range(cur_month + 1)]
    for datum in data:
        month = int(timestamp2month(datum.gmt_create))
        monthly_total_num[month] += 1

    for i in range(1, len(monthly_total_num)):
        monthly_total_num[i] += monthly_total_num[i - 1]
    return monthly_total_num


def get_recent_activities(project_id):
    """
    根据project_id 获取最近的活动
    :param project_id:
    :return:
    """
    activities = Activity.query.filter_by(project_id=project_id).order_by(Activity.gmt_create.desc()).limit(5)
    data = [
        {   
            "activity_id": activity.id,
            "title": activity.title,
            "gmt_create": timestamp2day(activity.gmt_create)
        }
        for activity in activities
    ]
    return data


def get_recent_policies(project_id):
    """
    获取某类业务的政策文件
    """
    policies = UploadFile.query.filter(UploadFile.category == 3, UploadFile.match_id == project_id).order_by(
        "gmt_create").limit(5)
    data = [
        {
            "name": policy.filename,
            "ctime": policy.gmt_create,
            "file_id": policy.id
        }
        for policy in policies
    ]
    return data


def get_agent_rank_new(project: Project, category):
    """
    获取
    :param project: Project对象
    :param category: declaration 政策申报统计
    :return: agent_list, series
    """
    now = datetime.now()
    # 先获取负责该project的所有中介
    agent_list = statistics_dao.get_agents_by_department(project.department_id)
    data = []
    # 政策申报统计
    if category == "declaration":
        statistics = statistics_dao.get_declaration_statistics_by_agent_and_month(now.year, project.id)
    else:
        statistics = statistics_dao.get_activity_statistics_by_agent_and_month(now.year, project.id)
    # 转换成键值对
    mapping = {statistic['name']: statistic['amount'] for statistic in statistics}
    # 填充值，目前并未限定中介的数量
    for agent_name in agent_list:
        amount = mapping[agent_name] if agent_name in mapping else 0
        data.append(amount)
    series = [{
        'type': 'bar',
        'data': data,
        'barWidth': 10
    }]
    return agent_list, series


def get_complete_num(project_id):
    """
    获取各个中介的完成数量，以及其他完成量
    其他完成量 是 总的完成量 - 所有中介的完成量之和
    :param project_id:
    :return:
    """
    data = db.session.query(ProjectDeclaration.agent_id, func.count(ProjectDeclaration.id).label("c")).group_by(ProjectDeclaration.agent_id).filter_by(status=2, project_id=project_id).all()
    series = []
    legend = []
    agent_res_num = 0  # 该项目 中介总的完成量
    for tup in data:
        agent_id = tup[0]
        num = tup[1]
        agent_name = Agent.query.get(agent_id).name
        series.append({
            "name": agent_name,
            "value": num
        })
        legend.append(agent_name)
        agent_res_num += num

    # 获取该项目总的完成量
    project_result_num = ProjectResult.query.filter_by(project_id=project_id).count()
    series.append({
        "name": "其他",
        "value": project_result_num - agent_res_num
    })
    legend.append("其他")
    return {
        "seriesName": "中介该项目完成量对比",
        "series": series,
        "legend": legend
    }
