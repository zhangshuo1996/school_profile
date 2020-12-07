import sys
import pandas as pd
from io import BytesIO
from urllib.parse import quote

from web.dao.patent_map import network_dao
from web.utils import min_max
from web.models import CoclassificationNetwork, District


def get_top_communities(category, unit_name, limit=20):
    network = CoclassificationNetwork.get_network(category, unit_name)
    if network is None:
        return
    data = {}
    # 限制返回数量
    communities, class_set, count = {}, set(), 0
    for class_, datum in network.communities.items():
        communities[class_] = datum
        class_set.add(class_)
        count += 1
        if count >= limit:
            break
    data['community'] = communities
    # 过滤节点
    nodes, node_set = [], set()
    for node in network.nodes:
        if node['class'] in class_set:
            nodes.append(node)
            node_set.add(node['name'])
    data['nodes'] = nodes
    # 过滤边
    links = []
    for link in network.links:
        if link['source'] in node_set and link['target'] in node_set:
            links.append(link)
    data['links'] = links
    return data


def get_recommend_unites(category, unit_name, class_list):
    # 先获取“自己”的IPC群组
    communities = _get_communities_from_json(category, unit_name, class_list)
    opposed_category = get_opposed_category(category)
    # 获取推荐的单位
    industry_codes = list(communities.keys())
    data = network_dao.get_recommended_unites_by_industry_codes(opposed_category, industry_codes)
    # {名称：索引} 便于定位数据
    mapping = {}
    # 排序推荐单位、雷达图使用的indicator
    results, indicator, self_data = [], [None] * len(industry_codes), {'name': unit_name, 'value': [0] * len(industry_codes)}
    unites, last_code, min_count, max_count = [], None, sys.maxsize, 0
    for idx, datum in enumerate(data):
        if (last_code is None or last_code == datum['industry_code']) or idx == len(data)-1:
            unites.append(datum)
            last_code = datum['industry_code']
            min_count, max_count = min_max(datum['patent_count'], min_count, max_count)
        else:
            # 填充self_data
            index = industry_codes.index(last_code)
            community = communities[last_code]
            self_data['value'][index] = community['patent_count']
            # 确定最大值和最小值
            min_count, max_count = min_max(community['patent_count'], min_count, max_count)
            indicator[index] = {'name': community['title'], 'max': max_count}
            for unit in unites:
                name, count = unit['name'], unit['patent_count']
                if name not in mapping:
                    results.append({'id': unit['unit_id'],'name': name,
                                    'similarity': 0.0, 'value': [0] * len(industry_codes)})
                    mapping[name] = len(results) - 1
                # 计算相似度 最大最小归一化
                result = results[mapping[name]]
                result['similarity'] += (count - min_count) / (max_count - min_count)
                result['value'][index] = count
            # 清除
            unites.clear()
            last_code = None
    # 通过判别self_data中0的位置，来填充数据
    for idx, value in enumerate(self_data['value']):
        if value != 0:
            continue
        community = communities[industry_codes[idx]]
        count = community['patent_count']
        indicator[idx] = {'name': community['title'], 'max': count}
        self_data['value'][idx] = count
    # 获取高校对应的学院
    school_institutions = network_dao.get_institutions_by_industry_codes(industry_codes, 1000)
    # 保留两位小数
    for result in results:
        result['similarity'] = round(result['similarity'], 2)
        institutions = []
        if result['id'] in school_institutions:
            institutions = school_institutions[result['id']]
        result['institution'] = institutions[:2]
    results = sorted(results, key=lambda x: x['similarity'], reverse=True)
    return results, indicator, self_data


def get_exported_recommend_file(category, unit_name, class_list):
    """
    获取推荐名单，并返回文件名称和BytesIO
    :param category:
    :param unit_name:
    :param class_list:
    :return:
    """
    # 获取推荐数据
    results, indicator, self_data = get_recommend_unites(category, unit_name, class_list)
    # 对result再处理，删除id institution变为str
    data = []
    for result in results:
        del result['id']
        del result['value']
        institution = '; '.join(result['institution'])
        result['institution'] = institution
        data.append(result)
    out = BytesIO()
    writer = pd.ExcelWriter(out)
    df = pd.DataFrame(data)
    # 更改列的顺序和名称
    order = ['name', 'institution', 'similarity']
    df = df[order]
    columns = {'name': '名称', 'institution': '学院', 'similarity': '契合度'}
    df.rename(columns=columns, inplace=True)
    df.to_excel(excel_writer=writer, sheet_name='Sheet', index=True)
    # 更改宽度
    worksheet = writer.sheets['Sheet']  # pull worksheet object
    for idx, col in enumerate(df):  # loop through all columns
        series = df[col]
        max_len = max((
            series.astype(str).map(len).max()*2,  # len of largest item
            len(str(series.name))*2  # len of column name/header
        )) + 1  # adding a little extra space
        worksheet.column_dimensions[chr(ord('A') + idx+1)].width = max_len  # set column width
    # 保存
    writer.save()
    out.seek(0)
    # 生成中文文件名
    if category == 'school':
        filename = quote('区县推荐.xlsx')
    else:
        filename = quote('高校推荐.xlsx')
    return filename, out


def _get_communities_from_json(category, unit_name, class_list):
    """筛选社区 一个则返回community 多个返回list[]"""
    district = District.query.filter_by(town=unit_name).first_or_404()
    network = CoclassificationNetwork.query.filter_by(unit_id=district.id, category=category).first_or_404()
    if len(class_list) == 1:
        community = network.communities[class_list[0]]
        return community
    data = {community['code']: community for class_, community in network.communities.items() if class_ in class_list}
    return data


def get_opposed_category(category):
    """
    根据类别，获取另外的类别 比如school，返回district
    :param category:
    :return:
    """
    if category == 'school':
        return 'district'
    elif category == 'district':
        return 'school'
