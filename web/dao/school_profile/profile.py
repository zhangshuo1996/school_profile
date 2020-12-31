from web.utils import db


def get_school_discipline(school):
    """
    获取学校的重点学科
    :param school:
    :return:
    """
    sql = """
        select s.name, d.discipline, d.result
        from discipline_assess d
        LEFT JOIN school s
        on d.school_id = s.id
        where s.name=:school and d.result like "A%%" 
        ORDER BY FIELD(d.result, "A+", "A", "A-")
    """
    return db.select(sql, {"school": school}, bind='data_mining')


def get_school_introduction(school):
    """
    获取学校的简介
    :param school:
    :return:
    """
    sql = """
        select introduction
        from school
        where name=:school
    """
    return db.select_one(sql, {"school": school}, bind='data_mining')


def get_school_is_exist(school):
    """
    判断该高校是否存在
    :param school:
    :return:
    """
    sql = """
        select id
        from school
        where name=:school
    """
    return db.select(sql, {"school": school}, bind="data_mining")


def get_all_schools():
    """
    获取所有学校列表， 按专利排序
    :return:
    """
    sql = """
        select name school
        from school
        where patent_count is not null
        order by patent_count desc
    """
    return db.select(sql)


def get_used_schools(user_id):
    """
    获取这个用户最常用的十所高校
    :param user_id:
    :return:
    """
    sql = """
        select school, count(1) cnt
        from visit_school_history
        where user_id=:user_id
        group by school 
        order by cnt desc
        limit 10
    """
    return db.select(sql, {"user_id": user_id}, bind="data_mining")


def get_province_school():
    """
    获取各个省份对应的高校， 省份 按照高校数量排序 高校 按照专利数量排序
    :return:
    """
    sql = """
        select province, name school
        from school
        where patent_num > 0
        ORDER BY province_school_num desc, patent_num desc
    """
    data = db.select(sql, bind="data_mining")
    return data


def get_permission_schools(user_id):
    """
    获取该用户有权查看的高校
    :param user_id:
    :return:
    """
    sql = """
        select s.name school, p.`name` permission
        from user u
        LEFT JOIN user_role ur
        on u.id = ur.user_id
        LEFT JOIN role r
        on ur.role_id = r.id
        LEFT JOIN role_school rs
        on rs.role_id = r.id
        LEFT JOIN school s
        on rs.school_id = s.id
        LEFT JOIN role_permission rp
        on rp.role_id = r.id
        LEFT JOIN permission p
        on p.id = rp.permission_id
        where u.id=:user_id and s.name is not null and p.name is not null
        order by s.patent_count desc
    """
    return db.select(sql, {"user_id": user_id})


def get_school_permission_by_user(user_id, school):
    """
    获取该用户有权查看的高校
    :param school:
    :param user_id:
    :return:
    """
    sql = """
        select s.name school, p.`name` permission
        from user u
        LEFT JOIN user_role ur
        on u.id = ur.user_id
        LEFT JOIN role r
        on ur.role_id = r.id
        LEFT JOIN role_school rs
        on rs.role_id = r.id
        LEFT JOIN school s
        on rs.school_id = s.id
        LEFT JOIN role_permission rp
        on rp.role_id = r.id
        LEFT JOIN permission p
        on p.id = rp.permission_id
        where u.id=:user_id and s.name=:school
        limit 1
    """
    return db.select(sql, {"user_id": user_id, "school": school})


def get_school_lab(school):
    """
    获取学院的实验平台
    :param school:
    :return:
    """
    sql = """
        select i.lab
        from clean_inventor i
        LEFT JOIN school s
        on i.school_id = s.id
        where s.name=:school and i.lab like "%%国家%%"
        GROUP BY lab
    """
    return db.select(sql, {"school": school}, bind='data_mining')


def get_institution_patent_num(school):
    """
    获取某一学校各学院的专利数量
    :return:
    """
    sql = """
        select t.institution, t.cnt
        from 
        (
        select i.institution, count(i.institution) cnt
        from clean_inventor i
        LEFT JOIN school s
        on i.school_id = s.id
        LEFT JOIN clean_inventor_patent ip
        on i.id = ip.inventor_id
        LEFT JOIN patent p
        on ip.patent_id = p.id
        where s.name=:school and i.institution is not null and i.institution != ""
        GROUP BY i.institution
        ORDER BY cnt desc
        ) t
        where t.cnt > 500
        order by cnt desc
    """
    return db.select(sql, {"school": school}, bind='data_mining')


