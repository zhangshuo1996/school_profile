from flask import Blueprint, current_app, flash
from flask import render_template, request, send_from_directory
from flask_login import login_required, current_user
from web.service.school_profile.PatentSearchService import PatentSearchService
from web.service.school_profile import RelationshipService as relationService
from web.service.school_profile import profile as profile_service
from web.utils.url import redirect_back
import logging
from web.utils import make_pdf
import time

school_search_bp = Blueprint("school_search", __name__)


@school_search_bp.route('/')
# @login_required
def index():
    return render_template('base.html')


@school_search_bp.route("/test")
# @login_required
def test():
    return render_template("school_profile/search_outcome.html")


@school_search_bp.route('/hunt', methods=["GET", "POST"])
# @login_required
def hunt():
    """
    搜索路由
    获取要搜索的类型以及输入的内容， 根据搜索类型调用相应的SearchService
    :return:
    """
    input_key = request.form.get("input_key")
    # school = request.form.get("school")
    school = ""  # 暂时不使用school这个参数
    # user_id = current_user.id
    # permission = profile_service.get_school_permission_by_user(user_id, school)
    permission = "WRITE"
    # if permission == "READ":
    #     flash("您沒有搜索权限, 请向管理员申请", "danger")
    #     return redirect_back()
    if input_key is not None:
        start = time.time()
        patent_service = PatentSearchService(input_key, school=school)  # 搜索专利服务
        # outcome_patent_dict = patent_service.construct_teacher_in_res()  # 获取相似成果对应的团队
        outcome_patent_dict = patent_service.compose_search_outcome_info()  # 获取相似成果及对应的团队信息
        current_app.outcome = outcome_patent_dict
        # outcome_id = searchService.save_this_search_text(1, input_key)  # 记录该次搜索的企业需求
        # search_history = patent_service.get_search_history()
        end = time.time()
        spend_time = end - start
        logging.warning("总的搜索时间" + str(spend_time) + "秒")
        if len(outcome_patent_dict["sorted_patent_id_list"]) == 0:
            flash("没有在该高校检索到相关成果", 'danger')
            return redirect_back()
        return render_template("school_profile/search_outcome.html", input_key=input_key, outcome_paper_list=[],
                               data=outcome_patent_dict, type="teacher", school=school, permission=permission)
    else:
        return render_template('school_profile/search.html')


@school_search_bp.route('/getTeamRelation')
# @login_required
def getTeamRelation():
    """
    获取该团队的关系数据
    :return:
    """
    start = time.time()
    school = request.args.get("school")
    team_id = request.args.get("team_id")
    institution = request.args.get("institution")
    if team_id is None:
        return {"success": False}
    result = relationService.get_cooperate_rel_by_team_id_list(school, institution, [team_id])
    teacher_name = profile_service.get_teacher_name_by_id(team_id)
    result["leader"] = teacher_name
    result["success"] = True
    end = time.time()
    logging.warning("获取该团队关系数据"+str(end-start))
    return result


@school_search_bp.route("/avatar/<filename>")
# @login_required
def avatar(filename):
    """
    寻找头像
    """
    avatar_path = current_app.config["SCHOOL_AVATAR_PATH"]
    return send_from_directory(avatar_path, filename + '.png')


@school_search_bp.route("/get_pdf", methods=["GET", "POST"])
# @login_required
def get_pdf3():
    """
    获取搜索结果中 第i个 团队对应的pdf
    :return:
    """
    page_num = request.form.get("page_num")
    outcome = current_app.outcome
    file_path = current_app.config["SCHOOL_SEARCH_DOC_PATH"]
    filename = make_pdf.generate_doc(page_num, outcome, file_path)
    return send_from_directory(file_path, filename, as_attachment=True)
