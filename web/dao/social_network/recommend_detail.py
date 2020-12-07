"""
获取推荐团队的详细信息
"""
from web.settings import RELATION, LABEL
from web.utils.neo4j_operator import neo4j as neo4j


def getTeamBasicInfo(_id, teacher=True):
    org = LABEL["UNIVERSITY"] if teacher is True else LABEL["COMPANY"]
    label = LABEL["TEACHER"] if teacher is True else LABEL["ENGINEER"]

    cql = "match (org:{org})-[]-(l:{label}) where l.id={id} " \
          "return org.name as org, l.member as members, l.name as name, " \
          "l.institution as institution".format(org=org, label=label, id=_id)
    return neo4j.run(cql)


def getTeamPatents(team_id, teacher=True, skip=0, limit=30):
    """
    根据 team_id 获取团队的专利， 包括专利号，专利名，专利发布时间
    :return: [{专利申请号， 专利名，专利发布时间}, ...]
        eg: [{"code": "xxxx", "name": "某某专利", "date": 1574899200}, ....]
    """
    label = LABEL["TEACHER"] if teacher is True else LABEL["ENGINEER"]
    cql = "match (:%s{team:%d})-[:write]-(p:Patent) " \
          "with distinct(p.application_number) as code, p.name as name, p.application_date as date " \
          "return code, name, date order by date desc skip %d limit %d" % (label, team_id, skip, limit)
    return neo4j.run(cql)


def getTeamField(eid, tid):
    """
    获取 工程师团队 与 专家团队 的行业交集
    :return: [{}]
    """
    cql = "match (e:Engineer{team:%d}) with distinct(e.industry) as industry_e, count(e.industry) as count_e " \
          "match (t:Teacher{team:%d}) with distinct(t.industry) as industry_t, count(t.industry) as count_t, " \
          "industry_e, count_e " \
          "return industry_e, industry_t  order by count_e desc, count_t desc limit 1" % (eid, tid)
    return neo4j.run(cql)


def getTeamPatentsNumber(_id, teacher=True):
    """
    TODO 根据 team_id 获取团队的专利数量， 待删除
    """
    label = LABEL["TEACHER"] if teacher is True else LABEL["ENGINEER"]
    cql = "Match (l:{label})-[:write]-(p:Patent) where l.team={id} " \
          "return count(distinct(p.application_number)) as nums".format(label=label, id=_id)
    return neo4j.run(cql)


def getTechnicalFieldComparison(eid=None, tid=None, team=True):
    """
    TODO to be deleted
    获取 企业工程师与专家的共同专利
    """
    param = "team" if team is True else "id"
    cql = "Match (e:Engineer)-[:write]-(ep:Patent)-[:include]-(ipc:IPC)-[:include]-(tp:Patent)-[:write]-(t:Teacher) " \
          f"where e.{param}={eid} and t.{param}={tid} " \
          "return ep.application_number as e_patent, " \
          "tp.application_number as t_patent, ipc.code as ipc".format(param=param, eid=eid, tid=tid)
    return neo4j.run(cql)


def getTeamTechnicalFieldDistribute(team_id, teacher=True):
    """
    获取企业工程师 / 高校专家的 团队专利技术分布 ==> 各个ipc下的专利数量分布
    """
    label = LABEL["TEACHER"] if teacher is True else LABEL["ENGINEER"]
    cql = f"Match (n:{label})-[:write]-(p:Patent)-[r:include]-(ipc:IPC) " \
          f"where n.team={team_id} " \
          f"return ipc.code as ipc, count(r) as count"
    return neo4j.run(cql)


def getTeamMembers(team_id, teacher=True):
    """
    获取团队成员信息，用于展示团队关系图
    """
    label = LABEL["TEACHER"] if teacher is True else LABEL["ENGINEER"]
    cql = f"match (t1:{label})-[r:cooperate]->(t2:{label}) where t1.team={team_id} and t2.team={team_id} " \
          f"and t1.id <> t2.id return t1.id as id1, t1.name as name1, t1.patent as patent1, r.frequency as count, " \
          f"t2.id as id2, t2.name as name2, t2.patent as patent2".format(label=label, team_id=team_id)
    return neo4j.run(cql)

