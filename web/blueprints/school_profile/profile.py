"""
画像部分
"""
from flask import Blueprint, current_app, send_from_directory
from flask import render_template, request
from flask_login import current_user, login_required
from web.service.school_profile import RelationshipService as relationService
from web.service.school_profile import profile as profile_service
import time
import logging

school_profile_bp = Blueprint("school_profile", __name__)


@school_profile_bp.route("/school_card", methods=["POST", "GET"])
# @login_required
def school_card():
    """
    展示学校卡片
    :return:
    """
    school = request.form.get("school", None)
    if school is None:
        schools = profile_service.get_all_schools()
        return render_template("school_profile/school_card.html", schools=schools)
    else:
        # 判断该高校是否存在
        is_exist = profile_service.get_school_is_exist(school)
        if is_exist:
            return render_template("school_profile/school_card.html", schools=[school])
        else:
            return render_template("school_profile/school_card.html", schools=[])


@school_profile_bp.route("/school_entrance")
def school_entrance():
    """
    高校画像入口 学校 检索框
    :return:
    """
    # 1. 获取常用的几所学校
    # user_id = current_user.id
    # used_schools = profile_service.get_used_schools(user_id)
    used_schools = ["东南大学", "浙江大学", "南京大学", "清华大学", "华南理工大学"]
    # 2. 获取各区域的几所学校
    province_list, province_school_list = profile_service.get_province_school()
    # 3. 获取所有高校
    schools = profile_service.get_all_schools()
    return render_template("school_profile/school_entrance.html", schools=schools, used_school=used_schools, province_list=province_list, province_school_list=province_school_list)


@school_profile_bp.route("/index/<school>")
# @login_required
def index(school):
    """
    画像展示界面,
    :return:
    """
    # TODO: 判断该用户是否有权限查看某高校
    # have_permission = profile_service.judge_have_permission(user_id=current_user.id, school=school)
    # if not have_permission:
    #     flash("您没有权限查看此高校, 请联系管理员分配权限", "danger")
    #     return redirect_back()

    labs = profile_service.get_school_lab(school=school)
    disciplines = profile_service.get_school_discipline(school)
    institutions = profile_service.get_institution_list(school)
    data = profile_service.get_institution_industry_distribution(school)
    return render_template("school_profile/profile.html", school=school, labs=labs, institutions=institutions, disciplines=disciplines, data=data)


@school_profile_bp.route("/school_logo/<school>")
# @login_required
def school_logo(school):
    """
    寻找头像
    """
    avatar_path = current_app.config["SCHOOL_AVATAR_PATH"]
    return send_from_directory(avatar_path, school + '.png')


@school_profile_bp.route("/school_header_logo/<school>")
# @login_required
def school_header_logo(school):
    """
    展示学校画像中最上方的图片
    """
    path = current_app.config["SCHOOL_HEADER_PATH"]
    avatar_path = current_app.config["SCHOOL_AVATAR_PATH"]
    return profile_service.get_school_header_logo(school, path, avatar_path)


@school_profile_bp.route("/industry_level_logo/<level>")
def industry_level_logo(level):
    """
    获取行业等级logo
    :return:
    """
    logo_path = current_app.config["INDUSTRY_LEVEL_LOGO_PATH"]
    return profile_service.get_industry_level_logo(logo_path, level)


@school_profile_bp.route("/school_header_background/<school>")
# @login_required
def school_header_background(school):
    """
    展示学校画像中最上方的图片
    """
    school_path = current_app.config["SCHOOL_HEADER_PATH"]
    return profile_service.get_school_header_background(school, path=school_path)


@school_profile_bp.route("/school_profile_cover")
# @login_required
def school_profile_cover():
    """
    展示高校画像封面
    """
    school_path = current_app.config["SCHOOL_HEADER_PATH"]
    return profile_service.get_school_profile_cover_background(school_path)


@school_profile_bp.route("/get_institution_patent_num")
# @login_required
def get_institution_patent_num():
    """
    获取某一学校各学院的专利数量
    :return:
    """
    school = request.args.get("school")
    result = profile_service.get_institution_patent_num(school)
    return result


