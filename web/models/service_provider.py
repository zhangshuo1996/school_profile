from web.extensions import db


class ServiceProvider(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64), comment="服务商")
    charger = db.Column(db.String(64), comment="负责人")
    telephone = db.Column(db.String(64), comment="电话号码")

    status = db.Column(db.Integer, comment="0已删除状态，1合作状态")
    org_code = db.Column(db.String(64), comment="组织结构代码")
    agent_id = db.Column(db.Integer, db.ForeignKey("agent.id"), comment="中介id")
    # 外键
    category_id = db.Column(db.Integer, db.ForeignKey('service_provider_category.id'), comment="类型id, 对应service_provider_category表的主键")
    # 该服务商对应的类型
    category = db.relationship('ServiceProviderCategory')
