from web.dao.school_profile import profile as profile_dao
from web.service.school_profile.CalScore import CalSchoolScore, CalInstitutionScore, CalTeamScore
from web.service.school_profile import RelationshipService as relationService
from flask import send_from_directory
import os
from web.utils import Ego_net as ego_net


def get_school_header_logo(school, path, avatar_path):
    """
    展示学校画像中最上方的图片中的学校图标
    """
    file_names = os.listdir(path)
    pic_file_name = ""
    for file_name in file_names:
        if school in file_name and "logo" in file_name:
            pic_file_name = file_name
            break
    if pic_file_name == "":
        pic_file_name = school + ".png"
        return send_from_directory(avatar_path, pic_file_name)
    else:
        return send_from_directory(path, pic_file_name)


def get_industry_level_logo(logo_path, index):
    """
    获取行业等级logo
    :param logo_path:
    :param index:
    :return:
    """
    filename = str(index) + ".png"
    return send_from_directory(logo_path, filename)


def get_school_header_background(school, path):
    """
    展示学校画像中最上方图片中的背景
    """
    file_names = os.listdir(path)
    pic_file_name = "default_pic.png"
    for file_name in file_names:
        if school in file_name and "logo" not in file_name:
            pic_file_name = file_name
            break
    return send_from_directory(path, pic_file_name)


def get_school_profile_cover_background(path):
    """
    展示学校画像中最上方图片中的背景
    """
    file_names = "school_profile_cover.jpg"
    return send_from_directory(path, file_names)


def get_school_discipline(school):
    """
    获取学校的重点学科
    :param school:
    :return:
    """
    _data = profile_dao.get_school_discipline(school)
    return _data


def get_institution_list(school):
    """
    获取学院名单， 按照专利数量排序
    :param school:
    :return:
    """
    data = profile_dao.get_institution_patent_num(school)
    institution_list = []
    i = 0
    for dic in data:
        i += 1
        if i > 20:
            break
        institution_list.append(dic["institution"])
    return institution_list


def get_school_is_exist(school):
    """
    判断该高校是否存在
    :param school:
    :return:
    """
    data = profile_dao.get_school_is_exist(school)
    if data is None or len(data) == 0:
        return False
    else:
        return True


def get_all_schools():
    """
    获取所有学校列表， 按专利排序
    :return:
    """
    data = profile_dao.get_all_schools()
    school_list = [dic["school"] for dic in data]
    return school_list


def get_used_schools(user_id):
    """
    获取这个用户最常用的十所高校
    :param user_id:
    :return:
    """
    data = profile_dao.get_used_schools(user_id)
    used_schools = [dic["school"] for dic in data]
    return used_schools


def get_province_school():
    """
    获取各个省份对应的高校， 省份 按照高校数量排序 高校 按照专利数量排序
    :return:
    """
    data = profile_dao.get_province_school()
    province_list = []
    province_school_dict = dict()
    for dic in data:
        if dic["province"] == "" or dic["province"] is None:
            continue
        if dic["province"] not in province_list:
            province_list.append(dic["province"])
        if dic["province"] in province_school_dict.keys():
            province_school_dict[dic["province"]].append(dic["school"])
        else:
            province_school_dict[dic["province"]] = [dic["school"]]

    # // 二维列表， 省份下对应的学校
    province_school_list = [province_school_dict[province] for province in province_list]
    return province_list, province_school_list


def get_permission_schools(user_id):
    """
    获取该用户有权查看的高校
    :param user_id:
    :return:
    """
    result = profile_dao.get_permission_schools(user_id)
    school_list = [dic["school"] for dic in result]
    return school_list


# def judge_have_permission(user_id, school):
#     """
#     判断该用户是否有权限查看某高校的画像
#     :param user_id:
#     :param school:
#     :return:
#     """
#     # 获取该用户有权查看的高校列表
#     schools = get_permission_schools(user_id)
#     for permission_school in schools:
#         if permission_school == school:
#             return True
#     return False


def get_school_lab(school):
    """
    获取学院的实验平台
    :param school:
    :return:
    """
    _data = profile_dao.get_school_lab(school)
    result = []
    for dic in _data:
        if "国家" in dic["lab"] or "省" in dic["lab"]:
            result.append(dic)
    return result


