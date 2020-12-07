import re
import random
import string
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from flask import request, redirect, url_for, current_app
from urllib.parse import urlparse, urljoin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

from config import SEND_SMS_CONFIG


TELEPHONE = re.compile(r"^1[3|4|5|6|7|8]\d{9}$")
PASSWORD = re.compile(r"(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,}")


def is_safe_url(target):
    """
    确保内部的URL才是安全的
    :param target:
    :return:
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='main.index', **kwargs):
    """
    重定向
    :param default:
    :param kwargs:
    :return:
    """
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def generate_token(expire_in=None, **kwargs):
    """
    生成令牌
    :param expire_in: 过期时间，默认为1小时
    :param kwargs:
    :return: 返回令牌
    """
    s = Serializer(current_app.config['SECRET_KEY'], expire_in)
    data = {}
    data.update(**kwargs)
    return s.dumps(data)


def get_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
        return data
    except (SignatureExpired, BadSignature) as e:
        return None


def transform_capital(capital):
    """
    将企业注册资金转化为以万元人名币为单位
    by:df
    """
    capital = str(capital)
    if capital.endswith("万元人民币"):
        return capital.replace("万元人民币", "")
    if capital.endswith("万美元"):
        return float(capital.replace("万美元", "")) * 7.0773
    if capital.endswith("万欧元"):
        return float(capital.replace("万欧元", "")) * 7.6619
    if capital.endswith("万日元"):
        return float(capital.replace("万日元", "")) * 0.06657
    elif "万" in capital:
        return capital[0:capital.index("万")]
    else:
        return 0


def generate_random():
    """
    生成四位随机整数验证码
    """
    seeds = string.digits
    random_str = []
    for i in range(4):
        random_str.append(random.choice(seeds))
    return "".join(random_str)


def return_error(error_msg=""):
    """
    返回 dict 格式的报错
    """
    return {"error": True, "errorMsg": error_msg}


def return_flash(message="", category="success"):
    return {"message": message, "category": category}


def is_valid_telephone(telephone):
    """
    检查输入手机号是否合法(11位手机号）
    return: True or False
    """
    if TELEPHONE.match(telephone):
        return True
    return False


def is_valid_password(password):
    """
    检查密码是否合法（最少8位，同时包含数字和字母）
    """
    if PASSWORD.match(password):
        return True
    return False


def replace_sql_inject(name):
    """
    替换sql注入的特殊字符
    :return:
    """
    name = name.replace("\\", "\\\\")
    name = name.replace("\"", "")
    name = name.replace("'", "''")
    name = name.replace(";", "；")
    name = name.replace("delete", "")
    name = name.replace("truncate", "")
    name = name.replace("update", "")
    name = name.replace("insert", "")
    name = name.replace("Exec", "")
    name = name.replace("Execute", "")
    name = name.replace("0x", "0 x")
    return name


def message_api(telephone, verification_code):
    """
    调用阿里云短信服务
    """
    # 服务器的AccessKeyId和AccessKeySecret
    client = AcsClient(SEND_SMS_CONFIG['AccessKeyId'], SEND_SMS_CONFIG['AccessKeySecret'], 'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', str(telephone))
    request.add_query_param('SignName', "三螺旋大数据")
    request.add_query_param('TemplateCode', SEND_SMS_CONFIG['TemplateCode'])
    request.add_query_param('TemplateParam', "{'code':" + verification_code + "}")

    response = client.do_action_with_exception(request)
    return_message = eval(str(response, encoding='utf-8'))
    # print(return_message)
    return return_message["Code"] is "OK"
