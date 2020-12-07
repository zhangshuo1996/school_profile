"""
@author: xiaoniu
@desc: 共分类网络相关路由
"""
from flask_login import login_required
from flask import Blueprint, render_template, jsonify, request, flash, send_file

from web.utils.url import redirect_back
from web.forms.patent_map import GraphForm
from web.service.patent_map import network_service
from web.models import CoclassificationNetwork, District


patent_network_bp = Blueprint('patent_network', __name__)


@patent_network_bp.route('/show_unit_communities')
@login_required
def show_unit_communities():
    """展示某个单位的共分类网络"""
    # TODO: 类型和名称
    category = 'district'
    unit_name = '开发区'
    return render_template('patent_map/show_graph.html', category=category, unit_name=unit_name)


@patent_network_bp.route('/recommend_unites')
@login_required
def recommend_unites():
    """推荐单位 html"""
    # TODO: 类型和名称
    category = 'district'
    unit_name = '开发区'
    # 从数据库获取网络数据
    district = District.query.filter_by(town=unit_name).first_or_404()
    network = CoclassificationNetwork.query.filter_by(unit_id=district.id, category=category).first_or_404()
    return render_template('patent_map/recommend.html', unit_name=unit_name, category=category,
                           communities=network.communities)


@patent_network_bp.route('/ajax/get_ipc_communities')
def get_ipc_communities():
    """获取某单位的所有IPC群组数据"""
    # TODO: 类型和名称
    category = 'district'
    unit_name = '开发区'
    # 从数据库获取网络数据
    data = network_service.get_top_communities(category, unit_name)
    if data is None:
        return jsonify({'error': True, 'msg': '数据获取失败，请稍后刷新重试'})
    # 返回共分类网络数据
    return jsonify({'error': False, 'data': data})


@patent_network_bp.route('/ajax/get_recommend_unites')
def get_recommend_unites():
    """根据选择的行业类别，获取实力比较强的高校/区县"""
    form = GraphForm(request.args)
    if form.validate():
        unit_name, category = form.unit_name.data, form.category.data
        class_list = request.args.getlist('class_list[]')
        if len(class_list) < 3:
            return jsonify({'error': True, 'msg': '请最少选择三个行业'})
        # 处理
        results, indicator, self_data = network_service.get_recommend_unites(category, unit_name, class_list)
        return jsonify({'error': False, 'data': results, 'indicator': indicator, 'self_data': self_data})
    return jsonify({'error': True, 'msg': 'error'})


@patent_network_bp.route('/ajax/download_recommend_unites')
def download_recommend_unites():
    """下载推荐的单位excel"""
    form = GraphForm(request.args)
    if form.validate():
        unit_name, category = form.unit_name.data, form.category.data
        class_list = request.args.getlist('class_list[]')
        if len(class_list) < 3:
            flash('请至少选择三个行业', 'danger')
            return redirect_back()
        # 待导出数据
        filename, out = network_service.get_exported_recommend_file(category, unit_name, class_list)
        response = send_file(out, as_attachment=True, attachment_filename=filename)
        response.headers['Content-Disposition'] += "; filename*=utf-8''{}".format(filename)
        response.headers["Content-type"] = "application/x-xlsx"
        return response
    flash('导出失败，请稍后重试', 'danger')
    return redirect_back()