def get_institution_patent_num(school):
    """
    获取某一学校各学院的专利数量
    :return:
    """
    _data = profile_dao.get_institution_patent_num(school)
    institutions = []
    series = []
    for dic in _data:
        institutions.append(dic["institution"])
        series.append(dic["cnt"])

    return {
        "institutions": institutions,
        "series": series
    }


def get_school_permission_by_user(user_id, school):
    """
    根据高校名以及用户id获取该用户对该高校的权限
    :param user_id:
    :param school:
    :return:  READ, WRITE, FORBIDDEN
    """
    result = profile_dao.get_school_permission_by_user(user_id, school)
    if result is None or len(result) == 0:
        return "FORBIDDEN"
    if result[0]["permission"] == "SCHOOL_PROFILE_READ":
        return "READ"
    if result[0]["permission"] == "SCHOOL_PROFILE_WRITE":
        return "WRITE"
    return "FORBIDDEN"


def get_teacher_name_by_id(team_id):
    """

    :param team_id:
    :return:
    """
    result = profile_dao.get_teacher_name_by_id(team_id)
    return result["name"]


def get_institution_dimension_info(school, institution):
    """
    获取学院的各维度信息
    :return:
    """
    # 1. 获取学院下所有的教师
    teacher_id_dict = profile_dao.get_institution_teacher_ids(school, institution)
    teacher_ids = [dic["id"] for dic in teacher_id_dict]
    # 2. 根据成员id获取这些成员中的头衔信息，专利数量，项目数量，所在的实验室列表
    dimension_info = get_teachers_info(list(teacher_ids), school)
    researcher_num = len(list(teacher_ids))
    # 3. 根据获取的各维度信息进行综合打分
    c = CalInstitutionScore()
    school_level_score = c.cal_school_score_by_discipline(dimension_info["good_discipline_num"])
    achieve_num = c.cal_achieve_score(dimension_info["patent_num"])
    researcher_num_score = c.cal_researcher_num_score(researcher_num)
    researcher_level_score = c.cal_researcher_level_score(dimension_info["academician_num"],
                                                          dimension_info["excellent_young"])
    lab_score = c.cal_lab_score(dimension_info["national_lab_num"], dimension_info["province_lab_num"])
    project_score = c.cal_project_num_score(dimension_info["project_num"])
    return {
        "school_level_score": school_level_score,
        "achieve_num": achieve_num,
        "researcher_num_score": researcher_num_score,
        "researcher_level_score": researcher_level_score,
        "lab_score": lab_score,
        "project_score": project_score
    }


def get_team_dimension_info(team_id, school):
    """
    获取团队的各维度信息
    :return:
    """
    # 1. 根据团队id获取该团队的所有成员id
    teacher_ids = relationService.get_teacher_team(teacher_id=team_id)
    # 2. 根据成员id获取这些成员中的头衔信息，专利数量，项目数量，所在的实验室列表
    dimension_info = get_teachers_info(list(teacher_ids), school)
    researcher_num = len(list(teacher_ids))
    # 3. 根据获取的各维度信息进行综合打分
    c = CalTeamScore()
    school_level_score = c.cal_school_score_by_discipline(dimension_info["good_discipline_num"])
    achieve_num = c.cal_achieve_score(dimension_info["patent_num"])
    researcher_num_score = c.cal_researcher_num_score(researcher_num)
    researcher_level_score = c.cal_researcher_level_score(dimension_info["academician_num"],
                                                          dimension_info["excellent_young"])
    lab_score = c.cal_lab_score(dimension_info["national_lab_num"], dimension_info["province_lab_num"])
    project_score = c.cal_project_num_score(dimension_info["project_num"])
    return {
        "school_level_score": school_level_score,
        "achieve_num": achieve_num,
        "researcher_num_score": researcher_num_score,
        "researcher_level_score": researcher_level_score,
        "lab_score": lab_score,
        "project_score": project_score
    }


