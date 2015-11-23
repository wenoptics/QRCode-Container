# coding: utf-8
from apicloudCore import get_an_empty_container, store_package_in_container, get_user_phone, draw_package_out, \
    add_succVal
from core import bmob_sms

__author__ = 'wenop'



def proc_for_deliver(package_id, fromDeliver_id, onSuccVal):
    #
    #   containerID = 找一个空箱子()
    print 'finding a empty container'
    container = get_an_empty_container()
    if not container:
        err = 'no available container.'
        return err, None

    #   打开箱子 -todo
    #       检测用户把门打开  -todo
    #       检测用户把门关上  -todo

    #   存package信息存云端(package)
    #       设置packageInfo的is_in_container=true
    #       增加一条StorageEntry
    #       增加一条SuccIndicator

    try:
        newEntry, receiver_id = store_package_in_container(package_id, container, fromDeliver_id, onSuccVal)
    except Exception,e:
        err = "err in store_package_in_container,"+e.message
        return err, None

    #   给package的receiver发一条推送通知
    #       "您有一个快递到达啦！存放在<%理工大学15号宿舍楼%>快件自取箱，请您凭二维码取件。
    #       如有疑问，可咨询您的派件员<%fromDeliver%>"
    #
    try:
        receiver_phone = get_user_phone(receiver_id)
        deliver_phone = get_user_phone(fromDeliver_id)
        ret = bmob_sms.push_msg_to_receiver(receiver_phone, deliver_phone)
        print 'send sms ret=', ret
    except Exception,e:
        err = "err when send sms,"+e.message
        return err, None

    err = None
    return err, []


def proc_for_receiver(code, onSuccVal):
    #
    # 根据code把一个箱子打开
    try:
        err, data = draw_package_out(code)
        if err:
            #print "draw_package_out.error:", err
            return err, None
    except Exception,e:
        err = "err when draw_package_out(),"+e.message
        return err, None

    # 打开箱子containerID
    #   检测用户把门打开
    #   检测用户把门关上
    #

    # 增加一条SuccIndicator
    add_succVal(onSuccVal)

    return None, []


import json
def parse_qrcode(strQRCode):

    # todo 不要阻塞二维码扫描进程, 做task队列，

    try:
        data = json.loads(strQRCode)

        if data.get('c') == 'd':
            # from deliver
            package_id = data['package_id']
            fromDeliver_id = data['deliver_id']
            onSuccVal = data['succVal']
            return proc_for_deliver(package_id, fromDeliver_id, onSuccVal)

        elif data.get('c') == 'r':
            # from deliver
            code = data['code']
            onSuccVal = data['succVal']
            return proc_for_receiver(code, onSuccVal)
        else:
            err = "fail to parse QRCode"
            return err, None

    except Exception,e:
        err = "fail to parse QRCode"
        return err, None


qrcodeText ="""{"c":"r","code":"25b1bb27d0d8f4551e160384ff57a10b","succVal":"A4fsncXB"}"""
#"""{"c":"d","deliver_id":"5651c20ceb5dc3cb13ee6baa","package_id":"565299c626fc432916c2e222","succVal":"GxEH6pZE"}"""

#"""{"c":"d", "deliver_id": "1122", "package_id": "3344", "succVal":"C8V8d"}"""
err, data = parse_qrcode(qrcodeText)
print "finally!",err, ";", data
