from web.utils import db


def save_this_search_text(searcher_id, search_text):
    """
    记录此次搜索的文本
    :param searcher_id:
    :param search_text:
    :return:
    """
    sql = """
        insert into search_history
        (searcher_id, search_text, gmt_create)
        values (?, ?, now())
    """
    return db.insert(sql, searcher_id, search_text, bind='data_mining')


def get_history_by_text(search_text):
    """
    判断是否存在相似的文本
    :param search_text:
    :return:
    """
    sql = """
        select id
        from search_history
        where search_text=:search_text
    """
    return db.select_one(sql, {"search_text": search_text}, bind='data_mining')


def update_history_time(search_text):
    """
    更新该搜索文本所在行的时间
    :param search_text:
    :return:
    """
    sql = """
        update search_history
        set gmt_create = now()
        where search_text = ?
    """
    return db.update(sql, search_text, bind='data_mining')