def get_teachers_info(teacher_ids, school):
    """
    根据多个教师的id获取这些教师的基本信息、学校信息、成果信息
    :param school:
    :param teacher_ids:
    :return:
    """
    # 1. 获取教师的实验平台信息， 荣誉信息（院士，长江...)
    lab_honor_info = profile_dao.get_labs_honors_by_teacher_ids(teacher_ids)
    academician_num, excellent_young, national_lab_num, province_lab_num = statistic_lab_honor_info(lab_honor_info)
    # 2. 获取多个教师的的拥有的专利数量
    patents = profile_dao.get_patent_num_by_teacher_ids(teacher_ids)
    patent_num = len(patents)
    # 3. 获取这些学校的一流学科数量，证明其学校水平
    discipline = profile_dao.get_good_discipline_num_by_school(school)
    discipline_num = discipline[0]["cnt"]
    # 4. 获取这一团队的项目数量
    try:
        project_num = profile_dao.get_project_num_by_teacher_ids(teacher_ids)["cnt"]
    except Exception as e:
        project_num = 0
    dimensions_info = {
        "academician_num": academician_num,  # 院士数量
        "excellent_young": excellent_young,  # 长江、杰青数量
        "national_lab_num": national_lab_num,  # 是否有国家、教育部重点实验室
        "province_lab_num": province_lab_num,  # 是否有省级重点实验室
        "patent_num": patent_num,  # 专利数量
        "good_discipline_num": discipline_num,  # 该学校的一流学科数量
        "project_num": project_num
    }
    return dimensions_info


def statistic_lab_honor_info(lab_honor_info):
    """
    根据一个学校中所有教师的荣誉与实验室信息，统计该学校下的荣誉与实验室信息
    :param lab_honor_info:
    :return:
    """
    academician_num = 0
    excellent_young = 0
    national_lab_num = 0
    province_lab_num = 0
    for dic in lab_honor_info:
        lab = dic["lab"] if dic["lab"] is not None else ""
        honor = dic["honor"] if dic["honor"] is not None else ""
        if "国家" in lab or "教育部" in lab:
            national_lab_num += 1
        if "省" in lab:
            province_lab_num += 1

        if "长江" in honor or "杰青" in honor:
            excellent_young += 1
        if "院士" in honor:
            academician_num += 1

    return academician_num, excellent_young, national_lab_num, province_lab_num


def get_school_normalize_dimension_score(school):
    """
    获取学校归一化之后的各维度分数
    TODO: 评分指标待调整，目前使用的评分是对团队各项指标的评分标准
    :return:
    """
    # 1. 获取学校中所有教师的头衔信息，专利数量，项目数量，所在的实验室列表
    dimension_info = get_school_dimensions_info(school)
    # 2. 根据获取的各维度信息进行综合打分
    c = CalSchoolScore()
    school_level_score = c.cal_school_score_by_discipline(dimension_info["good_discipline_num"])
    achieve_num = c.cal_achieve_score(dimension_info["patent_num"])
    researcher_num_score = c.cal_researcher_num_score(dimension_info["researcher_num"])
    researcher_level_score = c.cal_researcher_level_score(dimension_info["academician_num"],
                                                          dimension_info["excellent_young"])
    lab_score = c.cal_lab_score(dimension_info["national_lab_num"], dimension_info["province_lab_num"])
    return {
        "school_level_score": school_level_score,
        "achieve_num": achieve_num,
        "researcher_num_score": researcher_num_score,
        "researcher_level_score": researcher_level_score,
        "lab_score": lab_score,
    }


def get_school_dimensions_info(school):
    """
    获取该学校的各维度信息
    :param school:
    :return: {
                "academician_num": academician_num,    # 院士数量
                "excellent_young": excellent_young,    # 杰青数量
                "national_lab_num": national_lab_num,  # 国家、教育部重点实验室数量
                "patent_num": patent_num,              # 专利数量
                "good_discipline_num": discipline_num, # 该学校的一流学科数量
            }
    """
    # 获取该学校下教师的荣誉与实验室信息
    lab_honor_info = profile_dao.get_school_teacher_info(school)
    academician_num, excellent_young, national_lab_num, province_lab_num = statistic_lab_honor_info(lab_honor_info)
    # 获取该学校下教师的专利数量
    patent_num = profile_dao.get_school_teacher_patent_num(school)["cnt"]
    # 获取这些学校的一流学科数量，证明其学校水平
    discipline = profile_dao.get_good_discipline_num_by_school(school)
    discipline_num = discipline[0]["cnt"]
    # 获取该学校的研究人员数量
    researcher_num = profile_dao.get_school_teacher_num(school)["cnt"]
    # 获取学校下的项目数量
    project_num = profile_dao.get_project_num_by_school(school)["cnt"]
    dimensions_info = {
        "academician_num": academician_num,  # 院士数量
        "excellent_young": excellent_young,  # 长江、杰青数量
        "national_lab_num": national_lab_num,  # 是否有国家、教育部重点实验室
        "province_lab_num": province_lab_num,  # 是否有省级重点实验室
        "patent_num": patent_num,  # 专利数量
        "good_discipline_num": discipline_num,  # 该学校的一流学科数量
        "researcher_num": researcher_num,  # 该学校研究人员数量
        "project_num": project_num,  # 该学校项目的数量
    }
    return dimensions_info


