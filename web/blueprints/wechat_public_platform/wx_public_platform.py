from flask import request, send_from_directory, render_template, Blueprint
import os
from web.forms.forms import IncubatorForm, ActivitySignUpForm, PolicySignUpForm
from web.extensions import db
from web.models.wx_public_platform import incubator_project, sign_up
import datetime
import requests
import json
from web.blueprints.wechat_public_platform.template_message import send_template_message_for_incubator, send_template_message_for_signing_up


wx_public_platform_bp = Blueprint("wx_public_platform", __name__)


# 验证服务器
@wx_public_platform_bp.route("/MP_verify_fyLOYxU4R240V5e0.txt")
def download_file():
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    path = os.path.join(basedir, "static")
    print(path)
    return send_from_directory(path, "MP_verify_fyLOYxU4R240V5e0.txt")


@wx_public_platform_bp.route("/get_open_id")
def get_open_id():
    code = request.args.get("code")
    appId = "wxb011e9c49adfb81c"
    appSecret = "8bb5994bb06cc1dc1185f116012c20a1"
    url = '''https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code''' % (
    appId, appSecret, code)
    result = requests.get(url)
    id_dic = json.loads(result.text)
    open_id = id_dic.get("openid")
    print(open_id)
    if open_id is not None:
        return open_id
    else:
        return "未获取到open_id"


@wx_public_platform_bp.route('/incubator/index', methods=['GET', 'POST'])
def incubator_index():
    # 入孵首页
    form = IncubatorForm()
    if form.validate_on_submit():
        name = form.name.data
        telephone = form.telephone.data
        unit = form.unit.data
        project_name = form.project_name.data
        gmt_create = datetime.datetime.now()
        incubator_project_new = incubator_project(name=name, telephone=telephone, unit=unit, project_name=project_name, gmt_create=gmt_create)
        # 给管理员发送消息
        send_template_message_for_incubator(name, unit, telephone, project_name)
        db.session.add(incubator_project_new)
        db.session.commit()
        return render_template('wx_public_platform/incubator_finish.html')
    return render_template('wx_public_platform/incubator_index.html', form=form)


@wx_public_platform_bp.route('/activity/sign_up', methods=['GET', 'POST'])
def activity_sign_up():
    """活动报名"""
    form = ActivitySignUpForm()
    if form.validate_on_submit():
        activity_name = form.activity_name.data
        name = form.name.data
        telephone = form.telephone.data
        unit = form.unit.data
        gmt_create = datetime.datetime.now()
        category = 1
        sign_up_new = sign_up(item_name=activity_name, name=name, telephone=telephone, unit=unit, gmt_create=gmt_create,
                              category=category)
        send_template_message_for_signing_up(name, unit, telephone, activity_name, category)
        db.session.add(sign_up_new)
        db.session.commit()
        return render_template('wx_public_platform/incubator_finish.html')
    return render_template('wx_public_platform/sign_up.html', form=form, category=1)


@wx_public_platform_bp.route('/policy/sign_up', methods=['GET', 'POST'])
def policy_sign_up():
    """政策申报"""
    form = PolicySignUpForm()
    if form.validate_on_submit():
        activity_name = form.activity_name.data
        name = form.name.data
        telephone = form.telephone.data
        unit = form.unit.data
        gmt_create = datetime.datetime.now()
        category = 2
        sign_up_new = sign_up(item_name=activity_name, name=name, telephone=telephone, unit=unit, gmt_create=gmt_create,
                              category=category)
        send_template_message_for_signing_up(name, unit, telephone, activity_name, category)
        db.session.add(sign_up_new)
        db.session.commit()
        return render_template('wx_public_platform/incubator_finish.html')
    return render_template('wx_public_platform/sign_up.html', form=form, category=2)

