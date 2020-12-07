from web.utils import Ego_net as ego_net


def format2echarts(_data):
    """
    将返回数据(多个成员的社交关系)格式化为Echarts适配的格式
    :param _data:

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
    result = {
        "nodes": [],
        "links": []
    }
    if _data is None or len(_data) == 0:
        return result
    node_dict = {}
    for item in _data:
        teacher_id1 = item["nodes"][0]["id"]
        teacher_id2 = item["nodes"][1]["id"]
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
    result["nodes"] = nodes
    return result


def format2echarts2(_data):
    """
    将返回数据(多个成员的社交关系)格式化为Echarts适配的格式
    :param _data:

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
    result = {
        "nodes": [],
        "links": []
    }
    if _data is None or len(_data) == 0:
        return result
    node_dict = {}
    for dic in _data:
        teacher_id1 = dic["t1.id"]
        teacher_id2 = dic["t2.id"]
        # 获取节点
        if teacher_id1 not in node_dict.keys():
            node_dict[teacher_id1] = {
                "request_status": dic["t1.request_status"],
                "id": dic["t1.id"],
                "institution": dic["t1.institution"],
                "visit_status": dic["t1.visit_status"],
                "patent": dic["t1.patent"],
                "school_id": dic["t1.school_id"],
                "name": dic["t1.name"],
                "industry": dic["t1.industry"],
                "team": dic["t1.team"]
            }
        if teacher_id2 not in node_dict.keys():
            node_dict[teacher_id2] = {
                "request_status": dic["t2.request_status"],
                "id": dic["t2.id"],
                "institution": dic["t2.institution"],
                "visit_status": dic["t2.visit_status"],
                "patent": dic["t2.patent"],
                "school_id": dic["t2.school_id"],
                "name": dic["t2.name"],
                "industry": dic["t2.industry"],
                "team": dic["t2.team"]
            }

        # 获取关系
        result["links"].append({
            "source": teacher_id1,
            "target": teacher_id2,
            "value": dic["r.frequency"]
        })
    nodes = []
    for key, val in node_dict.items():
        nodes.append(val)
    result["nodes"] = nodes
    return result


def get_teacher_team(teacher_id):
    """
    获取教师的所在团队的教师id
    :return:
    """
    _data = ego_net.NeoOperator.get_this_teacher_team_id(teacher_id)
    if len(_data) == 0 or _data[0]["teacher.team"] is None:  # 该教师没有team_id，无团队
        return {0}
    team_id = _data[0]["teacher.team"]
    teacher_ids = ego_net.NeoOperator.get_team_member_id(team_id)
    team = convert_team_to_set(teacher_ids)
    return team


def convert_team_to_set(teacher_ids):
    """
    将团队中的列表形式转化为集合形式{t1, t2, t3}
    :param teacher_ids:
    :return:
    """
    team = {0}
    for dic in teacher_ids:
        teacher_id = dic["teacher.id"]
        team.add(teacher_id)
    return team


def get_cooperate_rel(teacher_id_list):
    """
    根据teacher_ids 获取这些teacher的合著关系
    :param teacher_id_list:
    :return:
    """
    _data = ego_net.get_cooperate_rel_teacher_ids(teacher_id_list)
    result = format2echarts(_data)
    return result


def get_cooperate_rel_by_team_id_list(school, institution, team_id_list):
    """
    根据学院中的team_id_list 获取 学院内部的社区关系
    :param school:
    :param institution:
    :param team_id_list:
    :return:
    """
    _data = ego_net.get_cooperate_rel_by_team_id_list(school, institution, team_id_list, 0)
    result = format2echarts2(_data)
    # if len(result["nodes"]) > 70:
    #     _data = ego_net.get_cooperate_rel_by_team_id_list(team_id_list, institution, 3)
    #     result = format2echarts(_data)
    # if len(result["nodes"]) > 70:
    #     _data = ego_net.get_cooperate_rel_by_team_id_list(team_id_list, institution, 5)
    #     result = format2echarts(_data)
    # if len(result["nodes"]) > 70:
    #     _data = ego_net.get_cooperate_rel_by_team_id_list(team_id_list, institution, 8)
    #     result = format2echarts(_data)
    return result


