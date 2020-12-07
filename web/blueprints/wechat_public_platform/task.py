# 获取access_token, 应该是两个小时更新一次，但获取access_token上限是十万次/天，现在的业务量达不到，所以没有设置定时任务
import requests
import json


def real_get_access_token():
    appId = "wxb011e9c49adfb81c"
    appSecret = "8bb5994bb06cc1dc1185f116012c20a1"
    postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type="
               "client_credential&appid=%s&secret=%s" % (appId, appSecret))
    r = requests.get(postUrl)
    print(r.text)
    token_dic = json.loads(r.text)
    print(token_dic.get("access_token"))
    print(token_dic.get("expires_in"))
    left_time = token_dic.get("expires_in")
    access_token = token_dic.get("access_token")
    return access_token

