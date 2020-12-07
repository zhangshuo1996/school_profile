"""
@author: zs
@date: 2020.2.20
"""
from web.utils import db

class SchoolService():

    def __init__(self):
        pass

    def get_introduction(self, school):
        """
        从数据库中获取学校的简介
        :return:
        """
        sql = "SELECT INTRODUCTION introduction \
                from es_school \
                where `NAME` = \"" + school + "\""
        introduction = db.execute(sql)
        print(introduction)
        return introduction[0]["introduction"]

    def get_key_discipline(self, school):
        """
        获取这个学校的重点学科（A-及其以上）
        :return: 重点学科列表
        """
        sql = "SELECT es_discipline.`NAME` discipline\
                from es_discipline \
                where es_discipline.`CODE` in \
                ( \
                SELECT es_relation_in_dis.DISCIPLINE_CODE disciline_code \
                from es_relation_in_dis \
                where es_relation_in_dis.INSTITUTION_ID in\
                ( \
                SELECT es_institution.ID institution_id \
                from es_institution \
                where es_institution.SCHOOL_ID = \
                ( \
                SELECT ID \
                from es_school \
                where es_school.`NAME` = \"" + school + "\" \
                ) \
                ) \
                and es_relation_in_dis.EVALUATION LIKE \"A%\" \
                ) \
                "
        res = db.execute(sql)
        key_discipline_list = []
        for d in res:
            key_discipline_list.append(d["discipline"])

        print(key_discipline_list)
        return key_discipline_list