def get_institution_teacher_id(school, institution):
    """
    获取这个学院下的所有人 id
    :param school:
    :param institution:
    :return:
    """
    sql = """
        select  i.id teacher_id
        from clean_inventor i
        LEFT JOIN school s
        on i.school_id = s.id
        LEFT JOIN clean_inventor_patent ip
        on i.id = ip.inventor_id
        where s.name=:school and i.institution=:institution
        GROUP BY i.id
    """
    return db.select(sql, {"school": school, "institution": institution}, bind='data_mining')


def get_teacher_name_by_id(team_id):
    """

    :param team_id:
    :return:
    """
    sql = """
        select name
        from clean_inventor i
        where id=:team_id
    """
    return db.select_one(sql, {"team_id": team_id}, bind='data_mining')


def get_institution_teacher_ids(school, institution):
    """
    获取该学校该学院下的老师id
    :param school:
    :param institution:
    :return:
    """
    sql = """
        select i.id
        from clean_inventor i
        LEFT JOIN school s
        on i.school_id = s.id
        where s.name=:school and i.institution=:institution
    """
    return db.select(sql, {"school": school, "institution": institution}, bind='data_mining')


def get_labs_honors_by_teacher_ids(teacher_ids):
    """
    获取教师的实验平台信息， 荣誉信息（院士，长江..., bind='data_mining')
    :param teacher_ids:
    :return:
    """
    sql = """
        select lab, honor
        from clean_inventor 
        where id in (
    """
    if len(teacher_ids) == 0:
        return []
    for _id in teacher_ids:
        sql += str(_id) + ","
    sql = sql[0:-1]
    sql += ")"
    return db.select(sql, bind='data_mining')


def get_project_num_by_teacher_ids(teacher_ids):
    """
    根据多个教师id 获取这些人的项目总数
    :param teacher_ids:
    :return:
    """
    sql = """
        select count(1) cnt
        from clean_inventor i
        LEFT JOIN funds p
        on i.id = p.teacher_id
        where i.id in (
    """
    if len(teacher_ids) == 0:
        return []
    for _id in teacher_ids:
        sql += str(_id) + ","
    sql = sql[0:-1]
    sql += ")"
    return db.select_one(sql, bind='data_mining')


def get_project_num_by_school(school):
    """
    根据多个教师id 获取这些人的项目总数
    :param school:
    :return:
    """
    sql = """
        select count(1) cnt
        from clean_inventor i
        LEFT JOIN funds p
        on i.id = p.teacher_id
        left join school s 
        on s.id = i.school_id
        where s.name=:school
    """
    return db.select_one(sql, {"school": school}, bind='data_mining')


def get_patent_num_by_teacher_ids(teacher_ids):
    """
    获取多个教师的所有专利id,以此获取其成果数量
    :param teacher_ids:
    :return:
    """
    sql = """
        select ip.patent_id
        from clean_inventor i
        LEFT JOIN clean_inventor_patent ip
        on i.id = ip.inventor_id
        where i.id in (
    """
    if len(teacher_ids) == 0:
        return []
    for _id in teacher_ids:
        sql += str(_id) + ","
    sql = sql[0:-1]
    sql += ") GROUP BY ip.patent_id"
    return db.select(sql, bind='data_mining')


def get_good_discipline_num_by_school(school):
    """
    获取这些学校的一流学科数量
    :param school:
    :return:
    """
    sql = """
        select count(1) cnt
        from discipline_assess
        where school=:school and result like "A%%" 
    """
    return db.select(sql, {"school": school}, bind='data_mining')


def get_school_teacher_info(school):
    """
    获取该学校下的教师 实验室、人员荣誉信息
    :param school:
    :return:
    """
    sql = """
        select i.lab, i.honor
        from clean_inventor i
        LEFT JOIN school s
        on i.school_id = s.id
        where s.name=:school
    """
    return db.select(sql, {"school": school}, bind='data_mining')


def get_school_teacher_patent_num(school):
    """
    获取该学校下教师的专利数量
    :param school:
    :return:
    """
    sql = """
        select count(1) cnt
        from (
        select ip.patent_id
        from clean_inventor i
        LEFT JOIN school s
        on i.school_id = s.id
        LEFT JOIN clean_inventor_patent ip
        on ip.inventor_id = i.id
        where s.name=:school
        GROUP BY ip.patent_id
        ) t
    """
    return db.select_one(sql, {"school": school}, bind='data_mining')


def get_school_teacher_num(school):
    """
    获取学校下的研究人员数量
    :param school:
    :return:
    """
    sql = """
        select count(1) cnt
        from (
        select ip.inventor_id
        from clean_inventor i
        LEFT JOIN school s
        on i.school_id = s.id
        LEFT JOIN clean_inventor_patent ip
        on ip.inventor_id = i.id
        where s.name=:school and institution is not null
        GROUP BY ip.inventor_id
        ) t
    """
    return db.select_one(sql, {"school": school}, bind='data_mining')


