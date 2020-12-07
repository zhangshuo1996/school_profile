import time

from web.extensions import db


class UploadFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Integer, comment='文件类型 1：项目 2：活动 3：政策 4：合同')
    match_id = db.Column(db.Integer, comment='文件对应的项目id或活动id')
    uploader = db.Column(db.String(32), comment='文件上传者')
    filename = db.Column(db.String(255), comment='文件名')
    path = db.Column(db.String(255), comment='文件相对路径')
    filename_hash = db.Column(db.String(64), comment='混编文件名')
    gmt_create = db.Column(db.Integer, comment='文件上传时间', default=time.time)