def get_institution_cooperate_rel_by_team_id_list(school, team_id_list, institution):
    """
    根据学院中的team_id_list 获取 学院内部的社区关系
    :param school:
    :param institution:
    :param team_id_list:
    :return:
    """
    _data = ego_net.get_institution_cooperate_rel_by_team_id_list2(school, team_id_list, institution, 0)

    result = format2echarts2(_data)
    result = trim_edges(result)
    return result


def get_team_member_info(school, institution):
    """
    获取某一学院下的团队以及团队中的成员信息，用于构造树图
    :return:
    """
    # 1. 获取学院内部的leader
    leader_list = ego_net.get_leader_list_in_institution(school, institution)
    leader_list = [dic["t1.team"] for dic in leader_list]
    # 2. 获取学院内的节点 关系数据
    _data = ego_net.get_institution_cooperate_rel_by_team_id_list2(school, leader_list, institution, 0)
    result = format2echarts2(_data)
    # 3. 转换数据格式
    result = format_data(result["nodes"], institution)
    return result


def format_data(nodes, institution):
    """

    :param institution:
    :param nodes:
    :return:
    """
    team_id_info_dict = dict()
    teacher_id_info_dict = dict()
    for dic in nodes:
        teacher_id_info_dict[dic["id"]] = dic
        if dic["team"] in team_id_info_dict.keys():
            team_id_info_dict[dic["team"]].append(dic["id"])
        else:
            team_id_info_dict[dic["team"]] = [dic["id"]]
    children = []
    for team_id, teacher_id_list in team_id_info_dict.items():
        if team_id not in teacher_id_info_dict.keys():
            continue
        leader_name = teacher_id_info_dict[team_id]["name"]
        sub_children = []
        for teacher_id in teacher_id_list:
            sub_children.append({
                "name": teacher_id_info_dict[teacher_id]["name"],
                "value": teacher_id_info_dict[teacher_id]["patent"],
                "depth": 2,
                "id": teacher_id
            })
        children.append({
            "name": leader_name + "团队",
            "children": sub_children,
            "depth": 1
        })
    result = {
        "name": institution,
        "children": children,
        "depth": 0
    }
    return result


def trim_edges(data):
    """
    删减多余的边， 如果一个边 两端的点不是同一个团队的，则删掉
    :param data:
    :return:
    """
    nodes = data["nodes"]
    links = data["links"]
    teacher_id_team_id_dict = {}
    for node in nodes:
        teacher_id_team_id_dict[node["id"]] = node["team"]

    trim_links = []
    for link in links:
        source_team_id = teacher_id_team_id_dict[link["source"]]
        target_team_id = teacher_id_team_id_dict[link["target"]]
        if(source_team_id == target_team_id):
            trim_links.append(link)

    return {
        "nodes": nodes,
        "links": trim_links
    }


def get_institution_relation(school, institution):
    """
    根据学校名 和学院名 获取学院内部的社交关系
    :return:
    """
    # 1. 获取学院内部的leader
    leader_list = ego_net.get_leader_list_in_institution(school, institution)
    leader_list = [dic["t1.team"] for dic in leader_list]
    # 2. 根据leader_list 获取 这些团队的社交关系
    result = get_institution_cooperate_rel_by_team_id_list(school, leader_list, institution)
    return result


def get_team_ids_by_teacher_ids(teacher_id_list):
    """
    根据教师的id列表获取这些教师对应的team_id
    :param teacher_id_list:
    :return:
    """
    team_ids = ego_net.get_team_ids_by_teacher_ids(teacher_id_list)
    # team_id_list = [dic["teacher.team"] for dic in team_ids]
    return team_ids


def get_team_id_list_by_teacher_ids(teacher_id_list):
    """
    根据教师的id列表获取这些教师对应的team_id
    :param teacher_id_list:
    :return:[team_id1, team_id2, ...]
    """
    team_ids = ego_net.get_team_ids_by_teacher_ids(teacher_id_list)
    team_id_list = []
    for dic in team_ids:
        if dic["teacher.team"] is not None:
            team_id_list.append(dic["teacher.team"])
    return team_id_list


def update_node_visit_status(teacher_id, status):
    """
    更新节点的拜访状态：0未联系过、1联系过、2做过活动、3签过合同、4创业
    :return:
    """
    result = ego_net.update_node_visit_status(teacher_id, status)
    return result


if __name__ == '__main__':
    get_teacher_team(9961)
