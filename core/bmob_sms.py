# coding: utf-8
import httplib
import json

__author__ = 'wenop'
import requests

from config import bmob_config
def push_msg_to_receiver(phone, fromPhone):
    try:
        payload = {
            "mobilePhoneNumber": phone,
            "content": ("【dLiver】您有一个快递到达啦！"
                       + "存放在%s"
                       + "快件自取箱，请您凭二维码取件。"
                       + "如有疑问，可咨询您的派件员%s"
                       + "【大学生创新训练项目】")
                       % ("理工大学15号宿舍楼", fromPhone)
        }
        url = 'https://api.bmob.cn/1/requestSms'
        #conn.request('POST', url = url, body = body)
        #如果需要带headers，则可先声明
        headers = {
            'X-Bmob-Application-Id' : bmob_config.appId,
            'X-Bmob-REST-API-Key' : bmob_config.restKey,
            'Content-Type': 'application/json',
        }
        res = requests.post(url, data=json.dumps(payload), headers=headers)
        if res.status_code == 200:
            return res.content
        else:
            return res
    except Exception, e:
        print ('[HttpGET] get from server failed, errmsg=%s' % (e))
        return -1
