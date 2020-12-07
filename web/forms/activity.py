import time
import datetime
from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms import StringField, SelectField, SubmitField, HiddenField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, Length

from web.extensions import db
from ._validator import date_picker
from web.models import Activity, User


def _text2timestamp(text):
    obj = time.strptime(text, '%Y-%m-%d %H:%M')
    timestamp = time.mktime(obj)
    return timestamp


def _timestamp2text(timestamp):
    """时间戳转换成字符串, 类似mysql的from_unixtime操作"""
    obj = time.localtime(timestamp)
    text = time.strftime('%Y-%m-%d %H:%M', obj)
    return text


class ActivityForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(max=255)])
    project = SelectField('项目', coerce=int)
    start_time = StringField('', validators=[date_picker])
    end_time = StringField('', validators=[date_picker])
    address = StringField('地址', validators=[DataRequired(), Length(max=255)])
    # description = TextAreaField('简介', validators=[DataRequired()])
    description = CKEditorField('简介', validators=[DataRequired()])
    submit = SubmitField('提交')
    activity_id = HiddenField()

    def __init__(self, projects, start_time=None, activity=None):
        super(ActivityForm, self).__init__()
        # 填充project
        self.project.choices = [(project.id, project.name) for project in projects]
        # 开始时间
        if start_time:
            now = datetime.datetime.today().strftime("%Y-%m-%d") + " 08:00"
            start_time = now if start_time < now else start_time + " 08:00"
            self.start_time.data = start_time
        # 填充数据
        if activity:
            self.project.data = activity.project_id
            self.title.data = activity.title
            self.start_time.data = _timestamp2text(activity.gmt_start)
            self.end_time.data = _timestamp2text(activity.gmt_end)
            self.address.data = activity.address
            self.description.data = activity.description

    def validate_start_time(self, field):
        """开始时间不能晚于结束时间"""
        if field.data > self.end_time.data:
            raise ValidationError('开始时间不能晚于结束时间')

    def add_activity(self, user: User):
        # 由ActivityForm => Activity，并插入数据库
        activity = Activity(user_id=user.id,
                            user_name=user.name,
                            sponsor_id=user.org_id,
                            sponsor_name=user.org_name,
                            title=self.title.data,
                            gmt_start=_text2timestamp(self.start_time.data),
                            gmt_end=_text2timestamp(self.end_time.data),
                            address=self.address.data,
                            description=self.description.data,
                            project_id=self.project.data)
        db.session.add(activity)
        db.session.commit()
        return activity

    def update_activity(self, activity):
        activity.title = self.title.data
        activity.gmt_start = _text2timestamp(self.start_time.data)
        activity.gmt_end = _text2timestamp(self.end_time.data)
        activity.address = self.address.data
        activity.description = self.description.data
        activity.project_id = self.project.data
        db.session.add(activity)
        db.session.commit()
        return activity
