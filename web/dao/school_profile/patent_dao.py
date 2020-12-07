from web.utils import db
import logging


class PatentDAO:

    teacher_patent = []

    def __init__(self, patent_id_list, school):
        """

        """
        self.get_teacher_patent(patent_id_list, school)

    def return_teacher_patent(self):
        """
        :return:
        """
        return self.teacher_patent

    def get_teacher_patent(self, patent_id_list, school):
        """
        根据获取的专利id得到对应的教师id,以及专利名,及其专利公开号
        :return:
            [
                {
                    "teacher_id": 11,
                    "patent_id": 11,
                    "patent_name":
                }
            ]
        """
        sql = """
            select i.id teacher_id, i.name teacher_name, p.id patent_id, p.title patent_name, s.id school_id, s.name school_name, p.publication_number, pt.summary
            from clean_inventor i
            LEFT JOIN clean_inventor_patent ip
            on i.id = ip.inventor_id
            LEFT JOIN patent p
            on ip.patent_id = p.id
            left join patent_text pt 
            on pt.patent_id = p.id
            LEFT JOIN school s
            on i.school_id = s.id
            where p.id in (
        """
        # 上面sql中的s.name = school 条件用于只取某一学校的成果
        teacher_patent = []
        get_patent_num = 20  # 一次获取专利的数量
        i = 0
        if len(patent_id_list) != 0:
            for patent_id in patent_id_list:
                if i > get_patent_num:
                    break
                sql += str(patent_id) + ","
                i += 1
            sql = sql[0:-1]
            sql += ")"
            logging.warning("-----获取专利信息----" + sql)
            teacher_patent = db.select(sql, {"school": school}, bind='data_mining')
        self.teacher_patent = teacher_patent

    def get_teacher_basic_info(self):
        """
        根据教师的多个id  (id1, id2, ...)
        获取教师的基本信息
        :return: {id1: {"school": school,
                        "institution": institution,
                        "school_id": school_id,
                        "institution_id": institution_id,
                        "lab": lab,
                        "name": name,
                        "title": title
                        },
                 id2: {..
                        }
                    ...
                }
        """
        logging.warn("-------------------------------------get_teacher_basic_info----------------------------------")
        teacher_patent = self.teacher_patent
        if len(teacher_patent) == 0:
            return {}
        sql = """
            select i.id teacher_id, i.name  name, s.name school, s.id school_id, i.lab,
            i.institution institution, "教授" title, 111 institution_id
            from clean_inventor i
            LEFT JOIN school s
            on i.school_id = s.id
            where i.id in (
        """
        for d in teacher_patent:
            teacher_id = d["teacher_id"]
            sql += str(teacher_id) + ","
        sql = sql[0:-1]
        sql += ")"
        logging.warning("-----获取专家信息----" + sql)
        res = db.select(sql, bind='data_mining')
        teacher_basic_info = {}
        for d in list(res):
            tmp_dict = {
                "school": d["school"],
                "lab": d["lab"],
                "institution": d["institution"],
                "name": d["name"],
                "school_id": d["school_id"],
                "institution_id": d["institution_id"],
                "title": d["title"]
            }
            teacher_basic_info[d["teacher_id"]] = tmp_dict
        return teacher_basic_info

    def get_teacher_project_info(self):
        """
        获取该专家对应的项目信息
        :return: [{"teacher_id": **, "project_name": **}]
        """
        sql = """
            select p.teacher_id, p.name project_name
            from funds p
            where p.category = 1 and p.teacher_id in (
        """
        if len(self.teacher_patent) == 0:
            return []
        for d in self.teacher_patent:
            teacher_id = d["teacher_id"]
            sql += str(teacher_id) + ","
        sql = sql[0:-1]
        sql += ")"
        logging.warning("-----获取项目信息----" + sql)
        result = db.select(sql, bind='data_mining')
        return result

    def get_search_history(self):
        """
        获取历史搜索记录
        :return:
        """
        sql = """
            select search_text, gmt_create
            from search_history
            limit 5
        """
        return db.select(sql, bind='data_mining')
