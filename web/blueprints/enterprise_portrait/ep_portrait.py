"""
@author: df
@desc: 企业画像路由
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import current_user, login_required
from web.service.enterprise_portrait import ep_search as ep_service
from web.service.enterprise_portrait import utils as utils_service

enterprise_portrait_bp = Blueprint('enterprise_portrait', __name__)


@enterprise_portrait_bp.route('/')
@login_required
def index():
    user_id = current_user.id
    role_with_portrait = ep_service.get_role_with_ep_portrait(user_id)
    if role_with_portrait['ep_portrait_write'] == 0 and role_with_portrait['ep_portrait_read'] == 0:
        flash("您没有权限, 请联系管理员分配权限", "danger")
        return redirect(request.referrer)
    history = ep_service.get_history(user_id)
    return render_template("enterprise_portrait/index.html", history=history)


@enterprise_portrait_bp.route('/search_ep', methods=["GET", "POST"])
@login_required
def search_ep():
    """
    检索企业
    :return:
    """
    user_id = current_user.id
    search_content = request.form.get("enterprise")
    search_style = request.values.get("options_radio")
    if search_style == "1":
        ep_info = ep_service.get_en_info_by_name_dim(search_content)
        ep_id_list = ""
        for i in ep_info:
            ep_id_list = ep_id_list + "," + str(i['id'])
        return render_template("enterprise_portrait/ep_info_name.html", ep_info=ep_info, search_content=search_content,
                               ep_id_list=ep_id_list)
    if search_style == "2":
        ep_info, patent_id_list = ep_service.search_ep(search_content)
        ep_id_list = ""
        pa_id_list = ""
        for i in ep_info:
            ep_id_list = ep_id_list + "," + str(i['id'])
        for i in patent_id_list:
            pa_id_list = pa_id_list + "," + str(i)
        # 插入历史记录
        history_count = ep_service.search_history(search_content, user_id)
        if len(history_count) > 0:
            ep_service.update_history(history_count[0]['id'])
        else:
            ep_service.insert_history(user_id, search_content)
        return render_template("enterprise_portrait/ep_info.html", ep_info=ep_info, ep_id_list=ep_id_list
                               , pa_id_list=pa_id_list)


@enterprise_portrait_bp.route('/search_ep_history/<int:history_id>/<search_content>')
@login_required
def search_ep_history(history_id, search_content):
    """
    检索企业
    :return:
    """
    ep_info, patent_id_list = ep_service.search_ep(search_content)
    ep_id_list = ""
    pa_id_list = ""
    for i in ep_info:
        ep_id_list = ep_id_list + "," + str(i['id'])
    for i in patent_id_list:
        pa_id_list = pa_id_list + "," + str(i)
    ep_service.update_history(history_id)
    return render_template("enterprise_portrait/ep_info.html", ep_info=ep_info, ep_id_list=ep_id_list
                           , pa_id_list=pa_id_list)


@enterprise_portrait_bp.route('/get_ep_detail/<int:ep_id>/<ep_name>/<pa_id>')
@login_required
def get_ep_detail(ep_id, ep_name, pa_id):
    """
    获取企业详细数据
    :param ep_id: 企业id
    :return:
    """
    ep_info = ep_service.get_en_info_by_id(ep_id)
    ip_count = ep_service.get_ip_count_type(ep_id)
    if isinstance(eval(pa_id), int):
        temp = []
        temp.enterprise_portrait_bpend(pa_id)
        temp = str(temp)
        pa_info = ep_service.get_pa_info_by_pa_id(set(eval(temp)))
    else:
        pa_info = ep_service.get_pa_info_by_pa_id(set(eval(pa_id)))
    pa_id_list = []
    for i in pa_info:
        pa_id_list.append(i["pa_id"])
    user_id = current_user.id
    role_with_portrait = ep_service.get_role_with_ep_portrait(user_id)['ep_portrait_write']
    return render_template("enterprise_portrait/ep_detail.html", ep_info=ep_info, ep_name=ep_name, pa_info=pa_info, ip_count=ip_count,
                           pa_id_list=pa_id_list, role_with_portrait=role_with_portrait)


@enterprise_portrait_bp.route('/get_ep_detail_name/<int:ep_id>/<ep_name>')
@login_required
def get_ep_detail_name(ep_id, ep_name):
    """
    获取企业详细数据
    :param ep_id: 企业id
    :param ep_name: 企业名
    :return:
    """
    ep_info = ep_service.get_en_info_by_id(ep_id)
    ip_count = ep_service.get_ip_count_type(ep_id)
    user_id = current_user.id
    role_with_portrait = ep_service.get_role_with_ep_portrait(user_id)['ep_portrait_write']
    return render_template("enterprise_portrait/ep_detail_name.html", ep_info=ep_info, ep_name=ep_name, ip_count=ip_count,
                                                role_with_portrait=role_with_portrait)


@enterprise_portrait_bp.route('/get_engineer_count', methods=["GET"])
@login_required
def get_engineer_count():
    """
    获取企业中的工程师的网络
    :return:
    """
    ep_id = request.args.get("ep_id")
    engineer_nodes, links = ep_service.get_engineer_net_center(ep_id)
    if len(engineer_nodes) == 0:
        engineer_nodes, links = ep_service.get_engineer_net(ep_id)
    research_score = ep_service.get_research_ability_info(ep_id)
    if engineer_nodes or research_score:
        return jsonify({"status": True, "engineer_nodes": engineer_nodes, "links": links, \
                        "research_score": research_score})
    else:
        return jsonify({"status": False})


@enterprise_portrait_bp.route("/sort_ep", methods=["GET"])
@login_required
def sort_ep():
    """
    企业排序
    :return:
    """
    vs = request.args.get("vs")
    ep_id_list = request.args.get("ep_id_list")
    patent_id_list = request.args.get("pa_id_list")
    ep_list = set(str(ep_id_list).lstrip(",").split(","))
    pa_id_list = set(str(patent_id_list).lstrip(",").split(","))
    ep_info = ep_service.sort_ep(ep_list, vs, pa_id_list)
    if ep_id_list:
        return jsonify({"status": True, "ep_info": ep_info})
    else:
        return jsonify({"status": False})


@enterprise_portrait_bp.route("/download_ep_info/<ep_id_list>")
@login_required
def download_ep_info(ep_id_list):
    """
    导出企业数据
    :param ep_id_list:
    :return:
    """
    ep_list = set(str(ep_id_list).lstrip(",").split(","))
    ep_info = ep_service.get_ep_info(ep_list)
    filename = utils_service.write_ep_excel_file(ep_info, ep_info[0][1])
    return redirect(url_for('enterprise_portrait.download', filename=filename))


@enterprise_portrait_bp.route("/download_pa_info/<pa_id_list>")
@login_required
def download_pa_info(pa_id_list):
    """
    导出专利数据
    :param pa_id_list:
    :return:
    """
    pa_info = ep_service.get_pa_info(set(eval(pa_id_list)))
    filename = utils_service.write_ep_excel_file(pa_info, pa_info[0][1], type=2)
    return redirect(url_for('enterprise_portrait.download', filename=filename))


@enterprise_portrait_bp.route("/download/<filename>")
@login_required
def download(filename):
    """
    下载文件
    :param filename:
    :return:
    """
    return utils_service.download_by_path(filename)


@enterprise_portrait_bp.route("/delete_history", methods=["GET"])
@login_required
def delete_history():
    history_id = request.args.get("history_id")
    ep_service.delete_history(history_id)
    return jsonify({"status": True})


@enterprise_portrait_bp.route('/get_industry_statistic')
@login_required
def get_industry_statistic():
    return render_template("enterprise_portrait/statistic.html")


@enterprise_portrait_bp.route('/patent_info')
@login_required
def patent_info():
    return render_template("enterprise_portrait/patent_info.html")


@enterprise_portrait_bp.route('/get_industry_info', methods=["GET"])
@login_required
def get_industry_info():
    """
    获取企业的行业分布情况
    :return:
    """
    industry_list, industry_count = ep_service.get_all_industry()
    if industry_list:
        return jsonify({"status": True, "industry_list": industry_list, "industry_count": industry_count})
    else:
        return jsonify({"status": False})


@enterprise_portrait_bp.route('/get_patent_by_first_ipc', methods=["GET"])
@login_required
def get_patent_by_first_ipc():
    """
    获取所有大类ipc的所有专利数量
    :param ipc_id:
    :return:
    """
    ipc_list, ipc_count = ep_service.get_patent_by_first_ipc()
    if ipc_list:
        return jsonify({"status": True, "ipc_list": ipc_list, "ipc_count": ipc_count})
    else:
        return jsonify({"status": False})


@enterprise_portrait_bp.route('/get_patent_by_second_ipc', methods=["GET"])
@login_required
def get_patent_by_second_ipc():
    """
    获取所有中类ipc的所有专利数量
    :param ipc_id:
    :return:
    """
    ipc_list, ipc_count = ep_service.get_patent_by_second_ipc()
    if ipc_list:
        return jsonify({"status": True, "ipc_list": ipc_list, "ipc_count": ipc_count})
    else:
        return jsonify({"status": False})


@enterprise_portrait_bp.route('/get_patent_by_third_ipc', methods=["GET"])
@login_required
def get_patent_by_third_ipc():
    """
    获取所有小类ipc的所有专利数量
    :param ipc_id:
    :return:
    """
    ipc_list, ipc_count = ep_service.get_patent_by_third_ipc()
    if ipc_list:
        return jsonify({"status": True, "ipc_list": ipc_list, "ipc_count": ipc_count})
    else:
        return jsonify({"status": False})


@enterprise_portrait_bp.route('/update_engineer_visited_status', methods=["GET"])
@login_required
def update_engineer_visited_status():
    """
    更新工程师访问状态
    :param engineer_id:工程师id
    :param visited_status:访问状态
    :return:
    """
    engineer_id = request.args.get("engineer_id")
    visited_status = request.args.get("visited_status")
    ep_service.update_engineer_visited_status(engineer_id, visited_status)
    return jsonify({"status": True})
