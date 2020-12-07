from web.extensions import db


class ProjectTaskTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(20), comment="任务名称， 每个中介不一样")
    default_executor = db.Column(db.String(60), comment="默认执行人名称")

    agent_id = db.Column(db.Integer, db.ForeignKey("agent.id"), comment='中介id')
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), comment='项目id')
