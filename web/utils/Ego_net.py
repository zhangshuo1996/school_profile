from py2neo import Graph
from config import NEO_CHEN as NEO
import logging


import pprint


class NeoOperator(object):

    graph = Graph(NEO["host"], auth=(NEO["user"], NEO["password"]))

    @classmethod
    def get_ego_net(cls, teacher_id):
        """
        根据教师id获取个人中心网络
        :param teacher_id:
        :return:
        [
            {
                "nodes": [Node tyep element, Node type element2],
                "relationship": []
            },...
        ]
        """
        try:
            cql = "Match p=(:Teacher{id:%s})-[r:学术合作]-(:Teacher) return NODES(p) as nodes," \
                  " RELATIONSHIPS(p) as relationship" % teacher_id
            back = NeoOperator.graph.run(cql).data()
            return back
        except Exception as e:
            print(e)

    @classmethod
    def get_this_teacher_net(cls, teacher_id):
        """
        根据教师的id获取与其团队中的其他教师id
        :return:
        """
        try:
            cql = "Match p=(:Teacher{id:%s}) return NODES(p) as nodes, RELATIONSHIPS(p) as relationship" % str(teacher_id)
            back = NeoOperator.graph.run(cql).data()
            return back
        except Exception as e:
            print(e)

    @classmethod
    def get_this_teacher_team_id(cls, teacher_id):
        """
        获取该教师所在团队的team_id
        :param teacher_id:
        :return:
        """
        try:
            cql = "match (teacher:Teacher) where teacher.id = %s return teacher.team" % str(teacher_id)
            back = NeoOperator.graph.run(cql).data()
            return back
        except Exception as e:
            print(e)

    @classmethod
    def get_team_member_id(cls, team_id):
        """
        根据team_id获取该团队下的所有成员id
        :param team_id:
        :return:
        """
        try:
            cql = "match (teacher:Teacher) where teacher.team = %s return teacher.id" % str(team_id)
            back = NeoOperator.graph.run(cql).data()
            return back
        except Exception as e:
            print(e)


def get_member_id_by_team_id(team_id):
    """
    根据team_id获取该团队下的所有成员id
    :param team_id:
    :return:
    """
    try:
        cql = "match (teacher:Teacher) where teacher.team = %s return teacher.id" % str(team_id)
        back = NeoOperator.graph.run(cql).data()
        return back
    except Exception as e:
        print(e)


def get_team_ids_by_teacher_ids(teacher_id_list):
    """
    根据teacher_ids 获取这些teacher对应的团队team_ids
    :return:[{"teacher.team": team_id, "teacher.id": t_id}]
    """
    try:
        cql = "match (teacher:Teacher) where teacher.id in [{ids_str}] return teacher.team, teacher.id"
        cql = compose_cql(cql, teacher_id_list)
        back = NeoOperator.graph.run(cql).data()
        return back
    except Exception as e:
        print(e)


def get_cooperate_rel_teacher_ids(teacher_id_list):
    """
    根据teacher_ids 获取这些teacher的合著关系
    :return:
    """
    try:
        cql = """
            Match p=(t:Teacher)-[r:cooperate]-(:Teacher) 
            where t.id in [{ids_str}]
            return NODES(p) as nodes, RELATIONSHIPS(p) as relationship
        """
        cql = compose_cql(cql, teacher_id_list)
        print(cql)
        back = NeoOperator.graph.run(cql).data()
        return back
    except Exception as e:
        print(e)


