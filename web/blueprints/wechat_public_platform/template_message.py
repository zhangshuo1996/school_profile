# 有人入孵或申请参加活动时给管理员发消息
from web.blueprints.wechat_public_platform.task import real_get_access_token
import requests
import datetime
import json
"""
段旭扬open_id :o3Gy00hT3Nhf_szJ7-BZTPusmUA8
"""


def get_template_list():
    """获取模板消息列表"""
    access_token = real_get_access_token()
    url = "https://api.weixin.qq.com/cgi-bin/template/get_all_private_template?access_token=%s" % access_token
    res = requests.get(url)
    print(res.text)


def send_template_message_for_incubator(name, unit, telephone, project_name):
    """
    发送模板消息
    :param name: 姓名
    :param unit: 单位
    :param telephone: 手机号码
    :param project_name: 项目名称
    :return:
    """
    timestamp = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
    remark = "申请人电话为"+str(telephone)+" 项目名称为"+str(project_name)+" 单位为"+str(unit)
    postJson = {"touser": "o3Gy00hT3Nhf_szJ7-BZTPusmUA8", "template_id": "xnIez3bY-jk-QA7yXrCdpYBE-9o1JX0WyVpxehxCmLM",
                "data": {
                    "first": {
                        "value": "入孵申请",
                    },
                    "keyword1": {
                        "value": name,
                    },
                    "keyword2": {
                        "value": "入孵",
                    },
                    "keyword3": {
                        "value": timestamp,
                    },
                    "remark": {
                        "value": remark,
                    }
                }}
    postJson = json.dumps(postJson)
    access_token = real_get_access_token()
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s" % access_token
    postJson = postJson.encode('utf-8')
    r = requests.post(url, data=postJson)
    print(r.text)
    return r.text


def send_template_message_for_signing_up(name, unit, telephone, item_name, category):
    """
    发送模板消息
    :param name: 姓名
    :param unit: 单位
    :param telephone: 手机号码
    :param item_name: 项目名称
    :param category: 类别
    :return:
    """
    timestamp = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
    if category == 1:
        title = "参与活动申请"
        item_type = "活动报名"
    else:
        title = "政策申报申请"
        item_type = "政策申报"
    remark = "申请人电话为" + str(telephone) + " 单位为" + str(unit) + " " + item_type[:2] + "名称为" + str(item_name)
    postJson = {"touser": "o3Gy00hT3Nhf_szJ7-BZTPusmUA8", "template_id": "xnIez3bY-jk-QA7yXrCdpYBE-9o1JX0WyVpxehxCmLM",
                "data": {
                    "first": {
                        "value": title,
                    },
                    "keyword1": {
                        "value": name,
                    },
                    "keyword2": {
                        "value": item_type,
                    },
                    "keyword3": {
                        "value": timestamp,
                    },
                    "remark": {
                        "value": remark,
                    }
                }}
    postJson = json.dumps(postJson)
    access_token = real_get_access_token()
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s" % access_token
    postJson = postJson.encode('utf-8')
    r = requests.post(url, data=postJson)
    print(r.text)
    return r.text


if __name__ == "__main__":
   pass