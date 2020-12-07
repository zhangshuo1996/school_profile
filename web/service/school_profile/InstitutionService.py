"""
@author: zs
@date: 2020.2.19
"""
from web.utils import db


class InstitutionService():
    institution_patent = []

    def __init__(self):

        pass

    def get_institution_patent(self, school, institution):
        """
        获取其他学校与该学院属于同一学科的学院的专利成果数量，以及该学院的所处学科
        :return:[
                    {"x": school, "y": num, "institution": institution},
                    {...},
                    ...
                ]
        """
        sql = "\
        select es_institution.SCHOOL_NAME school_name,es_institution.`NAME` institution_name, t5.patent_num patent_num\
        from es_institution, \
        ( \
        SELECT * \
        from \
        ( \
        SELECT  t3.INSTITUTION_ID institution_id, count(1) patent_num \
        from \
        ( \
        SELECT t2.INSTITUTION_ID, t2.teacher_id, teacher_patent2.patent_id \
        from \
        ( \
            SELECT t.INSTITUTION_ID, es_teacher.ID teacher_id \
            from \
            ( \
            SELECT INSTITUTION_ID \
            from es_relation_in_dis \
            where DISCIPLINE_CODE in \
                ( \
                    SELECT DISCIPLINE_CODE \
                    from es_relation_in_dis \
                    where INSTITUTION_ID = \
                        ( \
                                SELECT es_institution.ID INSTITUTION_ID \
                                from es_institution \
                                where es_institution.`NAME` = \"" + institution + "\" \
                                and es_institution.SCHOOL_NAME =\"" + school + "\" \
                        ) \
                ) \
            ) t JOIN es_teacher \
            on t.INSTITUTION_ID = es_teacher.INSTITUTION_ID \
        ) t2 JOIN teacher_patent2 \
        on t2.teacher_id = teacher_patent2.teacher_id \
        ) t3 \
        GROUP BY t3.INSTITUTION_ID \
        ) t4 \
        ORDER BY t4.patent_num desc LIMIT 10 \
        ) t5 where t5.institution_id = es_institution.ID;" \
                                                                               ""
        outcome = []
        try:
            res = db.execute(sql)
            print(res)

            for d in res:
                school = d["school_name"]
                institution = d["institution_name"]
                nums = d["patent_num"]
                outcome.append({
                    "x": school,
                    "y": nums,
                    "institution": institution
                })
        except Exception as e:
            print("__!__exception show: ", "there is not ", school, institution, "in mysql")
        # 获取该学院所属学科
        sql2 = "SELECT `NAME` discipline_name\
                from es_discipline \
                where CODE = \
                (SELECT DISCIPLINE_CODE \
                from es_relation_in_dis \
                where INSTITUTION_ID = \
                (select ID institution_id \
                from es_institution \
                where SCHOOL_NAME = \"" + school + "\" and `NAME` = \"" + institution + "\") \
                LIMIT 1 \
                )"
        try:
            discipline = db.execute(sql2)[0]["discipline_name"]
            return outcome, discipline
        except Exception as e:
            print("__!__there is not similar discipline with ", institution)
            return None, None