def get_institution_industry_distribution(school):
    """
    获取某一学校下学院的行业数据
    :param school:
    :return:
    """
    data = profile_dao.get_institution_industry_distribution(school)
    industry_institution_patentNum_dict = {}

    # 从data中获取该学校下学院对应的专利数量
    institution_patent_num_dict = {}
    # 从data中获取该学校下行业对应的专利数量
    industry_patent_num_dict = {}
    for dic in data:

        if dic["industry"] in industry_institution_patentNum_dict.keys():
            industry_institution_patentNum_dict[dic["industry"]][dic["institution"]] = dic["count"]
        else:
            industry_institution_patentNum_dict[dic["industry"]] = {dic["institution"]: dic["count"]}

        if dic["institution"] in institution_patent_num_dict.keys():
            institution_patent_num_dict[dic["institution"]] += dic["count"]
        else:
            institution_patent_num_dict[dic["institution"]] = dic["count"]

        if dic["industry"] in industry_patent_num_dict.keys():
            industry_patent_num_dict[dic["industry"]] += dic["count"]
        else:
            industry_patent_num_dict[dic["industry"]] = dic["count"]
    # 按专利数量得到该学校下的学院列表
    sorted_institution_patent_list = sorted(institution_patent_num_dict.items(), key=lambda x: x[1], reverse=True)
    # sorted_institution_list = [tup[0] for tup in sorted_institution_patent_list if tup[1] > 100]
    sorted_institution_list = []
    i = 0
    for tup in sorted_institution_patent_list:
        if i > 15:
            break
        sorted_institution_list.append(tup[0])
        i += 1

    # 按专利数量得到该学校下的行业列表
    sorted_industry_patent_list = sorted(industry_patent_num_dict.items(), key=lambda x: x[1], reverse=True)
    sorted_industry_list = [tup[0] for tup in sorted_industry_patent_list if tup[1] > 20]

    industry_institution_list_dict = {}
    for industry in sorted_industry_list:
        industry_institution_list_dict[industry] = []
        for institution in sorted_institution_list:
            if institution in industry_institution_patentNum_dict[industry].keys():
                industry_institution_list_dict[industry].append(
                    industry_institution_patentNum_dict[industry][institution])
            else:
                industry_institution_list_dict[industry].append(0)

    return {
        "institution_list": sorted_institution_list,
        "industry_institution_list_dict": industry_institution_list_dict
    }


def get_school_industry(school):
    """
    获取一所学校下主要的行业数量
    :return:
    """
    data = profile_dao.get_school_industry(school)
    legend = []
    series = []
    i = 0
    other_num = 0
    for dic in data:
        i += 1
        if i > 15:
            other_num += int(dic["cnt"])
        else:
            series.append({
                "name": dic["industry"],
                "value": int(dic["cnt"])
            })
            legend.append(dic["industry"])
    series.append({
        "name": "其他",
        "value": other_num
    })
    legend.append("其他")
    return {
        "seriesName": "",
        "series": series,
        "legend": legend
    }


def get_institution_by_industry(industry):
    """
    根据行业获取该行业下成果所在的主要学院
    :param industry:
    :return:
    """
    data = profile_dao.get_institution_by_industry(industry)
    school_institution_list = []
    patent_num_list = []
    for dic in data:
        school_institution_list.append(dic["school"] + "\n" + dic["institution"])
        patent_num_list.append(dic["count"])
    school_institution_list.reverse()
    patent_num_list.reverse()
    return {
        "school_institution_list": school_institution_list,
        "patent_num_list": patent_num_list
    }


