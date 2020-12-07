from web.extensions import db


class TeacherForEngineerCommunity(db.Model):
    community_id = db.Column(db.Integer, primary_key=True, comment="工程师社区id")
    teacher_id = db.Column(db.Integer, primary_key=True, comment='教师id')
    school = db.Column(db.String(100), primary_key=True, comment='学校名')
    patent_num = db.Column(db.Integer, comment='此领域下的专利数')
    title = db.Column(db.String(50), comment="院士杰青等头衔")
    teacher_name = db.Column(db.String(255), comment="教师姓名")
    institution = db.Column(db.String(100), comment="学院名")
