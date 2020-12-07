import json
import os
from web.settings import basedir
from web.dao.engineer_community import engineer_community as engineer_community_dao
from web.utils import Ego_net as ego_net


def get_relations(school, institution):
    """
    获取当前用户与某一学院之中的人员关系及其中的内部社区分布
    :param school: 学校名
    :param institution: 学院名
    :param agent_id: 商务自己建立的联系, [{id:xxx, name: xxx, weight: 123},{...},....]
    :return: 可供echarts直接渲染的json文件 or False
    """
    file_path = os.path.join(basedir, 'web', 'static', 'relation_data', '%s%s.txt' % (school, institution))

    # 判断该学院社区网络文件是否存在
    if not os.path.exists(file_path):
        print("%s %s 的社交网络尚未生成！" % (school, institution))
        return False
    with open(file_path, "r") as f:
        data = json.loads(f.read())
        # print(data)

        # agent_relation => [{visited: xxx, activity: xxx, id:13213},...] or []
        # agent_relation = self.get_institutions_relation_data(agent_id, school, institution)

        # relation_data = self.format_institution_relation_data(data, agent_relation)
        relation_data = format_institution_relation_data(data)
        return json.dumps(relation_data)


def format_institution_relation_data(data):
    """
    将学院关系数据简化为可发送的数据
    :param data: 预处理过的社区网络数据
    :return: 可供echarts直接渲染的json文件 or False
    """
    try:
        """
            nodes 中舍弃 code, school, insititution, centrality, class 属性, 
            添加 label,symbolSize 属性
            class 属性是指节点所属社区, 从 1 开始
        """
        teacher_id_dict = dict()
        class_id_dict = dict()

        for node in data["nodes"]:
            node['label'], node['name'] = node['name'], str(node['teacherId'])
            node['category'], node["draggable"] = node['class'], True
            node['symbolSize'] = int(node['centrality'] * 30 + 5)

            # 核心节点
            if node['teacherId'] in data["core_node"]:
                node["itemStyle"] = {
                    "normal": {
                        "borderColor": 'yellow',
                        "borderWidth": 2,
                        "shadowBlur": 10,
                        "shadowColor": 'rgba(0, 0, 0, 0.3)'
                    }
                }

                # 保存 class 的种类是为了划分社区 ==> 实现这一功能的前提是 class 值不存在断档
                # 其值为该社区核心节点 id
                class_id_dict[str(node["class"])] = node["label"]

            # 保存 teacherId => 判定商务创建的所有关系中有哪些属于当前社区;
            # 以其 class 为值是为了更方便的在隐藏非核心节点时, 将商务与其的关系累加到核心节点上
            teacher_id_dict[node['teacherId']] = node["class"]

            del node["teacherId"], node["class"], node["centrality"], node["code"], node["school"], node[
                "insititution"]

        data["links"] = []
        for link in data["edges"]:
            if "source" not in link or "target" not in link:
                print("缺少 起点 / 终点：", link)
            else:
                link["source"], link["target"] = str(link["source"]), str(link["target"])
                link["value"] = link["weight"]
                if "weight" in link: del link['weight']
                data["links"].append(link)

        """
            在生成的社区关系文件中, community_data 中的数据应该是每个社区中的对比数据, 即其 key 应当包含每个class的值
            但有部分数据并非如此, community_data 的 key 并未包括所有 class, 因此不能使用其作为分类的标准

            前提: nodes中的class连续 ==> 不会出现 1,2,5,...的情况
            传递社区总数
        """
        data["community"] = len(class_id_dict)

        # 添加商务节点
        # data["nodes"].append(self.create_agent_node())

        # 格式化商务创建的社交关系
        # agent_relation_links, core_node = self.create_agent_relation_links(agent_relation, teacher_id_dict, class_id_dict)

        # data["links"].extend(agent_relation_links)

        # data["core_node"] = core_node
        data["core_node"] = class_id_dict

        if "community_data" in data: del data['community_data']
        if "algorithm_compare" in data: del data['algorithm_compare']
        if "edges" in data: del data['edges']

        return data

    except Exception as e:
        print(e)
        return False


def get_community_id_list(industry):
    """
    根据行业获取社区列表
    :param industry:
    :return:
    """
    community_ids = ego_net.get_community_ids_by_industry(industry)
    community_id_list = []
    for community_id_dic in community_ids:
        if community_id_dic.get("community_id") is not None:
            community_id_list.append(community_id_dic.get("community_id"))
    return community_id_list


def get_cooperate_rel_by_community_id_list(industry, user_id, user_name):
    """
    根据社区id获取社区成员关系
    :param industry:
    :param user_id:
    :return:
    """
    data = ego_net.get_cooperate_rel_by_community_id_list_new(industry)
    participate_data = engineer_community_dao.get_activity_participate(user_id)
    result = format2echarts_new(data, participate_data, user_id, user_name)
    return result


