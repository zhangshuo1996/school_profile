from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, Length


class IncubatorForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired()])
    # sex = SelectField('性别', validators=[DataRequired()], choices = [(1, '男'), (2, '女')],coerce=int)
    telephone = StringField('手机号码', validators=[DataRequired(), Length(11, 11)])
    unit = StringField('单位', validators=[DataRequired()])
    project_name = StringField('项目名称', validators=[DataRequired()])
    submit = SubmitField('提交')


class ActivitySignUpForm(FlaskForm):
    activity_name = StringField('活动名称', validators=[DataRequired()])
    name = StringField('姓名', validators=[DataRequired()])
    telephone = StringField('手机号码', validators=[DataRequired(), Length(11, 11)])
    unit = StringField('单位', validators=[DataRequired()])
    submit = SubmitField('提交')


class PolicySignUpForm(FlaskForm):
    activity_name = StringField('政策名称', validators=[DataRequired()])
    name = StringField('姓名', validators=[DataRequired()])
    telephone = StringField('手机号码', validators=[DataRequired(), Length(11, 11)])
    unit = StringField('单位', validators=[DataRequired()])
    submit = SubmitField('提交')
