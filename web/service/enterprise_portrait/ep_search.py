"""
处理有关企业专利信息的数据库获取结果的处理
"""
from web.dao.enterprise_portrait import ep_dao
from config import BERT_Params
from config import Milvus_Params
from bert_serving.client import BertClient
from milvus import Milvus, IndexType, MetricType
import math


def string_to_vector(search_content):
    """
    将搜索内容转化为bert文本向量
    :param search_content: 搜索内容
    :return:
    """
    bc = BertClient(ip = BERT_Params["ip"])
    result = search_content.strip().replace(" ", "").replace('\n', '').replace('\r', '')
    output = bc.encode([result])
    return output[0].tolist()


def search_millvus(searched_table, query_vec_list):
    """
    查询向量返回id
    :param searched_table: 需要查询的表
    :param query_vec_list: 需要查询的向量
    :return: 结果的id
    """
    # 初始化一个Milvus类，以后所有的操作都是通过milvus来的
    milvus = Milvus()
    # 连接到服务器，注意端口映射，要和启动docker时设置的端口一致
    s = milvus.connect(host=Milvus_Params['host'], port=Milvus_Params['port'])
    # 进行查询, 注意这里的参数nprobe和建立索引时的参数nlist 会因为索引类型不同而影响到查询性能和查询准确率
    # 对于 FLAT类型索引，两个参数对结果和速度没有影响
    try:
        status, results = milvus.search(table_name=searched_table, query_records=query_vec_list, top_k=20, nprobe=16)
        # 断开连接
        milvus.disconnect()
        result = []
        for i in results[0]:
            result.append(str(i)[str(i).index("=") + 1:str(i).index(",")])
        return result
    except:
        return False


def get_en_info_by_id(ep_id):
    """
    根据企业名
    :param searched_patent:
    :return:企业信息
    """
    result = ep_dao.get_en_info_by_id(ep_id)
    return result


def search_ep(search_content):
    """
    根据搜索内容搜索企业
    :param search_content:搜索内容
    :return:
    """
    # 将搜索内容转化成文本向量
    search_content_vector = string_to_vector(search_content)
    # 搜索相关专利的id
    patent_id_list = search_millvus("patent_table", [eval(str(search_content_vector))])
    # 获取企业信息
    ep_base_info = ep_dao.get_ep_ip_by_pa_id(set(patent_id_list))
    # 获取相关的工程师
    engineer_info = ep_dao.get_engineer_by_pa_id(set(patent_id_list))
    # 获取搜索结果中专利对应的企业
    ep_id_list = ep_dao.get_ep_id_by_pa_id(set(patent_id_list))
    for i in ep_base_info:
        i['engineers'] = []
        i['pa_id'] = []
        i['registered_capital'] = int(float(i['registered_capital']))
        for j in engineer_info:
            if j['ep_id'] == i['id'] and j['engineer_name'] not in i['engineers']:
                i['engineers'].append(j['engineer_name'])
        for x in ep_id_list:
            if i['id'] == x['ep_id']:
                i['pa_id'].append(x['pa_id'])
        i['engineers'] = '、'.join(i['engineers'])
        i['engineers'] = i['engineers'].replace(",","、")
    return ep_base_info, set(patent_id_list)


def sort_ep(ep_list, vs, pa_id_list):
    """
    对选择的企业进行排序
    :param ep_list: 企业id列表
    :param vs: 排序类型
    :return:
    """
    # 获取企业信息
    if vs == "0":
        ep_base_info = ep_dao.sort_ep_by_similarity(set(ep_list))
    elif vs == "1":
        ep_base_info = ep_dao.sort_ep_by_date(set(ep_list))
    elif vs == "2":
        ep_base_info = ep_dao.sort_ep_by_date_desc(set(ep_list))
    elif vs == "3":
        ep_base_info = ep_dao.sort_ep_by_money(set(ep_list))
    else:
        ep_base_info = ep_dao.sort_ep_by_money_desc(set(ep_list))
    # 获取相关的工程师
    engineer_info = ep_dao.get_engineer_by_pa_id(set(pa_id_list))
    # 获取搜索结果中专利对应的企业
    ep_id_list = ep_dao.get_ep_id_by_pa_id(set(pa_id_list))
    for i in ep_base_info:
        i['engineers'] = []
        i['pa_id'] = []
        i['registered_capital'] = int(float(i['registered_capital']))
        for j in engineer_info:
            if j['ep_id'] == i['id'] and j['engineer_name'] not in i['engineers']:
                i['engineers'].append(j['engineer_name'])
        for x in ep_id_list:
            if i['id'] == x['ep_id']:
                i['pa_id'].append(x['pa_id'])
        i['engineers'] = '、'.join(i['engineers'])
        i['engineers'] = i['engineers'].replace(",", "、")
    return ep_base_info


def get_pa_info_by_pa_id(pa_list):
    """
    根据专利id获取专利信息
    :param pa_list: 专利id
    :return:
    """
    return ep_dao.get_pa_info_by_pa_id(pa_list)


