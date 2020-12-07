"""
有关企业搜索
"""
import pymysql

from config import MysqlDB_Params, NEO_CHEN
from web.utils.neo4j_operator import Neo4jOperate


conn = pymysql.connect(host=MysqlDB_Params['host'], user=MysqlDB_Params["user"], password=MysqlDB_Params["password"],
                       db=MysqlDB_Params['database'], port=MysqlDB_Params['port'], charset=MysqlDB_Params['charset'])
cursor = conn.cursor(pymysql.cursors.DictCursor)

neo = Neo4jOperate(**NEO_CHEN)

def get_en_info_by_id(ep_id):
    """
    根据企业名获取企业列表，模糊查询
    :param ep_id: 企业名
    :return: 企业信息
    """
    conn.ping(reconnect=True)
    sql = """select * from ep_base_info where id=%s"""
    cursor.execute(sql, ep_id)
    result = cursor.fetchone()
    return result


def get_ep_ip_by_pa_id(pa_id):
    """
    根据专利id获取企业信息
    :param pa_id:
    :return:
    """
    conn.ping(reconnect=True)
    sql = """select id, name, convert(registered_capital,decimal) registered_capital, entablish_date, website, telephone, telephone_more
          from ep_base_info
          where id in 
          (select ep_id from ep_patent where pa_id in %s)"""
    cursor.execute(sql, pa_id)
    result = cursor.fetchall()
    return result


def get_engineer_by_pa_id(pa_id):
    """
    根据专利获取相关工程师
    :param pa_id:
    :return: 工程师名单
    """
    conn.ping(reconnect=True)
    sql = """select ep_id, pa_inventor engineer_name from ep_patent
            where pa_id in %s
        """
    cursor.execute(sql, pa_id)
    result = cursor.fetchall()
    return result


def get_ep_id_by_pa_id(pa_list):
    """
    根据搜索的专利id获取企业id
    :param pa_list: 专利列表
    :return:
    """
    conn.ping(reconnect=True)
    sql = """
        select ep_id,pa_id from ep_patent where pa_id in %s
    """
    cursor.execute(sql, pa_list)
    result = cursor.fetchall()
    return result


def get_pa_info_by_pa_id(pa_list):
    """
    根据专利id获取专利信息
    :param pa_list: 专利id
    :return:
    """
    conn.ping(reconnect=True)
    sql = """
        select pa_id, pa_name, pa_filing_date, pa_public_date, pa_inventor, pa_abstract
        from ep_patent 
        where pa_id in %s and pa_type != 3
    """
    cursor.execute(sql, pa_list)
    result = cursor.fetchall()
    return result


def get_ip_count_type(ep_id):
    """
    获取企业的专利、实用新型、软件著作权数量
    :param ep_id: 企业id
    :return:
    """
    conn.ping(reconnect=True)
    sql = """
        select count(1) count from ep_patent where ep_id = %s and (pa_type = 1 or pa_type = 8) 
        UNION all select count(1) count from ep_patent where ep_id = %s and (pa_type = 2 or pa_type = 9) 
        UNION all select count(1) count from software_copyright where ep_id = %s
    """
    cursor.execute(sql, (ep_id, ep_id, ep_id))
    result = cursor.fetchall()
    return result


def get_engineer_with_count(ep_id):
    """
    根据ep_id获取企业里所有的工程师以及知识产权数量
    :param ep_id:
    :return:
    """
    conn.ping(reconnect=True)
    sql = """
        select id, engineer_name, patent_num 
        from ep_engineer
        where ep_id = %s 
        ORDER BY patent_num desc
        limit 10
    """
    cursor.execute(sql, ep_id)
    result = cursor.fetchall()
    return result


def get_engineer_relation(engineer_id):
    """
    获取工程师之间的合作关系
    :param engineer_id: 工程师id
    :return:
    """
    conn.ping(reconnect=True)
    sql = """
        select engineer_id,engineer_name, pa_id from engineer_patent 
        where engineer_id in %s
    """
    cursor.execute(sql, engineer_id)
    result = cursor.fetchall()
    return result


def get_engineer_count(ep_id):
    """
    获取企业的工程师数量
    :param ep_id:企业id
    :return:
    """
    conn.ping(reconnect=True)
    sql = """
        select count(1) count from ep_engineer where ep_id = %s 
    """
    cursor.execute(sql, ep_id)
    result = cursor.fetchone()
    return result


def get_ip_count(ep_ip):
    """
    获取企业的知识产权数量
    :param ep_ip: 企业id
    :return:
    """
    conn.ping(reconnect=True)
    sql = """
        select sum(count1) num from (
        select count(*) AS count1 from ep_patent where ep_id = %s 
        union all
        select count(*) as count1 from software_copyright where ep_id = %s
        ) as total
    """
    cursor.execute(sql, (ep_ip, ep_ip))
    result = cursor.fetchone()
    return result


