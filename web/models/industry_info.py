from web.extensions import db


class IndustryInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, comment='行业id')
    code = db.Column(db.Integer, comment='行业code')
    title = db.Column(db.String(255), comment='行业名字')
    patent_num = db.Column(db.Integer, comment='专利数量')
    # engineer_num = db.Column(db.Integer, comment='工程师数量')