def get_ip_count_type(ep_id):
    """
    获取企业的专利、实用新型、软件著作权数量
    :param ep_id:
    :return:
    """
    return ep_dao.get_ip_count_type(ep_id)


def get_engineer_net(ep_id):
    """
    根据ep_id获取企业里的工程师的网络
    :param ep_id:企业id
    :return:
    """
    data = []
    engineer_count = ep_dao.get_engineer_with_count(ep_id)
    max = engineer_count[0]['patent_num']
    min = engineer_count[len(engineer_count)-1]['patent_num']
    engineer_id_list = []
    engineer_list = []
    for i in engineer_count:
        engineer_id_list.append(i['id'])
        engineer_list.append(i['engineer_name'])
        temp = {
            "name": i['engineer_name'],
            "des": "知识产权:"+str(i["patent_num"]),
            "symbolSize": change_symbolSize(max, min, i['patent_num']),
            "id": i['id']
        }
        data.append(temp)
    links_temp = []
    for i in engineer_list:
        for j in engineer_list:
            temp = {
                "source": i,
                "target": j,
                "name": 0,
            }
            temp_converse = {
                "source": j,
                "target": i,
                "name": 0
            }
            if i != j and temp not in links_temp and temp_converse not in links_temp:
                links_temp.append(temp)
    engineer_relation = ep_dao.get_engineer_relation(set(engineer_id_list))
    for i in links_temp:
        for j in engineer_relation:
            for x in engineer_relation:
                if j['engineer_name'] == i['source'] and x['engineer_name'] == i['target'] and j['pa_id'] == x['pa_id']:
                    i['name'] = i['name'] + 1
    links = []
    for i in links_temp:
        if i['name'] != 0:
            links.append(i)
    for i in links:
        i['name'] = ""
    return data, links


def get_engineer_net_center(ep_id):
    """
    根据ep_id获取企业里专利数量最大的个人中心网络
    :param ep_id:企业id
    :return:
    """
    engineer_id = ep_dao.get_max_patent_engineer_id(ep_id)['id']
    net_data = ep_dao.get_engineer_net_center(engineer_id)
    engineer_count = []
    data = []
    links = []
    # 对专利数量第一人是否存在合作网络的处理
    if len(net_data) > 0:
        engineer_count.append(net_data[0]['e.patent'])
        for i in net_data:
            engineer_count.append(i['e2.patent'])
        engineer_count.sort(reverse=True)
        max = engineer_count[0]
        min = engineer_count[len(engineer_count) - 1]
        data.append(
            {
                "name": net_data[0]['e.name'],
                "des": "知识产权:" + str(i['e.patent']),
                "symbolSize": change_symbolSize(max, min, i['e.patent']),
                "category": i['e.visit_status'],
                "value": i['e.id'],
            }
        )
        for i in net_data:
            data_temp = {
                "name": i['e2.name'],
                "des": "知识产权:"+str(i['e2.patent']),
                "symbolSize": change_symbolSize(max, min, i['e2.patent']),
                "category": i['e2.visit_status'],
                "value": i['e2.id'],
            }
            link_temp = {
                "source": i['e.name'],
                "target": i['e2.name'],
                "name": ""
            }
            data.append(data_temp)
            links.append(link_temp)
    else:
        net_data = ep_dao.get_engineer_node(ep_id)
        for i in net_data:
            engineer_count.append(i['patent'])
        engineer_count.sort(reverse=True)
        max = engineer_count[0]
        min = engineer_count[len(engineer_count) - 1]
        for i in net_data:
            data.append(
                {
                    "name": i['name'],
                    "des": "知识产权:" + str(i['patent']),
                    "symbolSize": change_symbolSize(max, min, i['patent']),
                    "category": i['visit_status'],
                    "value": i['id'],
                }
            )
    return data, links


def change_symbolSize(max, min, pa_count):
    """
    转化关系图中节点大小
    :return:
    """
    dev = (max - min) / 4
    if min <= pa_count < min + dev:
        return 30
    elif min + dev <= pa_count < min + dev*2:
        return 40
    elif min + dev*2 <= pa_count < min + dev*3:
        return 50
    else:
        return 60


def get_research_ability_info(ep_id):
    """
    获取企业的研发能力数据
    :param ep_id: 企业id
    :return:
    """
    # 获取工程师数量
    engineer_count = ep_dao.get_engineer_count(ep_id)['count']
    engineer_count_score = int(math.log(engineer_count+1))*10 + 30
    # 获取知识产权数量
    ip_count = ep_dao.get_ip_count(ep_id)['num']
    ep_count_score = int(math.log(ip_count+1))*10 + 10
    # 获取企业的注册资金
    register_money = ep_dao.get_register_money(ep_id)['registered_capital']
    registered_capital_score = int(math.log(float(register_money),10))*10 + 40
    # 获取是否是工程技术研究中心、高企
    is_en_tech_rese_center = ep_dao.get_is_en_tech_rese_center(ep_id)['count']
    is_en_tech_rese_center_score = 30 + is_en_tech_rese_center * 10
    result = [registered_capital_score, engineer_count_score, is_en_tech_rese_center_score, ep_count_score]
    return result


