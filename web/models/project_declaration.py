import time
from web.extensions import db
from .enterprise import Enterprise
from .project import Project
from .agent import Agent
from web.utils import timestamp2day


class ProjectDeclaration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, comment='中介id')
    progress = db.Column(db.Integer, comment='备忘录，该项目的进度')
    gmt_create = db.Column(db.Integer, default=time.time, comment='创建时间')
    gmt_deadline = db.Column(db.Integer, comment='截止时间')
    start_time = db.Column(db.Integer, comment='项目申报开始时间')
    status = db.Column(db.Integer, comment='该项目的状态，0：进行中，1：已完成，2：已删除')
    uploader = db.Column(db.String(32), comment='上传者名称')

    task_num = db.Column(db.Integer, comment='该项目申报中的任务数量')
    complete_num = db.Column(db.Integer, comment='已完成的任务数量')
    # 外键
    ep_id = db.Column(db.Integer, db.ForeignKey('enterprise.id'), comment='企业id')
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), comment='项目id')

    tasks = db.relationship('ProjectDeclarationTask')

    @property
    def ep_name(self):
        ep = Enterprise.query.filter(Enterprise.id == self.ep_id).first()
        ep_name = ep.name
        return ep_name

    @property
    def project_name(self):
        # project = Project.query.filter(Project.id == self.project_id).first()
        project = Project.query.get(self.project_id)
        return project.name

    @property
    def agent_name(self):
        agent = Agent.query.get(self.agent_id)
        return agent.name

    def get_start_time(self):
        """
        获取“2020-06-22”形式的开始时间
        :return:
        """
        return timestamp2day(self.start_time)

    def get_gmt_deadline(self):
        """
        获取“2020-06-22”形式的截止时间
        :return:
        """
        return timestamp2day(self.gmt_deadline)
