#!/usr/bin/python
# coding: utf-8
__author__ = 'wenop'
from core.scan import init_zbar, zbar
from apicloudCore import draw_package_out

def proc_for_deliver(package, fromDeliver):
    #
    #   containerID = 找一个空箱子()
    #   打开箱子
    #       检测用户把门打开
    #       检测用户把门关上
    #   存package信息存云端(package)
    #   给package的receiver发一条推送通知
    #       "您有一个快递到达啦！存放在<%理工大学15号宿舍楼%>快件自取箱，请您凭二维码取件。
    #       如有疑问，可咨询您的派件员<%fromDeliver%>"
    #
    raise NotImplementedError

def proc_for_receiver(code):
    #
    # 根据code把一个箱子打开
    # containerID = draw_out_package(code)
    # 打开箱子containerID
    #   检测用户把门打开
    #   检测用户把门关上
    #
    raise NotImplementedError


import json
def parse_qrcode(strQRCode):

    # todo 不要阻塞二维码扫描进程, 做task队列，

    try:
        data = json.loads(strQRCode)

        if data:
            return proc_for_deliver(package, fromDeliver)
        elif 是receiver口令:
            return proc_for_receiver(code)
        else:
            err = "fail to parse QRCode"
            return err, None

    except Exception,e:
        err = "fail to parse QRCode"



def query_handler(proc, image, closure):
    # extract results
    for symbol in image.symbols:

        if symbol.type == zbar.Symbol.QRCODE:
            qrdata = symbol.data
            print '<QRCODE> "%s"' % qrdata
            # print '...Now query from db'
            error, data  = parse_qrcode(qrdata) #p2_receiver(symbol.data)
            if not error:
                print '-------------------------'
                print 'I should open Box-ID"%s"' % (data['container_id_that_storage_in'], )
                print '-------------------------'
            else:
                print '[ERROR] %s' % (error, )
        else:
            print 'decoded', symbol.type, '"%s"' % symbol.data




if __name__ == '__main__':

    proc = init_zbar(query_handler)

    # initiate scanning
    proc.active = True
    print 'scanning started...'
    try:
        # keep scanning until user provides key/mouse input
        proc.user_wait()
    except zbar.WindowClosed, e:
        pass
    except KeyboardInterrupt:
        pass