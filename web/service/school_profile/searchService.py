"""
搜索相关服务
2020.08.17
by zhang
"""
from web.dao.school_profile import search
import json


def save_this_search_text(searcher_id, search_text):
    """
    记录此次搜索的文本
    :param searcher_id:
    :param search_text:
    :return:
    """
    outcome = search.get_history_by_text(search_text)
    if outcome is None or "id" not in outcome.keys():
        outcome_id = search.save_this_search_text(searcher_id, search_text)
    else:
        outcome_id = outcome["id"]
        search.update_history_time(search_text)
    return outcome_id
