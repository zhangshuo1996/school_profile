# 设置自定义菜单
import requests
from web.blueprints.wechat_public_platform.task import real_get_access_token
import urllib.parse
import json


def create(postData, accessToken):
    postUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % accessToken
    postData = postData.encode('utf-8')
    r = requests.post(postUrl, data=postData)
    print(r.text)


def get_url_encode():
    # 进行urlEncode
    url = "http://wx.3luoxuan.com/"
    data = urllib.parse.quote(url)
    print(data)


def set_menu_for_getting_open_id():
    """改变自定义菜单，使得点击获取用户open_id"""
    # encode编码 http://tool.chinaz.com/tools/urlencode.aspx
    postJson = """
    {
        "button":
        [
                {
                    "type": "view",
                    "name": "点击获取open_id",
                    "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxb011e9c49adfb81c&redirect_uri=http%3A%2F%2Fwx.3luoxuan.com%2F&response_type=code&scope=snsapi_base&state=123#wechat_redirect"
                },
        ]
    }
    """
    accessToken = real_get_access_token()
    create(postJson, accessToken)


def query(accessToken):
    postUrl = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s" % accessToken
    r = requests.get(postUrl)
    print(r.text)


def delete(accessToken):
    postUrl = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % accessToken
    r = requests.get(postUrl)
    print(r.text)


# 获取自定义菜单配置接口
def get_current_selfmenu_info(accessToken):
    postUrl = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=%s" % accessToken
    r = requests.get(url=postUrl)
    print(r.text)


# 获取用户列表
def get_user_list():
    access_token = real_get_access_token()
    url = "https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s"%access_token
    r = requests.get(url)
    open_id_dic = json.loads(r.text)
    for open_id in open_id_dic.get("data").get("openid"):
        get_user_info_by_open_id(open_id)


# 由open_id获取用户信息
def get_user_info_by_open_id(open_id):
    access_token = real_get_access_token()
    url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN"%(access_token, open_id)
    r = requests.get(url)
    print(r.text)


if __name__ == '__main__':
    postJson = """
    {
        "button":
        [
                {
                    "type": "view",
                    "name": "入孵申请",
                    "url": "http://wx.3luoxuan.com/incubator/index"
                },
                {
                    "type": "view",
                    "name": "政策申报",
                    "url": "https://mp.weixin.qq.com/mp/homepage?__biz=MzUzNTAzOTcwOA==&hid=3&sn=982dab614fb91e26963fffc4618dff44"
                },
                {
                    "name": "活动资讯",
                    "sub_button":[
                                {
                                    "type": "view",
                                    "name": "活动预告",
                                    "url": "https://mp.weixin.qq.com/mp/homepage?__biz=MzUzNTAzOTcwOA==&hid=2&sn=1d2875715378177c3f9f7f77aa86cac1"
                                },
                                {
                                    "type": "view",
                                    "name": "历史活动",
                                    "url": "https://mp.weixin.qq.com/mp/homepage?__biz=MzUzNTAzOTcwOA==&hid=1&sn=8a63efd7a0b5c585f4576692dc35d83a"
                                }
                    ]
                }
        ]
    }
    """
    accessToken = real_get_access_token()
    print("access_token"+accessToken)
    create(postJson, accessToken)