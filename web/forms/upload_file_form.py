import time
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import IntegerField, FileField
from wtforms.validators import InputRequired

from web.models import UploadFile
from web.utils.file import save_file
from web.extensions import db


class UploadFileForm(FlaskForm):
    # 限定文件类型 文件类型 1：项目 2：活动 3：政策 4：合同
    category = IntegerField(validators=[InputRequired()])
    match_id = IntegerField(validators=[InputRequired()])
    upload_file = FileField(validators=[FileRequired(), FileAllowed(['jpg', 'png', 'doc', 'docx', 'pdf'], message='文件格式错误')])

    def __init__(self, category=None, match_id=None):
        if category is None or match_id is None:
            super(UploadFileForm, self).__init__()
        else:
            super(UploadFileForm, self).__init__()
            self.category.data = category
            self.match_id.data = match_id

    def add_file(self, uploader):
        """
        添加表单数据到数据库，同时存储文件
        :param uploader: 上传者的id
        :return: True/False
        """
        file = self.upload_file.data
        filename = file.filename
        # TODO:待存储的文件在upload_file下的路径
        path = "files"
        # 保存文件至文件系统，并获取文件名的哈希值
        filename_hash = save_file(path, file)
        # 存储文件记录至数据库
        upload_file = UploadFile(
            category=self.category.data,
            match_id=self.match_id.data,
            uploader=uploader,
            filename=filename,
            path=path,
            filename_hash=filename_hash,
        )
        db.session.add(upload_file)
        db.session.commit()
        return True
