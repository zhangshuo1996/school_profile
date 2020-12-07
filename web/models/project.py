from web.extensions import db


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.VARCHAR(255), comment='项目全称')
    name = db.Column(db.VARCHAR(255), comment='项目简称')
    cover_image = db.Column(db.VARCHAR(66), comment='项目背景图片')
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"), comment='选择的部门id')

    project_templates = db.relationship('ProjectTaskTemplate')
    department = db.relationship('Department', uselist=False)
    # 项目完成的结果
    project_result = db.relationship('ProjectResult')
