# import json
# import requests
# from flask import session, flash
# from urllib.parse import parse_qs
#
# # from web.models import User
# from web.utils.url import get_token
# from web.forms import LoginForm
# from config import WX_CONFIG
#
#
# def login(form: LoginForm):
#     """
#     验证是否登录成功
#     :return: None 用户不存在 False 登录失败 User对象，登录成功
#     """
#     user = User.query.filter(User.telephone == form.telephone.data, User.is_active == 1).first()
#     # 用户不存在
#     if user is None:
#         return None
#     # 密码登录
#     if form.login_type.data == 'password' and user.validate_password(form.password.data):
#         return user
#     # 验证码登录
#     elif form.login_type.data == 'verification_code' and 'verification_code' in session:
#         data = get_token(session['verification_code'])
#         if data and 'code' in data and form.verification_code.data == data['code']:
#             session.pop('verification_code')
#             return user
#     # 登录失败
#     return False
#
#
# def wechat_login(next_):
#     """
#     处理微信登录
#     :param next_:
#     :return: 返回(bool,open_id,user) bool 是否使用微信登录 open_id是None的时候，微信未找到该用户; user可能是None或user对象
#     """
#     dic = parse_qs(next_)
#     code_list = dic.get('/?code')
#     code = None
#     if code_list is not None and len(code_list) > 0:
#         code = code_list[0]
#     # 确实是微信登录
#     if code is not None:
#         openid = get_access_token_url(code)
#         print(openid)
#         # 未从微信获取到openid
#         if openid is None:
#             return True, None, None
#         user = User.query.filter_by(open_id=openid).first()
#         # 未绑定用户
#         if user is None:
#             return True, openid, None
#         # 已经绑定了用户
#         return True, openid, user
#     return False, None, None
#
#
# def get_access_token_url(code):
#     """由code到微信服务器获取用户唯一标识opid"""
#     AppID = WX_CONFIG.get("AppID")
#     AppSecret = WX_CONFIG.get("AppSecret")
#     url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code"%(AppID, AppSecret, code)
#     r = requests.get(url)
#     dic = json.loads(r.text)
#     return dic.get("openid")
#
#
# def transform_errors_to_flash(form, one=True):
#     """把form的产生的错误发送给flash"""
#     if form.errors:
#         for field, errors in form.errors.items():
#             flash(errors[0], 'danger')
#             if one:
#                 break
