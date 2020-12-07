from web.extensions import db


class Enterprise(db.Model):
    id = db.Column(db.Integer, primary_key=True, comment='企业id')
    name = db.Column(db.VARCHAR(100), comment='企业名')
    # 外键
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'))