def get_cooperate_rel_by_team_id_list(school, institution, team_id_list, patent_num):
    """
    根据学院中的team_id_list 获取 学院内部的社区关系
    :param school:
    :param patent_num:
    :param institution:
    :param team_id_list:
    :return:
    """
    try:
        cql = """
                   match p=(u1:University)-[:include]-(t1:Teacher)-[r:cooperate]-(t2:Teacher)-[:include]-(u2:University)
                    where u1.name = \"{school}\"
                    and t1.team in [{ids_str}] and t2.team in [{ids_str}] 
                    and t1.patent > 0 
                    and t1.patent > {patent_num} and t2.patent > {patent_num}
                    return t1.id,t1.name, t1.request_status, t1.institution, t1.visit_status, t1.patent, t1.school_id, t1.industry, 
                    t1.team,t2.id,t2.name, t2.request_status, t2.institution, t2.visit_status, t2.patent, t2.school_id, t2.industry, t2.team,r.frequency
                """

        ids_str = ""
        for _id in team_id_list:
            ids_str += str(_id) + ","
        ids_str = ids_str[0:-1]
        cql = cql.format(ids_str=ids_str, school=school, institution=institution, patent_num=patent_num)
        logging.warning(cql)
        back = NeoOperator.graph.run(cql).data()
        return back
    except Exception as e:
        print(e)


def get_institution_cooperate_rel_by_team_id_list(school, team_id_list, institution, patent_num):
    """
    根据学院中的team_id_list 获取 学院内部的社区关系
    :param school:
    :param patent_num:
    :param institution:
    :param team_id_list:
    :return:
    """
    # try:
    cql = """
                match p=(t1:Teacher)-[r:cooperate]-(t2:Teacher) 
                where (t1.team in [{ids_str}] and t2.team in [{ids_str}] and t1.institution = \"{institution}\" and t2.institution = \"{institution}\")
                and (
                (t1.patent > {patent_num} or t1.team = t1.id)
                and (t2.patent > {patent_num} or t2.team = t2.id)
                )
                return NODES(p) as nodes, RELATIONSHIPS(p) as relationship
            """
    cql = compose_cql2(cql, school, team_id_list, institution, patent_num)
    print(cql)
    back = NeoOperator.graph.run(cql).data()
    return back
    # except Exception as e:
    #     print(e)


def get_institution_cooperate_rel_by_team_id_list2(school, team_id_list, institution, patent_num):
    """
    根据学院中的team_id_list 获取 学院内部的社区关系
    :param school:
    :param patent_num:
    :param institution:
    :param team_id_list:
    :return:
    """
    # try:
    cql = """
    
                match p=(u1:University)-[:include]-(t1:Teacher)-[r:cooperate]-(t2:Teacher)-[:include]-(u2:University)
                where u1.name = \"{school}\"
                and (t1.team in [{ids_str}] 
                and t1.institution = \"{institution}\" and t2.institution = \"{institution}\")
                return t1.id,t1.name, t1.request_status, t1.institution, t1.visit_status, t1.patent, t1.school_id, t1.industry, 
                t1.team,t2.id,t2.name, t2.request_status, t2.institution, t2.visit_status, t2.patent, t2.school_id, t2.industry, t2.team,r.frequency
            """
    cql = compose_cql2(cql, school, team_id_list, institution, patent_num)
    print(cql)
    back = NeoOperator.graph.run(cql).data()
    return back


def get_leader_list_in_institution(school, institution):
    """
    获取学院内部的所有 leader
    :param school:
    :param institution:
    :return:
    """
    cql = """
        match p=(u1:University)-[:include]-(t1:Teacher)
        where u1.name = \"{school}\" 
        and t1.institution = \"{institution}\" and t1.team = t1.id
        return t1.team
        order by t1.member desc limit 15
    """
    cql = cql.format(school=school, institution=institution)
    print(cql)
    back = NeoOperator.graph.run(cql).data()
    return back


def compose_cql2(cql, school, _list, institution, patent_num):
    """
    组合查询cql中有in的语句,
    :param school:
    :param patent_num:
    :param institution:
    :param _list:
    :param cql:
    :return:
    """
    ids_str = ""
    for _id in _list:
        ids_str += str(_id) + ","
    ids_str = ids_str[0:-1]
    return cql.format(school=school, ids_str=ids_str, institution=institution, patent_num=patent_num)


def compose_cql(cql, _list):
    """
    组合查询cql中有in的语句,
    :param _list:
    :param cql:
    :return:
    """
    ids_str = ""
    for _id in _list:
        ids_str += str(_id) + ","
    ids_str = ids_str[0:-1]
    return cql.format(ids_str=ids_str)


