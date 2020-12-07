from web.utils import db


def get_activity_participate(agent_id):
    sql = """select engineer_id from activity_participate where agent_id=:agent_id"""
    return db.select(sql, {'agent_id': agent_id})