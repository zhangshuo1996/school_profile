from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from flask_login import current_user, login_user, logout_user

from web.models import User
from web.extensions import db
from web.service import auth as auth_service
from web.forms import WXBindForm, LoginForm, PasswordResetForm
from werkzeug.security import generate_password_hash
from web.utils.url import redirect_back, generate_random, get_token, generate_token, message_api

auth_bp = Blueprint("auth", __name__)


@auth_bp.route('/', methods=['GET'])
def index():
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    """处理用户登录的get请求，展示登录页面"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    # 处理微信登录
    is_wechat_login, openid, user = auth_service.wechat_login(request.args.get('next'))
    if is_wechat_login:
        if openid is None:
            flash('未获取到微信认证信息，请重试', 'danger')
        elif user is None:  # 未绑定用户
            flash('未绑定用户，请绑定用户', 'info')
            return redirect(url_for("auth.login_bind", openid=openid))
        else:
            login_user(user)
            return redirect(url_for('main.index'))
    # 处理正常登录
    form = LoginForm()
    if form.validate_on_submit():
        remember = form.remember.data
        user = auth_service.login(form)
        if user is None:  # user为空
            flash('用户不存在', 'danger')
        elif user is False:  # 登录失败
            if form.login_type.data == 'password':
                flash("账号或密码输入有误", "danger")
            else:
                flash('账号或验证码输入有误', 'danger')
        else:  # 登录成功
            login_user(user, remember)
            return redirect_back('main.index')
    auth_service.transform_errors_to_flash(form)
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/get_verification_code', methods=['POST'])
def get_validate_code():
    """获取验证码"""
    ret = {}
    telephone = request.form.get('telephone')
    code = generate_random()
    # print(code)
    # 保存验证码到session中
    session['verification_code'] = generate_token(expire_in=360, code=code)
    return_code = message_api(telephone, code)
    ret['status'] = 'ok' if return_code else 'error'
    return jsonify(ret)


@auth_bp.route("/login_bind", methods=["GET", "POST"])
def login_bind():
    """验证账号、密码、验证码，并将openid绑定到对应用户信息上"""
    openid = request.args.get("openid")
    form = WXBindForm()
    if form.validate_on_submit():
        telephone = form.telephone2.data
        password = form.password.data
        user_verification_code = form.verification_code.data
        if 'verification_code' in session:
            data = get_token(session['verification_code'])
            if data and 'code' in data and data['code'] == user_verification_code:
                if 'verification_code' in session:
                    session.pop('verification_code')
                user = User.query.filter_by(telephone=telephone).first()
                if user is None:
                    flash('无此用户', 'danger')
                    redirect_back()
                elif user.validate_password(password):
                    user.open_id = openid
                    db.session.commit()
                    login_user(user)
                    return redirect(url_for('main.index'))
                else:
                    flash("账号或密码错误", "danger")
                    return redirect_back()
        flash('验证码错误', 'danger')
        return redirect_back()
    return render_template("auth/bind_telephone.html", form=form)


@auth_bp.route("/password_reset", methods=['GET', "POST"])
def password_reset():
    reset_form = PasswordResetForm()
    if reset_form.validate_on_submit():
        telephone = reset_form.telephone.data  # telephone2:短信验证码发送时的手机号
        code = reset_form.verification_code.data
        new_password = reset_form.password_new.data

        t = current_user
        user = User.query.filter_by(telephone=telephone).first()
        if user is None:
            flash('账号不正确', 'danger')
        if 'verification_code' in session:
            data = get_token(session['verification_code'])
            if data and 'code' in data and data['code'] == code:
                session.pop('verification_code')
                current_user.password_hash = generate_password_hash(new_password)
                db.session.commit()
                return logout()
            else:
                flash("验证码错误", "danger")
        else:
            flash("请先获取验证码", "danger")
    return render_template("auth/password_reset.html", reset_form=reset_form)
