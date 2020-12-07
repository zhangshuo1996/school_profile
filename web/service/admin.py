from web.dao.statistics import get_admin_list
from web.models import User, Agent, Department


def get_user(category, name, phone, org, is_admin):
    # 得到管理员ID列表
    admins = get_admin_list()
    admin_list = []
    for item in admins:
        admin_list.append(item['id'])
    # 检索用户
    user_query = User.query.filter_by(is_active=1)
    if category != 0:
        user_query = user_query.filter_by(category_id=category)
    if name:
        user_query = user_query.filter(User.name.contains(name))
    if phone:
        user_query = user_query.filter(User.telephone.contains(phone))
    if org:
        org_list = []
        agents = Agent.query.filter(Agent.name.contains(org)).all()
        for agent in agents:
            org_list.append(agent.id)
        departments = Department.query.filter(Department.name.contains(org)).all()
        for department in departments:
            org_list.append(department.id)
        user_query = user_query.filter(User.org_id.in_(org_list))
    if is_admin:
        users = user_query.filter(User.id.in_(admin_list)).all()
    else:
        users = user_query.filter(~User.id.in_(admin_list)).all()
    return users