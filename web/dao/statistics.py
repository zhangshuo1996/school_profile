from web.utils import db


def get_affair_projects(affair_id):
    """
    获取某类业务下的所有项目id
    """
    sql = "select id from project where affair_id=:affair_id"
    return db.select(sql, {'affair_id': affair_id})


def get_activity_statistics_by_date(year, project_id):
    """
    获取project_id获取有关的活动数据
    :param year: 年份
    :param project_id: project的id
    :return: ['month': int, 'amount': int]
    """
    sql = """
    select FROM_UNIXTIME(gmt_start, "%c") month, count(1) amount from activity
    where FROM_UNIXTIME(gmt_start, "%Y")=:year and project_id=:project_id
    GROUP BY month order by month
    """
    return db.select(sql, {'year': year, 'project_id': project_id})


def get_active_distribute_projects_by_date(year, project_id):
    """
    按照年份获取属于该project的政策申报的数据
    :param year: 哪一年份
    :param project_id: 项目id
    :return: [{'month': int, amount: int}, ...]
    """
    sql = """
    select FROM_UNIXTIME(gmt_deadline, '%c') month, count(1) amount
    from agent_ep_project_distribute
    where FROM_UNIXTIME(start_time,'%Y')=:year and project_id=:project_id and `status` <> 2
    GROUP BY month order by month
    """
    return db.select(sql, {'year': year, 'project': project_id})


def get_recent_activities(project_id, limit):
    """
    按照项目id获取最近的活动
    :param project_id: int
    :param limit: 返回前几个
    :return:
    """
    sql = """
        select id activity_id, title, FROM_UNIXTIME(gmt_create, '%Y-%m-%d') gmt_create
        from activity
        where project_id=:project_id 
        order by gmt_create desc limit :limit
    """
    return db.select(sql, {'project_id': project_id, 'limit': limit})


def get_recent_activities_by_affair(affair_id, limit):
    """
    获取最近相关的活动
    """
    sql = """
        select a.id activity_id, a.title, FROM_UNIXTIME(gmt_create, '%Y-%m-%d') gmt_create
        from activity a
        JOIN project p on a.project_id = p.id
        where p.affair_id = :affair_id
        order by gmt_create desc limit :limit
    """
    return db.select(sql, {'affair': affair_id, 'limit': limit})


def get_agent_recent_activities(offset=0, limit=5):
    """
    获取全部中介（孵化器&众创空间）近期组织的活动
    企管科专用
    """
    sql = """
        select id, title, FROM_UNIXTIME(gmt_create, '%Y-%m-%d') as gmt_create
        from activity
        where  category = 1
        order by gmt_create desc 
        limit :offset,:limit
    """
    return db.select(sql, {'offset': offset, 'limit': limit})


def get_activity_statistics_by_agent(year, project_id):
    """
    按中介名称统计活动数量
    :param year: 年份
    :param project_id: 项目id
    :param category: 中介类别
    :return: ['name': str, 'amount': int]
    """
    sql = """
    select agent.name, count(1) amount
    from activity
    join agent on sponsor_id=agent.id
    where FROM_UNIXTIME(gmt_start, "%Y") =:year and project_id=:project_id and activity.user_id >= 1000000
    GROUP BY agent.name
    """
    return db.select(sql, {'year': year, 'project_id': project_id})


def get_activity_statistics_by_agent_affair(year, affair_id, category):
    """
    按中介名称统计活动数量
    :param year: 年份
    :param affair_id: affair id
    :param category: 中介类别
    :return: ['name': str, 'amount': int]
    """
    sql = """
    select agent.name, count(1) amount
    from activity
    join agent on sponsor_id=agent.id
    join project on project.id=project_id
    where FROM_UNIXTIME(gmt_start, "%Y") =:year and affair_id=:affair_id and activity.category=:category
    GROUP BY agent.name
    """
    return db.select(sql, {'year': year, 'affair_id': affair_id, 'category': category})


def get_declaration_statistics_by_agent(year, project_id):
    """
    按中介名称统计政策申报数量
    :param year: 年份
    :param project_id: 项目id
    :return: ['name': str, 'amount': int]
    """
    sql = """
    select agent.name, count(*) amount
    from agent_ep_project_distribute declaration
    join agent on declaration.agent_id=agent.id
    where FROM_UNIXTIME(start_time, '%Y')=:year and project_id=:project_id and declaration.status<>2
    group by agent.name;
    """
    return db.select(sql, {'year': year, 'project_id': project_id})


def get_declaration_statistics_by_agent_affair(year, affair_id):
    """
    按中介名称统计政策申报数量
    :param year: 年份
    :param affair_id: affair id
    :return: ['name': str, 'amount': int]
    """
    sql = """
    select agent.name, count(*) amount
    from agent_ep_project_distribute declaration
    join agent on declaration.agent_id=agent.id
    join project on project.id=declaration.project_id
    where FROM_UNIXTIME(start_time, '%Y')=:year and affair_id=:affair_id and declaration.status<>2
    group by agent.name;
    """
    return db.select(sql, {'year': year, 'affair_id': affair_id})


def get_agents_by_department(department_id):
    """
    获取负责该department_id的中介
    :param department_id:
    :return: [string, ...] 中介名称
    """
    sql = """
    select DISTINCT agent.name from user
    join user_role on user_role.user_id=user.id
    join role on role.id=user_role.role_id
    join agent on agent.id=user.org_id
    where user.category_id=2 and role.department_id=:department_id
    """
    return db.select(sql, {'department_id': department_id}, convert_list=True)