def get_register_money(ep_id):
    """
    获取企业的注册资金
    :param ep_id: 企业id
    :return:
    """
    conn.ping(reconnect=True)
    sql = """
        select registered_capital from ep_base_info where id = %s
    """
    cursor.execute(sql, ep_id)
    result = cursor.fetchone()
    return result


def get_is_en_tech_rese_center(ep_id):
    """
    获取是否是工程技术研究中心、高企
    :param ep_id: 企业id
    :return:
    """
    conn.ping(reconnect=True)
    sql = """
        select count(1) count from high_tech_affirm where ep_id = %s
    """
    cursor.execute(sql, ep_id)
    result = cursor.fetchone()
    return result


def sort_ep_by_date(ep_id):
    """
    对选择的企业按成立时间从早到晚排序
    :param ep_id: 企业id列表
    :return:
    """
    conn.ping(reconnect=True)
    sql = """
          select id, name, convert(registered_capital,decimal) registered_capital, entablish_date, website, telephone, telephone_more
          from ep_base_info
          where id in %s
          order by entablish_date
    """
    cursor.execute(sql, ep_id)
    result = cursor.fetchall()
    return result


def sort_ep_by_date_desc(ep_id):
    """
    对选择的企业按成立时间从晚到早排序
    :param ep_id: 企业id列表
    :return:
    """
    conn.ping(reconnect=True)
    sql = """
          select id, name, convert(registered_capital,decimal) registered_capital, entablish_date, website, telephone, telephone_more
          from ep_base_info
          where id in %s
          order by entablish_date desc
    """
    cursor.execute(sql, ep_id)
    result = cursor.fetchall()
    return result


def sort_ep_by_money(ep_id):
    """
    对选择的企业按注册资金从小到大排序
    :param ep_id: 企业id列表
    :return:
    """
    conn.ping(reconnect=True)
    sql = """
          select id, name, convert(registered_capital,decimal) registered_capital, entablish_date, website, telephone, telephone_more
          from ep_base_info
          where id in %s
          order by registered_capital
    """
    cursor.execute(sql, ep_id)
    result = cursor.fetchall()
    return result


def sort_ep_by_money_desc(ep_id):
    """
    对选择的企业按注册资金从大到小排序
    :param ep_id: 企业id列表
    :return:
    """
    conn.ping(reconnect=True)
    sql = """
          select id, name, convert(registered_capital,decimal) registered_capital, entablish_date, website, telephone, telephone_more
          from ep_base_info
          where id in %s
          order by registered_capital desc
    """
    cursor.execute(sql, ep_id)
    result = cursor.fetchall()
    return result


def sort_ep_by_similarity(ep_id):
    """
    对选择的企业按相似度排序
    :param ep_id: 企业id列表
    :return:
    """
    conn.ping(reconnect=True)
    sql = """
              select id, name, convert(registered_capital,decimal) registered_capital, entablish_date, website, telephone, telephone_more
              from ep_base_info
              where id in %s
        """
    cursor.execute(sql, ep_id)
    result = cursor.fetchall()
    return result


def get_ep_info(ep_list):
    """
    获取企业详细信息,导出数据
    :param ep_list:企业列表
    :return:
    """
    conn.ping(reconnect=True)
    sql = """
          select * from ep_base_info where id in %s
    """
    cursor.execute(sql, ep_list)
    result = cursor.fetchall()
    return result


def get_pa_info(pa_list):
    """
    根据专利id获取专利信息，导出数据
    :param pa_list: 专利id列表
    :return:
    """
    conn.ping(reconnect=True)
    sql = """
        select * from ep_patent where pa_id in %s and pa_type != 3
    """
    cursor.execute(sql, pa_list)
    result = cursor.fetchall()
    return result


def get_history(user_id):
    """
    获取用户搜索历史
    :param user_id: 用户id
    :return:
    """
    conn.ping(reconnect=True)
    sql = """
        select id,search_content from ep_portrait_search_history where user_id = %s order by search_time desc limit 8
    """
    cursor.execute(sql, user_id)
    result = cursor.fetchall()
    return result


def delete_history(history_id):
    """
    删除用户历史记录
    :param history_id: 历史id
    :return:
    """
    conn.ping(reconnect=True)
    sql = """
        delete from ep_portrait_search_history where id = %s
    """
    cursor.execute(sql, history_id)
    return conn.commit()


def update_history(history_id):
    """
    删除用户历史记录
    :param history_id: 历史id
    :return:
    """
    conn.ping(reconnect=True)
    sql = """
        update ep_portrait_search_history set search_time=UNIX_TIMESTAMP(NOW()) where id = %s
    """
    cursor.execute(sql, history_id)
    return conn.commit()