def get_institution_industry_distribution(school):
    """
    获取某一学校下学院的行业数据
    :param school:
    :return:
    """
    sql = """
        select institution, industry, count
        from institution_industry2
        where school=:school
    """
    return db.select(sql, {"school": school}, bind="data_mining")


def get_school_industry(school):
    """
    获取一所学校下主要的行业数量
    :return:
    """
    sql = """
        select industry, sum(count) cnt
        from institution_industry2 
        where school=:school
        GROUP BY industry 
        ORDER BY cnt desc
    """
    return db.select(sql, {"school": school}, bind="data_mining")


def get_institution_by_industry(industry):
    """
    根据行业获取该行业下成果所在的主要学院
    :param industry:
    :return:
    """
    sql = """
            select school, institution, count
            from institution_industry2
            where industry=:industry
            ORDER BY count desc
            limit 15
        """
    return db.select(sql, {"industry": industry}, bind="data_mining")


def get_sorted_institution_list(school):
    """
    获取某学校下的学院名单， 按照成果数量排序
    :param school:
    :return:
    """
    sql = """
        select institution, sum(count) s
        from institution_industry2
        where school=:school
        GROUP BY institution 
        ORDER BY s desc
        limit 20
    """
    return db.select(sql, {"school": school}, bind="data_mining")


def get_sorted_industry_list(school):
    """
    获取某学校下的行业名单， 按照成果数量排序
    :param school:
    :return:
    """
    sql = """
            select industry, sum(count) s
            from institution_industry2
            where school=:school
            GROUP BY industry 
            ORDER BY s desc
            limit 30
        """
    return db.select(sql, {"school": school}, bind="data_mining")


def get_institution_industry_achieve(school):
    """
    获取某学校下学院-行业对应的成果数量
    :param school:
    :return:
    """
    sql = """
        select institution, industry, count, level, outcome rank
        from institution_industry2
        where school=:school
        order by count desc
        limit 100
    """
    return db.select(sql, {"school": school}, bind="data_mining")


# def get_school_industry_level_num():
#     """
#     获取所有学校下各等级的行业数量
#     :return:
#     """
#     sql = """
#         select school, level - 1 as level, count(id) cnt
#         from institution_industry2
#         GROUP BY school, level
#         ORDER BY school, level
#     """
#     return db.select(sql, bind="data_mining")


# 该函数用于论文测试使用，与实际系统无关
def get_seu_industry_distribution():
    """
    获取seu下的行业分布
    :return:
    """
    sql = """
        select ci.institution, ind.title
        from clean_inventor ci
        LEFT JOIN school s
        on ci.school_id = s.id
        LEFT JOIN clean_inventor_patent cip
        on cip.inventor_id = ci.id
        LEFT JOIN new_patent_industry npi
        on npi.patent_id = cip.patent_id
        LEFT JOIN patent p
        on cip.patent_id = p.id
        LEFT JOIN industry ind
        on npi.industry_code = ind.code
        where npi.patent_id is not null and ci.institution is not null and s.name = "东南大学" 
    """
    return db.select(sql, bind="data_mining")


def get_patent_info_by_teacher_ids(teacher_ids):
    """
    根据多个教师的id,以此获取其专利信息
    :param teacher_ids:
    :return:
    """
    sql = """
        select ip.patent_id, p.title
        from clean_inventor i
        LEFT JOIN clean_inventor_patent ip
        on i.id = ip.inventor_id
        LEFT JOIN patent p
        on ip.patent_id = p.id
        where p.category = 1 and i.id in  (
    """
    if len(teacher_ids) == 0:
        return []
    for _id in teacher_ids:
        sql += str(_id) + ","
    sql = sql[0:-1]
    sql += ") limit 6 "
    return db.select(sql, bind='data_mining')


def get_project_info_by_teacher_ids(teacher_ids):
    """
    根据多个教师的id,以此获取其专利信息
    :param teacher_ids:
    :return:
    """
    sql = """
        select name
        from funds 
        where category = 1 and teacher_id in  (
    """
    if len(teacher_ids) == 0:
        return []
    for _id in teacher_ids:
        sql += str(_id) + ","
    sql = sql[0:-1]
    sql += ") GROUP BY name limit 6 "
    return db.select(sql, bind='data_mining')


def get_province_school_patent_num():
    """
    获取每个省份、城市、高校 的专利数量 用于生成旭日图
    :return:
    """
    sql = """
        select name school, province, city, patent_num
        from school
        where patent_num is not null
        order by patent_num desc 
        limit 100
    """
    return db.select(sql, bind="data_mining")

