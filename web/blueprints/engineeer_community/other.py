import pymysql
import json

conn=pymysql.connect(host='49.235.2.212', user='root', passwd='5ag3oYEGVwRgHQ2020', port=3306, db='ren_db', charset='utf8')
cur = conn.cursor()


def get_industry_rank():
    """获取行业排名"""
    sql = "select * from industry where depth=2"
    cur.execute(sql)
    industry_info = cur.fetchall()
    rank_list = []
    rank_dict = {}
    for info in industry_info:
        code = info[0]
        title = info[1]
        description = info[2]
        depth = info[3]
        parent_code = info[4]
        num = get_patent_count_of_industry_and_unit("开发区", code)
        if num != 0:
            rank_list.append({"code": code, "title": title, "patent_num": num})
    rank_list = sorted(rank_list, key=lambda item: item.get("patent_num"), reverse=True)
    with open('industry.txt', 'w') as f:
        f.write(json.dumps(rank_list))
    print("length")
    print(len(rank_list))
    print(rank_list[:20])


def get_patent_count_of_industry_and_unit(name, industry_parent_code):
    """
    根据单位名称获取该行业下对应的专利数量
    :param name: 高校名称或所在区县的名称(目前仅仅是town)
    :param industry_parent_code: 行业代码，目前只能中类
    :return: 专利总数量
    """
    # industry = Industry.query.get(industry_parent_code)
    # if industry is None or industry.depth != 2:
    #     logging.warning('industry not found or the depth != 2')
    #     return 0
    # 获取该行业对应的ipc
    ipc_code_list = get_ipc_code_list_by_industry_parent_code(industry_parent_code)
    # 专利的总数量和随年份的数量
    patent_count = get_patent_count_of_industry_and_district(name, ipc_code_list)
    # statistics = command_dao.get_patent_count_by_year_of_industry_and_district(name, ipc_code_list)
    # 把数据由{year: str, count: int} => (str, int)
    # results = [(statistic['year'], statistic['count']) for statistic in statistics]
    return patent_count


def get_ipc_code_list_by_industry_parent_code(parent_code):
    """
    根据parent_id获取相对应的ipc id数组
    :param parent_code: 国民经济行业 中类id
    :return: [ipc,]
    """
    # 获取行业对应的大组分类号，以及对应的全部分类号
    sql = """
    (select DISTINCT ipc.code from industry
    join industry_ipc on industry_ipc.industry_code=industry.code
    join ipc on ipc.parent_code=ipc_code
    where industry.parent_code=%s) UNION
    select ipc_code from industry
    join industry_ipc on industry_ipc.industry_code=industry.code
    where industry.parent_code=%s
    """%(parent_code, parent_code)
    cur.execute(sql)
    ipc_code_tuples = cur.fetchall()
    ipc_code_list = []
    for ipc_code_tuple in ipc_code_tuples:
        ipc_code_list.append(ipc_code_tuple[0])
    return ipc_code_list


def get_patent_count_of_industry_and_district(town, ipc_id_list):
    if len(ipc_id_list) == 0:
        return 0
    sql = """
    select count(DISTINCT patent_ipc.patent_id) count from district
    join enterprise on enterprise.district_id=district.id
    join enterprise_patent on enterprise_patent.enterprise_id=enterprise.id
    join patent_ipc on patent_ipc.patent_id=enterprise_patent.patent_id
    where town="开发区" and patent_ipc.ipc_code in (%s)
    """
    ipc_words = ['"%s"' % cls_number for cls_number in ipc_id_list]
    sql = sql % ",".join(ipc_words)
    cur.execute(sql)
    result = cur.fetchone()
    if len(result) == 0:
        return 0
    result = result[0]
    print(result)
    return result


if __name__ == "__main__":
    get_industry_rank()