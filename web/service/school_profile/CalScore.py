"""
学校、学院层面 各个维度进行打分
"""


class CalSchoolScore:
    """
    计算学校层面上的分数
    """

    def cal_school_score_by_discipline(self, discipline_num):
        """
        根据一流学科数量为学校水平打分
        :param discipline_num:
        :return:
        """
        if discipline_num == 0:
            return 50
        elif discipline_num <= 1:
            return 55
        elif discipline_num <= 3:
            return 60
        elif discipline_num <= 6:
            return 70
        elif discipline_num <= 10:
            return 80
        elif discipline_num <= 20:
            return 90
        else:
            return 100

    def cal_achieve_score(self, patent_num):
        """
        学校层面 - 计算成果数量得分
        :param patent_num:
        :return:
        """
        if patent_num > 25000:
            return 100
        elif patent_num > 20000:
            return 90
        elif patent_num > 15000:
            return 80
        elif patent_num > 10000:
            return 70
        elif patent_num > 5000:
            return 60
        return 50

    def cal_researcher_num_score(self, researcher_nums):
        """
        计算研究人员数量得分
        :param researcher_nums:
        :return:
        """
        if researcher_nums > 2500:
            return 100
        elif researcher_nums > 2000:
            return 90
        elif researcher_nums > 1500:
            return 80
        elif researcher_nums > 1000:
            return 70
        elif researcher_nums > 500:
            return 60
        return 50

    def cal_researcher_level_score(self, academician_num, excellent_young):
        """
        计算研究人员水平
        :param academician_num:
        :param excellent_young:
        :return:
        """
        if academician_num >= 10:
            return 100
        elif academician_num > 5:
            return 90
        elif academician_num > 2:
            return 80

        if excellent_young > 50:
            return 100
        if excellent_young > 25:
            return 90
        if excellent_young > 10:
            return 80
        return 70

    def cal_lab_score(self, national_lab_num, province_lab_num):
        """
        计算实验平台得分
        :param national_lab_num: 实验室中的人员数量
        :param province_lab_num:
        :return:
        """
        if national_lab_num >= 2000:
            return 100
        if national_lab_num >= 1500:
            return 90
        if national_lab_num >= 1000:
            return 80
        if national_lab_num >= 500:
            return 70
        return 60

    def cal_project_num_score(self, project_num):
        """
        计算项目数量得分
        :param project_num:
        :return:
        """
        if project_num > 35000:
            return 100
        if project_num > 30000:
            return 90
        if project_num > 25000:
            return 80
        if project_num > 20000:
            return 70
        if project_num > 15000:
            return 60
        return 50


class CalInstitutionScore:
    """
    计算学校层面上的分数
    """

    def cal_school_score_by_discipline(self, discipline_num):
        """
        根据一流学科数量为学校水平打分
        :param discipline_num:
        :return:
        """
        if discipline_num == 0:
            return 50
        elif discipline_num <= 1:
            return 55
        elif discipline_num <= 3:
            return 60
        elif discipline_num <= 6:
            return 70
        elif discipline_num <= 10:
            return 80
        elif discipline_num <= 20:
            return 90
        else:
            return 100

    def cal_achieve_score(self, patent_num):
        """
        学院层面 - 计算成果数量得分
        :param patent_num:
        :return:
        """
        if patent_num > 3500:
            return 100
        elif patent_num > 3000:
            return 90
        elif patent_num > 2500:
            return 80
        elif patent_num > 2000:
            return 70
        elif patent_num > 1000:
            return 60
        return 50

    def cal_researcher_num_score(self, researcher_nums):
        """
        计算研究人员数量得分
        :param researcher_nums:
        :return:
        """
        if researcher_nums > 200:
            return 100
        elif researcher_nums > 150:
            return 90
        elif researcher_nums > 100:
            return 80
        elif researcher_nums > 700:
            return 70
        elif researcher_nums > 50:
            return 60
        return 50

    def cal_researcher_level_score(self, academician_num, excellent_young):
        """
        计算研究人员水平
        :param academician_num:
        :param excellent_young:
        :return:
        """
        if academician_num >= 1:
            return 100

        if excellent_young >= 5:
            return 100
        if excellent_young >= 3:
            return 90
        if excellent_young >= 1:
            return 80
        return 70

    def cal_lab_score(self, national_lab_num, province_lab_num):
        """
        计算实验平台得分
        :param national_lab_num: 实验室中的人员数量
        :param province_lab_num:
        :return:
        """
        if national_lab_num >= 100:
            return 100
        if national_lab_num >= 90:
            return 90
        if national_lab_num >= 70:
            return 80
        if national_lab_num >= 50:
            return 70
        return 60

    def cal_project_num_score(self, project_num):
        """
        计算项目数量得分
        :param project_num:
        :return:
        """
        if project_num > 500:
            return 100
        if project_num > 400:
            return 90
        if project_num > 300:
            return 80
        if project_num > 200:
            return 70
        if project_num > 100:
            return 60
        return 50


class CalTeamScore:
    """
    计算团队层面上的分数
    """

    def cal_school_score_by_discipline(self, discipline_num):
        """
        根据一流学科数量为学校水平打分
        :param discipline_num:
        :return:
        """
        if discipline_num == 0:
            return 50
        elif discipline_num <= 1:
            return 55
        elif discipline_num <= 3:
            return 60
        elif discipline_num <= 6:
            return 70
        elif discipline_num <= 10:
            return 80
        elif discipline_num <= 20:
            return 90
        else:
            return 100

    def cal_achieve_score(self, patent_num):
        """
        学院层面 - 计算成果数量得分
        :param patent_num:
        :return:
        """
        if patent_num > 400:
            return 100
        elif patent_num > 300:
            return 90
        elif patent_num > 200:
            return 80
        elif patent_num > 100:
            return 70
        elif patent_num > 50:
            return 60
        return 50

    def cal_researcher_num_score(self, researcher_nums):
        """
        计算研究人员数量得分
        :param researcher_nums:
        :return:
        """
        if researcher_nums > 30:
            return 100
        elif researcher_nums > 250:
            return 90
        elif researcher_nums > 20:
            return 80
        elif researcher_nums > 15:
            return 70
        elif researcher_nums > 10:
            return 60
        return 50

    def cal_researcher_level_score(self, academician_num, excellent_young):
        """
        计算研究人员水平
        :param academician_num:
        :param excellent_young:
        :return:
        """
        if academician_num >= 1:
            return 100

        if excellent_young >= 5:
            return 100
        if excellent_young >= 3:
            return 90
        if excellent_young >= 1:
            return 80
        return 70

    def cal_lab_score(self, national_lab_num, province_lab_num):
        """
        计算实验平台得分
        :param national_lab_num: 实验室中的人员数量
        :param province_lab_num:
        :return:
        """
        if national_lab_num >= 100:
            return 100
        if national_lab_num >= 90:
            return 90
        if national_lab_num >= 70:
            return 80
        if national_lab_num >= 50:
            return 70
        return 60

    def cal_project_num_score(self, project_num):
        """
        计算项目数量得分
        :param project_num:
        :return:
        """
        if project_num > 500:
            return 100
        if project_num > 400:
            return 90
        if project_num > 300:
            return 80
        if project_num > 200:
            return 70
        if project_num > 100:
            return 60
        return 50