from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, HiddenField, StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError, AnyOf, Regexp
from web.utils.url import is_valid_telephone


class LoginForm(FlaskForm):
    telephone = StringField('手机号', validators=[DataRequired()])
    password = PasswordField('密码')
    verification_code = StringField('验证码')
    remember = BooleanField('七天免登陆')
    # 登录类型 该登录必须是password 或者 verification_code
    login_type = HiddenField(validators=[AnyOf(values=['password', 'verification_code'])], default='password')
    submit = SubmitField('登录')

    def validate_telephone(self, field):
        """验证手机号"""
        if is_valid_telephone(field.data) is False:
            raise ValidationError("请输入格式正确的手机号")

    def validate_password(self, field):
        """验证密码"""
        if self.login_type.data == 'password' and len(field.data) == 0:
            raise ValidationError('请输入密码')

    def validate_verification_code(self, field):
        """验证码"""
        if self.login_type.data == 'verification_code' and len(field.data) != 4:
            raise ValidationError('请输入完整的4位验证码')



class WXBindForm(FlaskForm):
    telephone2 = StringField('telephone2', validators=[DataRequired()],
                             render_kw={'class': 'form-control', 'placeholder': "请输入手机号"})
    password = PasswordField('password', validators=[DataRequired(), Length(min=1)],
                             render_kw={'class': 'form-control mb-2', "placeholder": "请输入密码"})
    verification_code = StringField('validate_code', validators=[DataRequired(), Length(min=4, max=4)],
                                    render_kw={'class': 'form-control', "placeholder": "请输入验证码"})
    submit_bind = SubmitField('提交', render_kw={'class': 'form-control btn-block btn btn-primary'})

    def validate_telephone2(self, field):
        if is_valid_telephone(field.data) is False:
            raise ValidationError("请输入格式正确的手机号码")


class PasswordResetForm(FlaskForm):
    telephone = StringField('telephone', validators=[DataRequired()],
                              render_kw={'class': 'form-control', 'placeholder': "请输入手机号"})
    verification_code = StringField('validate_code', validators=[DataRequired(), Length(min=4, max=4)],
                                    render_kw={'class': 'form-control mb-2', "placeholder": "请输入验证码"})
    password_new = PasswordField("password", validators=[DataRequired(), Length(min=8),
                                                         Regexp(regex=r"(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,}",
                                                                flags=0, message="密码至少8位，包含数字和字母")],
                                 render_kw={'class': 'form-control mb-2', "placeholder": "新密码，至少8位，包含数字和字母"})

    submit_btn = SubmitField("确定", render_kw={'class': 'btn btn-lg btn-block btn-primary mb-3'})

    def validate_telephone(self, field):
        if is_valid_telephone(field.data) is False:
            raise ValidationError("请输入格式正确的手机号码")