def get_declaration_statistics_by_agent_and_month(year, project_id):
    """
    按中介名和月份统计政策申报数量
    :param year: 年份
    :param project_id: 项目id
    :return: [{'name': 中介公司名称, 'month': 月份, 'amount': 数量}]
    """
    sql = """
    select agent.name,count(*) amount
    from project_declaration declaration
    join agent on declaration.agent_id=agent.id
    where FROM_UNIXTIME(start_time, '%Y')=:year and project_id=:project_id and declaration.status<>2
    group by agent.name order by amount;
    """
    return db.select(sql, {'year': year, 'project_id': project_id})


def get_iur_declaration_statistics_by_agent_and_month(year):
    """
    获取今年产学研中介每月的项目数量
    :param year:
    :param project_id:
    :return: [{'name': 中介公司名称, 'month': 月份, 'amount': 数量}]
    """
    sql = """
    SELECT agent.name, CAST(FROM_UNIXTIME(gmt_submit, '%m') AS UNSIGNED) month, count(*) amount 
    FROM `iur_contract` join agent on iur_contract.sponsor_id=agent.id
    where contract_year=:year group by agent.name, month order by agent.name, month;
    """
    return db.select(sql, {'year': year})


def get_declaration_statistics_by_agent_and_month_affair(year, affair_id):
    """
    按中介名和月份统计政策申报数量
    :param year: 年份
    :param affair_id: affair id
    :return: [{'name': 中介公司名称, 'month': 月份, 'amount': 数量}]
    """
    sql = """
    select agent.name, CAST(FROM_UNIXTIME(start_time, '%m')AS UNSIGNED) month, count(*) amount
    from agent_ep_project_distribute declaration
    join agent on declaration.agent_id=agent.id
    join project on project.id=project_id
    where FROM_UNIXTIME(start_time, '%Y')=:year and affair_id=:affair_id and declaration.status<>2
    group by agent.name, `month` order by agent.name,month;
    """
    return db.select(sql, {'year': year, 'affair_id': affair_id})


def get_activity_statistics_by_agent_and_month(year, project_id):
    """
    按中介名和月份统计活动数量
    :param year:
    :param project_id:
    :return:  [{'name': 中介公司名称, 'month': 月份, 'amount': 数量}]
    """
    sql = """select agent.name, count(*) amount
            from activity join agent on activity.sponsor_id=agent.id 
            where FROM_UNIXTIME(gmt_start, '%Y')=:year and project_id=:project_id
            group by agent.name order by agent.name
            """
    return db.select(sql, {'year': year, 'project_id': project_id})


def get_declaration_activities_by_agent_and_month_affair(year, affair_id):
    """
    按中介名和月份统计活动数量
    :param year:
    :param affair_id:
    :return: [{'name': 中介公司名称, 'month': 月份, 'amount': 数量}]
    """
    sql = """select agent.name, CAST(FROM_UNIXTIME(gmt_start, '%m') AS UNSIGNED) month, count(*) amount
             from activity join agent on activity.sponsor_id=agent.id
             join project on project.id=activity.project_id
             where FROM_UNIXTIME(gmt_start, '%Y')=:year and affair_id=:affair_id 
             group by agent.name, month order by agent.name, month
            """
    return db.select(sql, {'year': year, 'affair_id': affair_id})


def get_iur_tr_statistics_by_agent_and_month(year):
    """
    获取产学研数据
    :param year:
    :param project_id:
    :return:
    """
    sql = """
    SELECT agent.name, CAST(FROM_UNIXTIME(gmt_submit, '%m') AS UNSIGNED) month, sum(tr_num) amount
    from technical_requirements join agent on technical_requirements.sponsor_id=agent.id
    where FROM_UNIXTIME(gmt_submit, '%Y')=:year
    group by agent.name, month order by agent.name, month   
    """
    return db.select(sql, {'year': year})


def get_agents_of_selected_project(project_id):
    """
    获取选中了该project的中介
    :param project_id: project id
    :return: [str, ...]
    """
    sql = """
    SELECT DISTINCT agent.name FROM project_declaration
    join agent on project_declaration.agent_id=agent.id
    where project_declaration.project_id=:project_id
    """
    return db.select(sql, {'project_id': project_id})


def get_agents_of_selected_affair(affair_id):
    """
    获取选中了该affair的中介
    :param affair_id: affair id
    :return: [str, ...]
    """
    sql = """
    SELECT DISTINCT agent.name FROM `project_declaration`
    join agent on project_declaration.agent_id=agent.id
    where project_id= :project
    """
    return db.select(sql, {'affair_id': affair_id})


def get_department_functions(department_id, is_sidebar):
    """获取科室对应的侧边栏"""
    sql = """
    select endpoint, name, blueprint, icon from gov_function
    join department_function on department_function.function_id=gov_function.id
    where department_id=:department_id and is_sidebar=:is_sidebar
    """
    return db.select(sql, {'department_id': department_id, 'is_sidebar': is_sidebar})


def get_recent_tech_requirements(limit):
    sql = """SELECT id tr_id, ep_name, FROM_UNIXTIME(gmt_submit,  "%Y-%m-%d") gmt_submit 
             from technical_requirements order by gmt_submit desc limit :limit"""
    return db.select(sql, {'limit': limit})

def get_admin_list():
    sql = """select user.id from user 
    join user_role on user_role.user_id = user.id
    join role on role.id=user_role.role_id
    join role_permission on role_permission.role_id=role.id
    join permission on permission.id=role_permission.permission_id
    where permission.name in ('GOV_ADMINISTRATOR', 'AGENT_ADMINISTRATOR', 'SYSTEM_ADMINISTRATOR')"""
    return db.select(sql)

