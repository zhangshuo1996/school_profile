from flask import url_for
from sqlalchemy import and_

from web.models import Activity


# 日历上的显示类型
SHOW_TYPE = {
    0: "event-important",
    1: "event-warning",
    2: "event-info",
    3: "event-inverse",
    4: "event-success",
    5: "event-special"
}


def get_activities_by_time(from_time, to_time):
    """
    根据时间获取所有的活动，并转换格式
    :param from_time: 起始时间
    :param to_time: 结束时间
    :return: 活动数据
    """
    # 获取活动
    activities = Activity.query.filter(and_(Activity.gmt_start > from_time, Activity.gmt_end <= to_time)).all()
    # 转换结构
    results = [{
        'id': activity.id,
        'title': activity.title,
        'url': url_for('activity.show_base_info', activity_id=activity.id),
        'class': SHOW_TYPE[activity.id % 6],
        'start': activity.gmt_start * 1000,
        'end': activity.gmt_end * 1000,
    } for activity in activities]
    return results


def get_breadcrumbs(level, **kwargs):
    """
    :param level: 1 不需要参数 2需要department_id 3 需要project 4 如果有declaration_id 表示申报，否则是活动
    :param kwargs:
    :return:
    """
    breadcrumbs = [{'name': "活动日历"}]
    if level > 1:
        breadcrumbs = [{'name': "活动日历", "link": ".index", "args": {"": ""}}]
    if level == 2:
        activity_name = kwargs.get("activity_name")
        breadcrumbs.append({'name': activity_name})

    return breadcrumbs