def get_ep_info(ep_list):
    """
    获取企业详细信息
    :param ep_list:企业列表
    :return:
    """
    temp = ep_dao.get_ep_info(ep_list)
    result = []
    for item in temp:
        temp_ep = []
        for keys, value in item.items():
            if keys not in ["id", "is_high_tech_ep", "is_store_ep", "is_small_tech_ep", "lng", "lat", "patent_count",
                            "practical_count", "software_count", "ep_contacts", "town"]:
                temp_ep.append(value)
        result.append(temp_ep)
    return result


def get_pa_info(pa_list):
    """
    根据专利id获取专利信息，导出数据
    :param pa_list: 专利id列表
    :return:
    """
    temp = ep_dao.get_pa_info(pa_list)
    result = []
    for item in temp:
        temp_ep = []
        for keys, value in item.items():
            if keys not in ["pa_id", "ep_id", "ep_name", "pa_type"]:
                temp_ep.append(value)
        result.append(temp_ep)
    return result


def get_history(user_id):
    """
    获取用户搜索历史
    :param user_id: 用户id
    :return:
    """
    return ep_dao.get_history(user_id)


def delete_history(history_id):
    """
    删除用户历史记录
    :param history_id: 历史id
    :return:
    """
    return ep_dao.delete_history(history_id)


def search_history(search_content, user_id):
    """
    查找历史记录
    :param search_content: 检索内容
    :param user_id: 用户id
    :return:
    """
    return ep_dao.search_history(search_content, user_id)


def update_history(history_id):
    """
    删除用户历史记录
    :param history_id: 历史id
    :return:
    """
    return ep_dao.update_history(history_id)


def insert_history(user_id, search_content):
    """
    删除用户历史记录
    :param history_id: 历史id
    :return:
    """
    return ep_dao.insert_history(user_id, search_content)


def get_all_industry():
    """
    获取所有企业的行业
    :return:
    """
    result = ep_dao.get_all_industry()
    industry_info = {}
    for i in result:
        try:
            if i['industry'] is not None and "和" in i['industry']:
                for j in i['industry'].split("和"):
                    if j in industry_info:
                        industry_info[j] = industry_info.get(j) + 1;
                    else:
                        industry_info[j] = 1
            else:
                if i['industry'] in industry_info:
                    industry_info[i['industry']] = industry_info.get(i['industry']) + 1;
                else:
                    industry_info[i['industry']] = 1
        except:
            pass
    dict = sorted(industry_info.items(), key=lambda x: x[1], reverse=True)
    industry_list = []
    industry_count = []
    for i in dict:
        industry_list.append(i[0])
        industry_count.append(i[1])

    return industry_list, industry_count


def get_patent_by_first_ipc():
    """
    获取所有大类ipc的所有专利数量
    :param ipc_id:
    :return:
    """
    all_first_ipc = ep_dao.get_patent_by_first_ipc()
    ipc_list = []
    ipc_count = []
    for i in all_first_ipc:
        ipc_list.append(i['ipc_root'] + ":" + i['ipc_title'])
        ipc_count.append(i['count'])
    return ipc_list, ipc_count



def get_patent_by_second_ipc():
    """
    获取所有中类ipc的所有专利数量
    :param ipc_id:
    :return:
    """
    all_first_ipc = ep_dao.get_patent_by_second_ipc()
    ipc_list = []
    ipc_count = []
    for i in all_first_ipc[0:30]:
        ipc_list.append(i['ipc_class'] + ":" + i['ipc_title'])
        ipc_count.append(i['count'])
    return ipc_list, ipc_count


def get_patent_by_third_ipc():
    """
    获取所有小类ipc的所有专利数量
    :param ipc_id:
    :return:
    """
    all_first_ipc = ep_dao.get_patent_by_third_ipc()
    ipc_list = []
    ipc_count = []
    for i in all_first_ipc[0:30]:
        ipc_list.append(i['ipc_class_sm'] + ":" + i['ipc_title'])
        ipc_count.append(i['count'])
    return ipc_list, ipc_count


def get_en_info_by_name_dim(ep_name):
    """
    根据企业名获取企业列表，模糊查询
    :param ep_name: 企业名
    :return: 企业信息
    """
    return ep_dao.get_en_info_by_name_dim(ep_name)


def update_engineer_visited_status(engineer_id, visited_status):
    """
    更新工程师访问状态
    :param engineer_id:工程师id
    :param visited_status:访问状态
    :return:
    """
    return ep_dao.update_engineer_visited_status(engineer_id, visited_status)


def get_role_with_ep_portrait(user_id):
    """
    获取当前用户对于企业画像的权限
    :param user_id: 用户
    :return:
    """
    temp = ep_dao.get_role_with_ep_portrait(user_id)
    result = {}
    result['ep_portrait_write'] = 0
    result['ep_portrait_read'] = 0
    if temp is not None:
        for i in temp:
            if i['role_id'] == 60:
                result['ep_portrait_write'] = 1
            if i['role_id'] == 61:
                result['ep_portrait_read'] = 1
    return result
