# 教师表 clean_inventor,honor(中国科学院院士、杰出青年、长江学者（特聘教授）、中国工程院院士、长江学者（青年学者），
# 长江学者（讲座教授）
# 教师表和图数据库的教师可以通过id对应

# TODO
# 1. 推荐和排序
# 行业排名
# 教师推荐重做
# 要不要存为json数据
# 2. 活动相关
# 谁来上传数据
# 3. 一行强制容纳10个行业(丑）

import io
import pandas as pd
from urllib.parse import quote
from flask import Blueprint, render_template, request, flash, make_response
import json
from flask_login import login_required, current_user

from web.models.industry_info import IndustryInfo
from web.models.teacher_for_engineer_community import TeacherForEngineerCommunity
from web.models.data_mining.teacher_for_industry import TeacherForIndustry
from web.utils.url import redirect_back
from web.service import engineer_community as engineer_community_service


# url_prefix='/engineer_community'
engineer_community_bp = Blueprint('engineer_community', __name__)


@engineer_community_bp.route('/')
@engineer_community_bp.route('/index')
@login_required
def index():
    """
    显示该区域前五个行业的工程师社区
    """
    breadcrumbs = [{'name': '昆山市开发区工程师社区', 'link': "engineer_community.index"}]
    # info = [{"name": "行业1"}, {"name": "行业2"}, {"name": "行业3"}, {"name": "行业4"}, {"name": "行业5"},
    #         {"name": "行业6"}, {"name": "行业7"}, {"name": "行业8"}, {"name": "行业9"}, {"name": "行业10"}]
    info = IndustryInfo.query.limit(10).all()
    info1 = info[:5]
    info2 = info[5:]
    return render_template('engineer_community/index.html', info1=info1, info2=info2, breadcrumbs=breadcrumbs)


@engineer_community_bp.route('/get_industry_graph_data')
@login_required
def get_industry_graph_data():
    industry = request.args.get("industry")
    # print(industry)
    result = engineer_community_service.get_cooperate_rel_by_community_id_list(industry, current_user.id, current_user.name)
    return result


@engineer_community_bp.route('/search_community')
@login_required
def search_community():
    search_content = request.args.get("enterprise")
    breadcrumbs = [{'name': '昆山市开发区工程师社区'}]
    community_info = [{'engineers': '熊勇军、李进龙、沈喜荣、杨晶、胡祖军'},
                      {'engineers': '熊勇军、李进龙、沈喜荣、杨晶、胡祖军'},
                      {'engineers': '熊勇军、李进龙、沈喜荣、杨晶、胡祖军'},
                      {'engineers': '熊勇军、李进龙、沈喜荣、杨晶、胡祖军'}]
    return render_template("engineer_community/community_info.html",
                           search_content=search_content, community_info=community_info, breadcrumbs=breadcrumbs)


@engineer_community_bp.route('/get_teacher_info')
@login_required
def get_teacher_info():
    community_id = request.args.get('community_id')
    teacher_info = TeacherForEngineerCommunity.query.filter_by(community_id=community_id).all()
    results = []
    for info in teacher_info:
        if info.institution is not None and info.institution != "None":
            results.append({'teacher_id': info.teacher_id,
                        'patent_num': info.patent_num, 'title': info.title, 'teacher_name': info.teacher_name,
                        'institution': info.institution, 'school': info.school})
        else:
            results.append({'teacher_id': info.teacher_id,
                        'patent_num': info.patent_num, 'title': info.title, 'teacher_name': info.teacher_name,
                        'institution': "", 'school': info.school})
    return json.dumps(results)


@engineer_community_bp.route('/get_teacher_info_for_industry')
@login_required
def get_teacher_info_for_industry():
    industry = request.args.get('industry')
    teacher_info = TeacherForIndustry.query.filter_by(industry_name=industry).all()
    results = []
    for info in teacher_info:
        if info.institution is not None and info.institution != "None":
            results.append({'teacher_id': info.teacher_id,
                        'patent_num': info.patent_num, 'title': info.title, 'teacher_name': info.teacher_name,
                        'institution': info.institution, 'school': info.school})
        else:
            results.append({'teacher_id': info.teacher_id,
                        'patent_num': info.patent_num, 'title': info.title, 'teacher_name': info.teacher_name,
                        'institution': "", 'school': info.school})
    return json.dumps(results)


@engineer_community_bp.route('/download_namelist')
@login_required
def download_namelist():
    community_id = request.args.get('community_id')
    print(community_id)
    items = engineer_community_service.get_namelist(community_id)
    if len(items) == 0:
        flash("暂无数据", "info")
        return redirect_back()
    if len(items) > 15:
        items = items[:15]
    data = pd.DataFrame(items)
    out = io.BytesIO()
    writer = pd.ExcelWriter(out, engine='xlsxwriter')
    data.to_excel(excel_writer=writer, index=False, sheet_name='名单')
    writer.save()
    writer.close()

    response = make_response(out.getvalue())
    filename = "工程师名单.xlsx"
    response.headers['Content-Disposition'] = 'attachment;filename={0};filename*={0}'.format(quote(filename))
    response.headers["Content-type"] = "application/x-xls"

    return response



