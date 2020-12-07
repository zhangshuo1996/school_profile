"""
@author: zs
@date: 2020.2.17
update: 2020.8.17-19
"""
import requests
import json
import sys
import logging
import time
from web.dao.school_profile.patent_dao import PatentDAO
from web.service.school_profile import RelationshipService

sys.path.append("..")
logger = logging.getLogger(__name__)


class PatentSearchService:
    """
    为搜索提供服务
    """
    patent_id_list = []
    distance_list = []
    id_dis_dict = {}
    teacher_patent = []
    teacher_basic_info = None
    patentDao = None
    school = None

    def __init__(self, input_key, school):
        """
        初始化service
        :param input_key:
        :param school:
        """
        # TODO: school 这个参数暂时不使用
        self.school = school
        self.get_ids_by_input(input_key)  # 调用restful服务获得相似的专利id
        self.combine_id_distance()
        self.patentDao = PatentDAO(patent_id_list=self.patent_id_list, school=school)  # 实例化专利数据类
        self.teacher_patent = self.patentDao.return_teacher_patent()  # 获取专利与教师的对应
        self.teacher_basic_info = self.patentDao.get_teacher_basic_info()  # 获取教师的基本信息

    def compose_search_outcome_info(self):
        """
        组合检索结果信息
        :return:
        """
        # 1. 根据获取的teacher_patent信息获取专利对应的著作人信息列表
        patent_id_authors_dict = self.get_patent_author_info()  # { patent_id: [], ... }
        # 2. 获取专利对应的文本
        patent_id_text_dict = self.get_patent_text_info()  # {patent_id: {"patent_name": patent_name, "patent_text": patent_text}}
        # 3. 获取专利对应著作人所在的团队
        patent_id_team_id_list = self.get_team_info_by_authors(patent_id_authors_dict)
        # 4. 获取著作人所在的学院 done

        # 5. 获取这些著作人的项目信息
        patent_id_projects_dict = self.get_project_info_by_teacher_ids(patent_id_authors_dict)

        # 6. 按照检索的顺序 求的 该学校中 相似专利的id列表
        sorted_patent_id_list = []
        for patent_id, dist in self.id_dis_dict.items():
            if patent_id in patent_id_authors_dict.keys():
                sorted_patent_id_list.append(patent_id)

        return {
            "sorted_patent_id_list": sorted_patent_id_list,
            "patent_id_authors_dict": patent_id_authors_dict,
            "patent_id_text_dict": patent_id_text_dict,
            "patent_id_team_id_list": patent_id_team_id_list,
            "patent_id_projects_dict": patent_id_projects_dict,
            "teacher_base_info": self.teacher_basic_info
        }

    def get_patent_author_info(self):
        """
        根据获取的teacher_patent信息获取专利对应的作者信息
        :return: {
                    patent_id: [teacher_name1, .. ]
                }
        """
        patent_id_authors_dict = {}
        for dic in self.teacher_patent:
            patent_id = dic["patent_id"]
            teacher_id = dic["teacher_id"]
            if patent_id in patent_id_authors_dict.keys():
                patent_id_authors_dict[patent_id].append(teacher_id)
            else:
                patent_id_authors_dict[patent_id] = [teacher_id]
        return patent_id_authors_dict

    def get_patent_text_info(self):
        """
        根即获取的teacher_patent信息获取专利对应的文本信息
        :return: {patent_id: {"patent_name": patent_name, "patent_text": patent_text}}
        """
        patent_id_text_dict = {}
        for dic in self.teacher_patent:
            patent_id = dic["patent_id"]
            patent_name = dic["patent_name"]
            patent_text = dic["summary"]
            if patent_id not in patent_id_text_dict.keys():
                patent_id_text_dict[patent_id] = {
                    "patent_name": patent_name,
                    "patent_text": patent_text
                }
        return patent_id_text_dict

    def get_team_info_by_authors(self, patent_id_authors_dict):
        """
        根即teacher_id 获取该专家坐在的团队id， 并组成对应patent_id_authors_dict的列表
        :return: {patent_id: team_id, ...}
        """
        teacher_ids = []
        # 1. 将搜索结果中专利对应的专家id组成列表
        for patent_id, id_list in patent_id_authors_dict.items():
            teacher_ids.extend(id_list)
        # 2. 获取这些专家对应的团队， 组成{teacher_id: team_id}
        teacher_team_list = RelationshipService.get_team_ids_by_teacher_ids(teacher_ids)
        teacher_id_team_id_dict = {}
        for dic in teacher_team_list:
            teacher_id = dic["teacher.id"]
            team_id = dic["teacher.team"]
            if team_id is not None:
                teacher_id_team_id_dict[teacher_id] = team_id
        # 3. 按照patent_id_authors_dict中的顺序，找到该专利著作人所在的团队
        patent_id_team_id_dict = {}
        for patent_id, id_list in patent_id_authors_dict.items():
            temp_team_id_freq = {}
            for teacher_id in id_list:
                if teacher_id not in teacher_id_team_id_dict.keys():
                    continue
                team_id = teacher_id_team_id_dict[teacher_id]
                if team_id in temp_team_id_freq.keys():
                    temp_team_id_freq[team_id] += 1
                else:
                    temp_team_id_freq[team_id] = 1
            sorted_tup_list = sorted(temp_team_id_freq.items(), key=lambda x: x[1], reverse=True)
            if len(sorted_tup_list) == 0:
                continue
            team_id = sorted_tup_list[0][0]
            patent_id_team_id_dict[patent_id] = team_id
        return patent_id_team_id_dict

    def get_org_info_by_teacher_id(self):
        """
        根即teacher_patent 信息获取 teacher_id 所在的学院信息及实验室信息
        :return:
        """
        teacher_id_org_dict = {}
        for dic in self.teacher_patent:
            teacher_id = dic["teacher_id"]
            institution = self.teacher_basic_info[teacher_id]["institution"]
            lab = self.teacher_basic_info[teacher_id]["lab"]
            teacher_id_org_dict[teacher_id] = {
                "institution": institution,
                "lab": lab
            }
        return teacher_id_org_dict

    def get_project_info_by_teacher_ids(self, patent_id_authors_dict):
        """
        根即teacher_ids获取这些专家对应的成果
        :return: {teacher_id: [project_name1, project_name2, ...]}
        """
        # 获取项目的信息，并将老师对应的项目信息添加到对应的字典中
        project_info = self.patentDao.get_teacher_project_info()
        teacher_id_project_list_dict = {}
        for dic in project_info:
            teacher_id = dic["teacher_id"]
            project_name = dic["project_name"]
            if teacher_id in teacher_id_project_list_dict.keys():
                teacher_id_project_list_dict[teacher_id].append(project_name)
            else:
                teacher_id_project_list_dict[teacher_id] = [project_name]
        patent_id_projects_dict = {}
        for patent_id, id_list in patent_id_authors_dict.items():
            this_project_list = []
            for teacher_id in id_list:
                if teacher_id in teacher_id_project_list_dict.keys():
                    this_project_list.extend(teacher_id_project_list_dict[teacher_id])
            this_project_list = list(set(this_project_list))  # 去除重复项目
            patent_id_projects_dict[patent_id] = this_project_list
        return patent_id_projects_dict

    def get_patent_info(self):
        """
        获取patent_id为键， 专利名为值的字典
        :return:
        """
        patent_info = {}
        for dic in self.teacher_patent:
            patent_id = dic["patent_id"]
            patent_name = dic["patent_name"]
            publication_number = dic["publication_number"]
            summary = dic["summary"]
            patent_info[patent_id] = (patent_name, publication_number, summary)
        return patent_info

    def get_ids_by_input(self, input_key):
        """
        根据用户的输入内容, 通过调用restful服务获取与之相关的成果id
        :return:
        """
        start = time.time()
        data = {"K": 300, "key": input_key}
        url = "http://39.100.224.138:8777/search"
        data_json = json.dumps(data)
        headers = {'Content-type': 'application/json'}
        response = requests.post(url, data=data_json, headers=headers)
        i_string = eval(response.text)["I"]  # 返回的成果ID列表（字符串形式）
        d_string = eval(response.text)["D"]  # 返回的成果距离列表 （字符串形式）
        i_list = eval(i_string)
        d_list = eval(d_string)
        logging.warning('-----------------------------------get_ids_by_input--相似成果id获取成功-----------------------------------')

        self.patent_id_list = i_list[0]
        self.distance_list = d_list[0]
        end = time.time()
        logging.warning("faiss 检索时间  " + str(end-start))

    def combine_id_distance(self):
        """
        将patent_id列表与distance列表组合成字典
        :return: {id1: dis1, id2: dis2, ...}
        """
        for i in range(len(self.patent_id_list)):
            if self.patent_id_list[i] not in self.id_dis_dict.keys():
                self.id_dis_dict[self.patent_id_list[i]] = self.distance_list[i]

    def get_this_teacher_patents(self):
        """
        获取某一个教师的专利 --> {teacher_id1: [patent_id1, patent_id2],}
        :return:
        """
        teacher_all_patent = {}
        teacher_patent = self.teacher_patent
        for d in teacher_patent:
            teacher_id = d["teacher_id"]
            patent_id = d["patent_id"]
            if teacher_id not in teacher_all_patent.keys():
                teacher_all_patent[teacher_id] = [patent_id]
            else:
                tmp_list = teacher_all_patent[teacher_id]
                tmp_list.append(patent_id)
                teacher_all_patent[teacher_id] = tmp_list
        return teacher_all_patent

    def cal_teacher_patent_dist(self, teacher_all_patent):
        """
        计算每一教师对应所有成果相似度的平均距离和最小距离
        :return:
        """
        teacher_avg_min = {}
        for teacher_id in teacher_all_patent:
            sum_dis = 0
            min_dis = 100000000
            for paper_id in teacher_all_patent[teacher_id]:
                sum_dis += self.id_dis_dict[paper_id]
                min_dis = min(min_dis, self.id_dis_dict[paper_id])
            dis_avg = sum_dis / len(teacher_all_patent[teacher_id])
            teacher_avg_min[teacher_id] = (dis_avg, min_dis)
        return teacher_avg_min

    def construct_teacher_in_res(self):
        """
        构造位于返回结果中的教师的信息
        {
            "team_list": [
                {
                    team_id1: {"team_id": **, "school": *, "institution": * "lab": *, "member_id_list": , "patent_list": *, "project_list"}
                }, ...
            ],
            "teacher_base_info":{
                teacher_id: {"lab": *, "institution": *, "school': "title": *, "name": *, "achieve_nums": *, "patent_list": *, "project_list"},
                .....
            }
            "patent_info": {
                patent_id: (patent_name, publication_number),
                ....
            },
            "school_proportion":{
                "legend": [school1, school2, ...],
                "series": [{"name": school1, 'value': 7}],  value 是该学校拥有的相似成果的数量
                "seriesName": "学校数量占比"
            }
        }
        :return:
        """
        logging.info("-------------------------------------construct_teacher_in_res----------------------------------")
        # 1. find 专家对应的所有成果 --> {teacher_id1: [patent_id1, patent_id2],}
        teacher_all_patent = self.get_this_teacher_patents()

        for teacher_id in self.teacher_basic_info.keys():
            self.teacher_basic_info[teacher_id]["achieve_nums"] = len(teacher_all_patent[teacher_id])
            self.teacher_basic_info[teacher_id]["patent_list"] = self.get_patent_by_teacher_id(teacher_id)

        # 3. 获取项目的信息，并将老师对应的项目信息添加到对应的字典中
        project_info = self.patentDao.get_teacher_project_info()
        for dic in project_info:
            teacher_id = dic["teacher_id"]
            if "project_list" in self.teacher_basic_info[teacher_id].keys():
                self.teacher_basic_info[teacher_id]["project_list"].append(dic["project_name"])
            else:
                self.teacher_basic_info[teacher_id]["project_list"] = [dic["project_name"]]

        team_list = self.construct_team_info()
        school_proportion = self.get_school_proportion(team_list)  # 获取每个学校的相似成果个数
        return {"team_list": team_list, "teacher_basic_info": self.teacher_basic_info, "patent_info": self.get_patent_info(), "school_proportion": school_proportion}

    def get_school_proportion(self, team_list):
        """
        获取搜索结果中各个学校对应的专利数量
        :return:
        """
        school_patent_num = {}
        school_set = {0}
        for dic in team_list:
            school = dic["school"]
            nums = dic["achieve_nums"]
            if school in school_patent_num.keys():
                school_patent_num[school] += nums
            else:
                school_set.add(school)
                school_patent_num[school] = nums
        school_set.remove(0)
        data = [{"name": school, "value": nums} for school, nums in school_patent_num.items()]
        return {
            "legend": list(school_set),
            "series": data,
            "seriesName": "学校数量占比"
        }

    def get_patent_by_teacher_id(self, teacher_id):
        """
        根据teacher_id 从teacher_patent中获取搜索结果中该教师的专利列表
        :param teacher_id:
        :return:
        """
        return_list = []  # 该教师对应的专利列表
        for d in self.teacher_patent:
            if teacher_id == d["teacher_id"]:
                return_list.append({
                    "patent_name": d["patent_name"],
                    "patent_id": d["patent_id"]
                })
        return return_list

    def get_teacher_team(self, teacher_id_list):
        """
        获取搜索到的教师列表中的团队
        :return: {
            team_id1: {"member_id_list":[t1_id, t2_id], ...},
            ...
        }
        """

        teacher_team_list = RelationshipService.get_team_ids_by_teacher_ids(teacher_id_list)  # [{"teacher.team": team_id, "teacher.id": t_id}, ...]
        team = {}
        no_team_list = []
        for dic in teacher_team_list:
            team_id = dic["teacher.team"]
            teacher_id = dic["teacher.id"]
            if team_id is None:  # 该教师没有团队
                no_team_list.append(teacher_id)
                continue
            if team_id in team.keys():
                team[team_id]["member_id_list"].append(teacher_id)
            else:
                team[team_id] = {"member_id_list": [teacher_id], "team_id": team_id}
        # TODO: no_team的如何处理？？
        return team

    def compose_teacher_id_list(self):
        """
        从[{"teacher_id": **, "teacher_name": **, "patent_id": **, ..}, {..}, ..]中提取出teacher_id_list
        :return: [t1_id, t2_id, ...]
        """
        teacher_list = self.teacher_patent
        teacher_id_list = []
        for teacher in teacher_list:
            teacher_id = teacher["teacher_id"]
            teacher_id_list.append(teacher_id)
        return teacher_id_list

    def construct_team_info(self):
        """
        获取该团队的相关信息，通过团队中的每个人相应信息出现的频次
        相关信息包括： 所在学校；所在学院；依托平台；工程技术中心（可能没有）
        :return:
        """
        teacher_id_list = self.compose_teacher_id_list()
        team_dict = self.get_teacher_team(teacher_id_list)
        team_dict = self.cal_team_org(team_dict)  # 计算团队所在的组织（学校/学院）以及拥有的平台（实验室）
        team_dict = self.cal_team_similar_patent_list(team_dict)  # 获取该团队拥有的相似专利列表， 添加到对应的team
        team_dict = self.cal_team_project_info(team_dict)  # 计算该团队拥有的项目信息，添加到对应的team
        team_list = self.cal_composite_score(team_dict)
        return team_list

    def cal_composite_score(self, team_dict):
        """
        计算每个团队的综合分数，并排序
        目前分数计算 直接使用该团队的相似成果数量
        :param team_dict:
        :return:
        """
        for team_id in team_dict.keys():
            # TODO: 更改计算分数
            team_dict[team_id]["score"] = team_dict[team_id]["achieve_nums"]
        team_list = [team_dict[team_id] for team_id in team_dict.keys()]  # 字典转成列表
        team_list = sorted(team_list, key=lambda e: e["score"], reverse=True)
        return team_list

    def cal_team_similar_patent_list(self, team_dict):
        """
        计算该团队所拥有的相似专利列表
        :return:
        """
        for team_id in team_dict.keys():
            teacher_id_list = team_dict[team_id]["member_id_list"]
            patent_set = {0}
            for teacher_id in teacher_id_list:
                patent_list = self.teacher_basic_info[teacher_id]["patent_list"]
                for patent in patent_list:
                    patent_id = patent["patent_id"]
                    patent_set.add(patent_id)
            patent_set.remove(0)
            team_dict[team_id]["patent_id_list"] = list(patent_set)
            team_dict[team_id]["achieve_nums"] = len(list(patent_set))
        return team_dict

    def cal_team_org(self, team_dict):
        """
        计算团队所在的组织（学校/学院）以及拥有的平台（实验室）
        :return:
        """
        # 获取多个教师的基本信息
        teacher_basic_info = self.teacher_basic_info

        for team_id, info in team_dict.items():
            # 对于每一个团队，获取团队中的每个成员的学校 学院 实验室信息，计算出现的频次，取频次最高的作为该团队的相应标识
            school_dict = {}
            institution_dict = {}
            lab_dict = {}
            for teacher_id in info["member_id_list"]:
                school = teacher_basic_info[teacher_id]["school"]
                institution = teacher_basic_info[teacher_id]["institution"]
                lab = teacher_basic_info[teacher_id]["lab"]
                if school is not None and school != "":
                    if school in school_dict.keys():
                        school_dict[school] += 1
                    else:
                        school_dict[school] = 1

                if institution is not None and school != "":
                    if institution in institution_dict.keys():
                        institution_dict[institution] += 1
                    else:
                        institution_dict[institution] = 1

                if lab is not None and school != "":
                    if lab in lab_dict.keys():
                        lab_dict[lab] += 1
                    else:
                        lab_dict[lab] = 1
            school = self.get_max_value_key(school_dict)
            institution = self.get_max_value_key(institution_dict)
            lab = self.get_max_value_key(lab_dict)
            team_dict[team_id]["school"] = school
            team_dict[team_id]["institution"] = institution
            team_dict[team_id]["lab"] = lab
        return team_dict

    def cal_team_project_info(self, team_dict):
        """
        计算一个团队内的项目信息
        :return:
        """
        for team_id in team_dict.keys():
            teacher_id_list = team_dict[team_id]["member_id_list"]
            project_set = {0}
            for teacher_id in teacher_id_list:
                if "project_list" not in self.teacher_basic_info[teacher_id].keys():  # 该教师没有项目
                    continue
                project_list = self.teacher_basic_info[teacher_id]["project_list"]
                for project in project_list:
                    project_set.add(project)
            project_set.remove(0)
            team_dict[team_id]["project_list"] = list(project_set)
        return team_dict

    def get_max_value_key(self, _dict):
        """
        获取字典中最大值对应的键，并返回该键
        :return:
        """
        max_times = 0
        key = ""
        for temp_key, _times in _dict.items():
            if max_times < _times:
                key = temp_key
                max_times = _times
        return key

    # def get_search_history(self):
    #     """
    #     获取历史搜索记录
    #     :return:
    #     """
    #     result = self.patentDao.get_search_history()
    #     return result


if __name__ == '__main__':
    s = PatentSearchService("空调系统")
    s.construct_teacher_in_res()
