from web.extensions import db


class TechnicalRequirement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, comment="同一个文件中技术需求的数量")

    ep_name = db.Column(db.String(100), comment="企业名")
    uploader = db.Column(db.String(100), comment="上传者名字")
    gmt_create = db.Column(db.Integer)
    title = db.Column(db.String(100), comment="企业技术需求")
    partner_unit = db.Column(db.String(100), comment="合作单位")
    # 外键
    agent_id = db.Column(db.Integer, db.ForeignKey("agent.id"))
