from web.extensions import db


class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), comment="孵化器名字（简称）")
    full_name = db.Column(db.String(100), comment="孵化器名字（全称）")
    company = db.Column(db.String(100), comment="运营孵化器的公司")
    pattern = db.Column(db.String(10), comment="经营模式")
    town = db.Column(db.String(10), comment="所在区镇")

    gmt_create = db.Column(db.Integer, comment="创建时间")
    category = db.Column(db.Integer, comment="类别：0：数据平台， 1：孵化器， 2: 众创空间")
    level = db.Column(db.String(30), comment="等级（国家级/省级/市级）")
    area = db.Column(db.Integer, comment="占地面积")
    address = db.Column(db.String(255), comment="孵化器/众创空间 地址")
    lng = db.Column(db.String(32), comment="经度")
    lat = db.Column(db.String(32), comment="纬度")
    is_active = db.Column(db.Integer, comment="标志是否被关注，默认1，表示活跃状态，0表示不活跃")
    avatar = db.Column(db.String(40), comment="头像图片文件名")
    contact_name = db.Column(db.String(64), comment="联系人名称")
    contact_telephone = db.Column(db.String(11), comment="联系人电话")
    # 一个中介对应多个...
    service_providers = db.relationship('ServiceProvider')
    technical_requirements = db.relationship("TechnicalRequirement")
    enterprises = db.relationship('Enterprise')
    project_template = db.relationship('ProjectTaskTemplate')