def get_institution_industry_patent_num2(school):
    """
    获取某学校下 各学院中的行业对应的成果数量 以及  学院本身的成果数量
    :return:
    """
    # 1. 获取学院-行业下的成果数量， 组合成{institution: {industry: num, ...}, ...} 字典
    institution_industry_achieve_list = profile_dao.get_institution_industry_achieve(school)
    institution_set = set()
    institution_industry_achieve_dict = {}
    for dic in institution_industry_achieve_list:
        institution_set.add(dic["institution"])
        if dic["institution"] in institution_industry_achieve_dict.keys():
            institution_industry_achieve_dict[dic["institution"]][dic["industry"]] = (
                dic["count"], dic["level"], dic["rank"])
        else:
            institution_industry_achieve_dict[dic["institution"]] = {
                dic["industry"]: (dic["count"], dic["level"], dic["rank"])}
    result = []

    # 组合返回的数据格式
    for institution, item in institution_industry_achieve_dict.items():
        sum_value = 0
        each_dict = {
            "category": institution,
            "name": institution,
            "path": institution,
        }
        child = []
        for industry, val in item.items():
            sum_value += val[0]
            child.append({
                "name": industry,
                "path": industry,
                "category": institution,
                "value": val[0]
            })
        each_dict["value"] = sum_value
        each_dict["children"] = child
        result.append(each_dict)
    return {
        "result": result,
        "institution_list": list(institution_set),
    }


def get_team_patent_project_data(team_id):
    """
    获取团队的专利 与 项目信息
    :param team_id:
    :return:
    """
    # 1. 获取团队内所有成员的id
    data = ego_net.get_member_id_by_team_id(team_id)
    teacher_ids = [dic["teacher.id"] for dic in data]

    # 2. 获取专利
    patent_info = profile_dao.get_patent_info_by_teacher_ids(teacher_ids)

    # 3. 获取项目
    project_info = profile_dao.get_project_info_by_teacher_ids(teacher_ids)

    return {
        "patent_info": patent_info,
        "project_info": project_info
    }


def get_teacher_patent_project_data(teacher_id):
    """
    获取团队的专利 与 项目信息, 与get_team_patent_project_data函数公用
    :param teacher_id:
    :return:
    """
    # 1. 获取团队内所有成员的id
    teacher_ids = [teacher_id]

    # 2. 获取专利
    patent_info = profile_dao.get_patent_info_by_teacher_ids(teacher_ids)

    # 3. 获取项目
    project_info = profile_dao.get_project_info_by_teacher_ids(teacher_ids)

    return {
        "patent_info": patent_info,
        "project_info": project_info
    }


def get_province_school_patent_num():
    """
    获取每个省份、城市、高校 的专利数量 用于生成旭日图
    :return: {
                "江苏省" : {
                        "南京市" : {
                            "南大"： 1111，
                            "东大"： 2222，
                            。。。
                        }，
                        。。。
                }，
                。。。。
            }
    """
    data = profile_dao.get_province_school_patent_num()
    province__city_school = {}  # 省份-城市-高校
    province__area_patent_num = {}  # 省份-区域-专利数量
    city__patent_num = {}  # 城市-专利数量
    school__patent_num = {}  # 高校专利数量
    for dic in data:
        province = dic["province"]
        city = dic["city"]
        if province in province__city_school.keys():
            if city in province__city_school[province].keys():
                province__city_school[province][city][dic["school"]] = dic["patent_num"]
            else:
                province__city_school[province][city] = {dic["school"]: dic["patent_num"]}
        else:
            province__city_school[province] = {
                city: {dic["school"]: dic["patent_num"]}
            }
    # for dic in data:
    #     province = dic["province"]
        if province in province__area_patent_num.keys():
            province__area_patent_num[province]["patent_num"] += dic["patent_num"]
        else:
            province__area_patent_num[province] = {
                "area": dic["area"],
                "area_code": dic["area_code"],
                "patent_num": dic["patent_num"]
            }

        if city in city__patent_num.keys():
            city__patent_num[city] += dic["patent_num"]
        else:
            city__patent_num = {city: dic["patent_num"]}

        school = dic["school"]
        if school in school__patent_num.keys():
            school__patent_num[school] += dic["patent_num"]
        else:
            school__patent_num = {school: dic["patent_num"]}

    return province__city_school, province__area_patent_num, city__patent_num, school__patent_num
