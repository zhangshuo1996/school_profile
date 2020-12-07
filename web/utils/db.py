"""
使用原生sql代替flask-sqlalchemy的使用
"""
from web.extensions import db


def select(sql, params=None, fetch='all', convert_list=False, bind=None):
    """
    以dict方式返回数据
    :param sql: select * from xxx where name=:name
    :param params: {'name': 'zhangsan'}
    :param fetch: all one
    :param convert_list: 是否把dict 转换成 list，仅仅对只有单个键的dict有效
    :param bind: 连接的数据，默认取配置的SQLALCHEMY_DATABASE_URL
    :return: 默认返回全部数据，返回格式[{}, {}]，如果fetch='one'，返回单条数据，格式为dict
    """
    if params is None:
        params = {}

    result_proxy = db.session.execute(sql, params, bind=db.get_engine(bind=bind))
    if fetch == 'one':
        result_tuple = result_proxy.fetchone()
        if result_tuple:
            result = dict(zip(result_proxy.keys(), list(result_tuple)))
        else:
            return None
    else:
        result_tuple_list = result_proxy.fetchall()
        if result_tuple_list:
            result = []
            keys = result_proxy.keys()
            for row in result_tuple_list:
                if len(keys) == 1 and convert_list:
                    result_row = row[0]
                else:
                    result_row = dict(zip(keys, row))
                result.append(result_row)
        else:
            return []
    return result


def select_one(sql, params=None, fetch='one', convert_list=False, bind=None):
    """
    只获取一条数据，参数同select()
    :param sql:
    :param params:
    :param fetch:
    :param convert_list:
    :param bind:
    :return:
    """
    return select(sql, params, fetch, convert_list, bind)