@school_profile_bp.route("/institution_profile/<school>/<institution>")
# @login_required
def institution_profile(school, institution):
    """
    展示学院内的画像，包括学院内部的社交关系 以及 学院内部的各项指标评估
    :return:
    """
    # user_id = current_user.id
    # permission = profile_service.get_school_permission_by_user(user_id, school)
    permission = "WRITE"
    return render_template("school_profile/institution.html", school=school, institution=institution, permission=permission)


@school_profile_bp.route("/get_institution_relation")
# @login_required
def get_institution_relation():
    """
    获取学院内部的社交关系
    :return:
    """
    start = time.time()
    school = request.args.get("school")
    institution = request.args.get("institution")
    result = relationService.get_institution_relation(school, institution)
    end = time.time()

    logging.warning("检索社区关系花费时间:  " + str(end-start))
    return result


@school_profile_bp.route("/get_institution_dimension_info")
# @login_required
def get_institution_dimension_info():
    """
    获取学院内部的各项指标评估
    :return:
    """
    school = request.args.get("school")
    institution = request.args.get("institution")
    result2 = profile_service.get_institution_dimension_info(school, institution)
    return result2


@school_profile_bp.route("/get_team_dimension_info")
# @login_required
def get_team_dimension_info():
    """
    获取团队的各维度信息
    :return:
    """
    team_id = request.args.get("team_id")  # team_id与教师id是对应的
    if team_id is None:
        return {"success": False}
    school = request.args.get("school")
    teacher_name = profile_service.get_teacher_name_by_id(team_id)
    result = profile_service.get_team_dimension_info(team_id, school)
    result["leader"] = teacher_name
    result["success"] = True
    return result


@school_profile_bp.route('/get_school_normalize_dimension_score')
# @login_required
def get_school_normalize_dimension_score():
    """
    获取学校归一化之后的各维度分数
    :return:
    """
    school = request.args.get("school")
    result = profile_service.get_school_normalize_dimension_score(school)
    return result


@school_profile_bp.route("/update_node_visit_status")
# @login_required
def update_node_visit_status():
    """
    更新节点的拜访状态：0未联系过、1联系过、2做过活动、3签过合同、4创业
    :return:
    """
    teacher_id = request.args.get("teacher_id")
    visit_status = request.args.get("visit_status")
    relationService.update_node_visit_status(teacher_id, visit_status)
    return {"success": True}


@school_profile_bp.route("/industry_map")
def industry_map():
    """
    展示行业地图
    :return:
    """
    return render_template("school_profile/industry_map.html")


@school_profile_bp.route("/get_school_industry")
def get_school_industry():
    """
    获取一所学校下主要的行业数量
    :return:
    """
    school = request.args.get("school")
    data = profile_service.get_school_industry(school)
    return data


@school_profile_bp.route("/industry_compare/<school>/<industry>")
def industry_compare(school, industry):
    """
    行业对比页面，
    1、 显示某高校下的行业对比饼图
    2.  显示某一行业下各高校的学院分布柱状图
    :param school:
    :param industry:
    :return:
    """
    data = profile_service.get_institution_by_industry(industry)

    return render_template("school_profile/industry_compare.html", data=data, school=school, industry=industry)


@school_profile_bp.route("/get_institution_industry_patent_num2")
# @login_required
def get_institution_industry_patent_num2():
    """
    获取某学校下 各学院中的行业对应的成果数量 以及  学院本身的成果数量， 用于生成矩形树图
    :return:
    """
    school = request.args.get("school")
    result = profile_service.get_institution_industry_patent_num2(school)
    return result


@school_profile_bp.route("/get_team_patent_project_data")
def get_team_patent_project_data():
    """
    获取某一团队下的专利数据和项目数据
    :return:
    """
    team_id = request.args.get("team_id")
    result = profile_service.get_team_patent_project_data(team_id)
    return result


@school_profile_bp.route("/get_teacher_patent_project_data")
def get_teacher_patent_project_data():
    """
    获取某一专家下的专利数据和项目数据
    :return:
    """
    teacher_id = request.args.get("teacher_id")
    result = profile_service.get_teacher_patent_project_data(teacher_id)
    return result


@school_profile_bp.route("/get_team_member_info")
def get_team_member_info():
    """
    获取某一学院下的团队以及团队中的成员信息，用于构造树图
    :return:
    """
    school = request.args.get("school")
    institution = request.args.get("institution")
    result = relationService.get_team_member_info(school, institution)
    return {"success": True, "data": result}