def search_history(search_content, user_id):
    """
    查找历史记录
    :param search_content: 检索内容
    :param user_id: 用户id
    :return:
    """
    conn.ping(reconnect=True)
    sql = """
        select id from ep_portrait_search_history where search_content = %s and user_id = %s
    """
    cursor.execute(sql, (search_content, user_id))
    result = cursor.fetchall()
    return result


def insert_history(user_id, search_content):
    """
    删除用户历史记录
    :param history_id: 历史id
    :return:
    """
    conn.ping(reconnect=True)
    sql = """
        insert into ep_portrait_search_history(user_id, search_content, search_time) values(%s,%s,UNIX_TIMESTAMP(NOW()))
    """
    cursor.execute(sql, (user_id, search_content))
    return conn.commit()


def get_all_industry():
    """
    获取所有企业的行业
    :return:
    """
    conn.ping(reconnect=True)
    sql = """select industry from ep_base_info where patent_count > 0 or practical_count > 0 or software_count > 0"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def get_patent_by_first_ipc():
    """
    获取所有大类ipc的所有专利数量
    :param ipc_id:
    :return:
    """
    conn.ping(reconnect=True)
    sql = """select ipc_root, ipc_title, count(1) count from 
            (select distinct pa_id, ipc_root, ipc.title ipc_title
            from engineer_patent 
            left join ipc on ipc.code = ipc_root) 
            as a 
            where ipc_title is not null 
            GROUP BY ipc_root,ipc_title
            order by count desc"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def get_patent_by_second_ipc():
    """
    获取所有中类ipc的所有专利数量
    :param ipc_id:
    :return:
    """
    conn.ping(reconnect=True)
    sql = """select ipc_class, ipc_title, count(1) count from 
            (select distinct pa_id, ipc_class, ipc.title ipc_title
            from engineer_patent 
            left join ipc on ipc.code = ipc_class) 
            as a 
            where ipc_title is not null 
            GROUP BY ipc_class,ipc_title
            order by count desc"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def get_patent_by_third_ipc():
    """
    获取所有小类ipc的所有专利数量
    :param ipc_id:
    :return:
    """
    conn.ping(reconnect=True)
    sql = """select ipc_class_sm, ipc_title, count(1) count from 
            (select distinct pa_id, ipc_class_sm, ipc.title ipc_title
            from engineer_patent 
            left join ipc on ipc.code = ipc_class_sm) 
            as a 
            where ipc_title is not null 
            GROUP BY ipc_class_sm,ipc_title
            order by count desc"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def get_en_info_by_name_dim(ep_name):
    """
    根据企业名获取企业列表，模糊查询
    :param ep_name: 企业名
    :return: 企业信息
    """
    conn.ping(reconnect=True)
    query_param = ['%%%s%%' % ep_name]
    sql = "select * from ep_base_info where name like %s"
    cursor.execute(sql, query_param)
    result = cursor.fetchall()
    return result


def get_max_patent_engineer_id(ep_id):
    """
    获取当前企业中专利数量最多的工程师节点
    :param ep_id: 企业id
    :return:
    """
    conn.ping(reconnect=True)
    sql = """
        select id from ep_engineer where ep_id = %s order by patent_num desc limit 1
    """
    cursor.execute(sql, ep_id)
    result = cursor.fetchone()
    return result


def get_engineer_net_center(engineer_id):
    """
    获取企业里专利数量最多的工程师个人中心网络
    :param engineer_id: 工程师id
    :return:
    """
    cql = "Match (c:Company)-[:employ]-(e:Engineer)-[co:cooperate]-(e2:Engineer) " \
          "where e.id=%d return e.name,e.patent,e.visit_status,e.id,e2.id,e2.name,e2.patent,e2.visit_status limit 20" % (engineer_id)
    return neo.run(cql)


def get_engineer_node(ep_id):
    """
    获取企业的前10个工程师节点
    :param ep_id: 企业id
    :return:
    """
    cql = "Match (c:Company)-[:employ]-(e:Engineer) where c.id=%s return e.id as id, e.name as name, e.patent as patent, e.visit_status as visit_status order by e.patent desc limit 10" %(ep_id)
    return neo.run(cql)


def update_engineer_visited_status(engineer_id, visited_status):
    """
    更新工程师访问状态
    :param engineer_id:工程师id
    :param visited_status:访问状态
    :return:
    """
    cql = "Match (e:Engineer) where e.id = %s set e.visit_status = %s" %(engineer_id, visited_status)
    return neo.run(cql)


def get_role_with_ep_portrait(user_id):
    """
    获取当前用户对于企业画像的权限
    :param user_id: 用户
    :return:
    """
    conn.ping(reconnect=True)
    sql = """select * from user_role where (role_id=60 or role_id=61) and user_id= %s"""
    cursor.execute(sql, user_id)
    result = cursor.fetchall()
    return result


