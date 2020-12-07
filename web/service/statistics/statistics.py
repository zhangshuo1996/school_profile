from web.dao import statistics as statistics_dao
from web.models import ProjectDeclaration, Activity
from web.utils import timestamp2month
from web.utils import timestamp2year
from datetime import datetime
cur_year = str(datetime.now().year)


def get_month_activity_declaration(project_id):
    """
    获取今年来 各月份 关于 某一项目的 活动和申报的 各月份 数量
    :param project_id:
    :return:
    """
    activity_list, month_list = get_month_activity_num(project_id)
    declaration_list = get_month_declaration_num(project_id)
    return {
        "activity": activity_list,
        "declaration": declaration_list,
        "month": month_list
    }


def get_month_activity_num(project_id):
    """
    获取今年来 各月份 关于 某一项目的 活动的 各月份 数量
    :param project_id:
    :return:
    """
    month_activity_num = get_init_month_dict()
    activities = Activity.query.filter(Activity.project_id == project_id)
    for activity in activities:
        gmt_create = activity.gmt_create
        year = str(timestamp2year(gmt_create))
        if year != cur_year:  # 过滤不是今年的活动
            continue
        month = timestamp2month(gmt_create)
        month_activity_num[month] = month_activity_num[month] + 1
    return list(month_activity_num.values()), list(month_activity_num.keys())


def get_month_declaration_num(project_id):
    """
    获取今年来 各月份 关于 某一项目的 申报的 各月份 数量
    :param project_id:
    :return:
    """
    declarations = ProjectDeclaration.query.filter(Activity.project_id == project_id)
    month_declaration_num = get_init_month_dict()
    for declaration in declarations:
        start_time = declaration.start_time
        year = str(timestamp2year(start_time))
        if year != cur_year:  # 过滤不是今年的申报
            continue
        month = timestamp2month(start_time)
        month_declaration_num[month] = month_declaration_num[month] + 1
    return list(month_declaration_num.values())


def get_init_month_dict():
    """
    返回最初始的月份及对应数量字典
    :return:
    """
    return {
        "01": 0,
        "02": 0,
        "03": 0,
        "04": 0,
        "05": 0,
        "06": 0,
        "07": 0,
        "08": 0,
        "09": 0,
        "10": 0,
        "11": 0,
        "12": 0,
    }


def get_agent_rank(project_id):
    """
    按中介名称统计项目申报数量和活动数量
    :param project_id: 仅仅统计该project_id对应的政策申报
    :param affair_id: 统计affair_id下的project_id对应的政策申报
    :return:
    months ['1', '2', ...,now.month]
    agents_lists[ [company 1,..company n], [],...[]] 长度为months长度
    res_data [[],[],...[]] 长度为months长度，为每个月每个中介项目数
    """
    if project_id is None:
        return {"error": True, "message": '获取数据失败，请刷新后重试'}

    now = datetime.now()
    months = [str(i+1) for i in range(now.month)]
    # [{'name': 中介公司名称, 'month': 月份, 'amount': 数量}]
    statistics = statistics_dao.get_declaration_statistics_by_agent_and_month(now.year, project_id)
    # [{'name': 中介公司名称, 'month': 月份, 'amount': 数量}]
    activity_statistics = statistics_dao.get_activity_statistics_by_agent_and_month(now.year, project_id)
    agents_list = []
    for statistic in statistics:
        if statistic.get('name') not in agents_list:
            agents_list.append(statistic.get('name'))
    for statistic in activity_statistics:
        if statistic.get('name') not in agents_list:
            agents_list.append(statistic.get('name'))
    res_data = []
    res_data_activity = []
    for month in months:
        data = [0 for i in agents_list]
        data_activity = [0 for i in agents_list]
        for statistic in statistics:
            if str(statistic.get("month")) == month:
                data[agents_list.index(str(statistic.get("name")))] = statistic.get("amount")
        for statistic_activity in activity_statistics:
            if str(statistic_activity.get("month")) == month:
                data_activity[agents_list.index(str(statistic_activity.get("name")))] = statistic_activity.get("amount")
        res_data.append(data)
        res_data_activity.append(data_activity)
    agents_lists = []
    for month in months:
        agents_lists.append(agents_list)

    return {
        'months': months,
        'agents_list': agents_lists,
        'data': res_data,
        'activity_data': res_data_activity
    }