def update_node_visit_status(teacher_id, status):
    """
    更新教师节点的拜访状态
    :param teacher_id:
    :param status:
    :return:
    """

    try:
        cql = """
            match (t:Teacher) where t.id = {teacher_id}  set t.visit_status = {status} return t
        """.format(teacher_id=teacher_id, status=status)
        print(cql)
        back = NeoOperator.graph.run(cql).data()
        return back
    except Exception as e:
        print(e)


def format2Echarts(data):
    """
    将返回数据格式化为Echarts适配的格式
    :param data:

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
    result = {"nodes":[], "links": []}
    if len(data) == 0:
        return result

    center_node = dict(data[0]["nodes"][0])
    result["nodes"].append(center_node)

    for item in data:
        target_node = dict(item["nodes"][1])
        result["nodes"].append(target_node)

        relation = dict(item["relationship"][0])
        result["links"].append({"source": center_node['id'], "target": target_node["id"], "value": relation})

    return result


def get_community_ids_by_industry(industry):
    """
    根据行业获取社区ids
    :param industry:
    :return:
    """
    cql = """match(n:Engineer) where n.industry=~'.*{industry}.*' 
            return distinct n.community as community_id""".format(industry=industry)
    back = NeoOperator.graph.run(cql).data()
    return back


def get_cooperate_rel_by_community_id_list(industry):
    """
    根据行业中的community_id_list获取行业内部的社区关系
    :param industry
    :return:
    """
    cql = """
        match p=(t1:Engineer)-[r:engineer_community]-(t2:Engineer)
        where t1.industry='{industry}' and t1.show=1 and t2.industry='{industry}' and t2.show=1
        return NODES(p) as nodes, RELATIONSHIPS(p) as relationship
    """.format(industry=industry)
    print(cql)
    back = NeoOperator.graph.run(cql).data()
    return back


def get_cooperate_rel_by_community_id_list_new(industry):
    """
    根据行业中的community_id_list获取行业内部的社区关系
    :param industry
    :return:
    """
    cql = """
        match p=(t1:Engineer)-[r:engineer_community]-(t2:Engineer)
        where t1.industry='{industry}' and t1.show=1 and t2.industry='{industry}' and t2.show=1 return 
        t1.id as engineer_id1,t1.name as name1, t1.community as community1,t1.ep_name as ep_name1,t1.patent as patent1,
        t2.id as engineer_id2,t2.name as name2, t2.community as community2,t2.ep_name as ep_name2,t2.patent as patent2,
        r.frequency as frequency
    """.format(industry=industry)
    print(cql)
    back = NeoOperator.graph.run(cql).data()
    return back


# def compose_cql2(cql, _list, patent_num):
#     """
#     组合查询cql中有in的语句,
#     :param patent_num:
#     :param _list:
#     :param cql:
#     :return:
#     """
#     ids_str = ""
#     for _id in _list:
#         ids_str += str(_id) + ","
#     ids_str = ids_str[0:-1]
#     return cql.format(ids_str=ids_str, patent_num=patent_num)


def get_community_list(industry):
    """
    由行业名获取社区列表
    :param industry: 行业名
    :return:
    """
    cql = """match (n:Engineer) where n.industry='{title}' return distinct n.community as community""".format(title=industry)
    back = NeoOperator.graph.run(cql).data()
    return back


def get_namelist(community_id):
    """由社区id获取工程师名单"""
    cql = """match(n:Engineer) where n.community={community_id} return n.name as name, n.ep_name as ep_name, n.patent as patent""".format(community_id=community_id)
    back = NeoOperator.graph.run(cql).data()
    return back


def get_activity_data():
    """由中介id获取与该中介有关的工程师"""
    cql = """match(n:Engineer) where """


if __name__ == '__main__':
    data = NeoOperator.get_ego_net(86791)
    print(pprint.pformat(data))
    res = format2Echarts(data)
