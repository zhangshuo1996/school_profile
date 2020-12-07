from web.extensions import db
from .enterprise import Enterprise
from .project import Project
from web.utils import timestamp2day


class ProjectDeclarationTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, comment="中介id")
    ep_id = db.Column(db.Integer, comment="企业id")

    task_name = db.Column(db.String(64), comment='任务名')
    executor = db.Column(db.String(64), comment='执行人')
    gmt_create = db.Column(db.Integer, comment="任务开始时间")
    gmt_deadline = db.Column(db.Integer, comment="任务截止时间")
    status = db.Column(db.Integer, comment="该任务的状态，0: 待分配， 1：进行中， 2已完成")
    file_id = db.Column(db.Integer, comment="该任务对应的文件id，一个任务只有一个文件")

    distribute_id = db.Column(db.Integer, db.ForeignKey("project_declaration.id"), comment='中介id')

    def get_gmt_create(self):
        return timestamp2day(self.gmt_create)

    def get_gmt_deadline(self):
        return timestamp2day(self.gmt_deadline)