def format2echarts_new(data, participate_data, user_id, user_name):
    """
    将返回数据(多个成员的社交关系)格式化为Echarts适配的格式
    :param data:
    :param participate_data:
    :return:
     dict {
            "nodes": [
                {id, name, ....}, ...
            ],

            "links": [
                {"source": xx, "target": xxx}, ...
            ]

        }
    """
    participate_engineer_id_list = []
    for dic in participate_data:
        participate_engineer_id_list.append(dic.get('engineer_id'))
    result = {
        "nodes": [],
        "links": []
    }
    if len(data) == 0:
        return result
    node_dict = {}
    for item in data:
        engineer_id1 = item.get('engineer_id1')
        engineer_id2 = item.get('engineer_id2')
        if engineer_id1 not in node_dict.keys():
            node_dict[engineer_id1] = {
                'id': item.get('engineer_id1'), 'name': item.get('name1'),
                'community': item.get('community1'), 'ep_name': item.get('ep_name1'),
                'patent': item.get('patent1')
            }
        if engineer_id2 not in node_dict.keys():
            node_dict[engineer_id2] = {
                'id': item.get('engineer_id2'), 'name': item.get('name2'),
                'community': item.get('community2'), 'ep_name': item.get('ep_name2'),
                'patent': item.get('patent2')
            }
        result["links"].append({
            "source": engineer_id1,
            "target": engineer_id2,
            "value": item.get('frequency')
        })
    nodes = []
    for key in node_dict:
        nodes.append(node_dict.get(key))

    nodes_dict = {}
    # 将中介与工程师的关系在这里加入

    for node in nodes:
        node_dict = dict(node)
        # print(node_dict)
        if node_dict.get("community") not in nodes_dict:
            nodes_dict[node_dict.get("community")] = []
        nodes_dict[node_dict.get("community")].append(node)
    for key in nodes_dict:
        user_id += 1
        current_user_node = {'id': user_id, 'name': user_name, 'community': nodes_dict[key][0].get('community'),
                             'ep_name': "", "is_agent": 1}

        # 将工程师与中介的关系放在这里加入
        for node in nodes_dict[key]:
            if node.get('id') in participate_engineer_id_list:
                result["links"].append({
                    "source": user_id,
                    "target": node.get("id"),
                    "value": 1,
                })

        nodes_dict[key].append(current_user_node)
    nodes_list = []
    for key in nodes_dict:
        nodes_list.extend(nodes_dict.get(key))
    result["nodes"] = nodes_list
    return result


def format2echarts(data, participate_data, user_id, user_name):
    """
    将返回数据(多个成员的社交关系)格式化为Echarts适配的格式
    :param data:
    :param participate_data:
    :return:
     dict {
            "nodes": [
                {id, name, ....}, ...
            ],

            "links": [
                {"source": xx, "target": xxx}, ...
            ]

        }
    """
    participate_engineer_id_list = []
    for dic in participate_data:
        participate_engineer_id_list.append(dic.get('engineer_id'))
    result = {
        "nodes": [],
        "links": []
    }
    if len(data) == 0:
        return result
    node_dict = {}
    community_id_set = set()
    for item in data:
        teacher_id1 = item["nodes"][0]["id"]
        teacher_id2 = item["nodes"][1]["id"]
        community_id1 = item["nodes"][0]["community"]
        community_id2 = item["nodes"][1]["community"]
        community_id_set.add(community_id1)
        community_id_set.add(community_id2)
        # 获取节点
        if teacher_id1 not in node_dict.keys():
            node_dict[teacher_id1] = item["nodes"][0]
        if teacher_id2 not in node_dict.keys():
            node_dict[teacher_id2] = item["nodes"][1]

        # 获取关系
        result["links"].append({
            "source": teacher_id1,
            "target": teacher_id2,
            "value": item["relationship"][0]["frequency"]
        })
    nodes = [val for key, val in node_dict.items()]
    nodes_dict = {}

    # 将中介与工程师的关系也放在这里加入
    for node in nodes:
        node_dict = dict(node)
        if node_dict.get("community") not in nodes_dict:
            nodes_dict[node_dict.get("community")] = []
        nodes_dict[node_dict.get("community")].append(node)

    for key in nodes_dict:
        user_id += 1
        current_user_node = {'id': user_id, 'name': user_name, 'community': nodes_dict[key][0].get('community'),
                             'ep_name': "", "is_agent": 1}

        # 将工程师与中介的关系放在这里加入
        for node in nodes_dict[key]:
            if node.get('id') in participate_engineer_id_list:
                result["links"].append({
                    "source": user_id,
                    "target": node.get("id"),
                    "value": 1,
                })

        nodes_dict[key].append(current_user_node)

    nodes_list = []
    for key in nodes_dict:
        nodes_list.extend(nodes_dict.get(key))
    result["nodes"] = nodes_list
    return result


def get_community_list(industry):
    """
    由行业名获取社区列表
    :param industry: 行业名
    :return:
    """
    data = ego_net.get_community_list(industry)
    community_list = []
    for id_dic in data:
        community = id_dic.get('community')
        if community is not None:
            community_list.append(community)
    return community_list


def get_namelist(community_id):
    """
    由community_id在图数据库中获得名单
    :param community_id:
    :return:
    """
    datas = ego_net.get_namelist(community_id)
    datas = sorted(datas, key=lambda item: item['patent'], reverse=True)
    items = [
        {
            "公司": data.get('ep_name'),
            "姓名": data.get('name')
        }
        for data in datas
    ]
    return items