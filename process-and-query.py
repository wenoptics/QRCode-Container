#!/usr/bin/python
# coding: utf-8
__author__ = 'wenop'
from core.scan import init_zbar, zbar
# from core.lc import leancloud_init, query_code
from main_process_flow import draw_package_out

def query_handler(proc, image, closure):
    # extract results
    for symbol in image.symbols:

        if symbol.type == zbar.Symbol.QRCODE:
            qrdata = symbol.data
            print '<QRCODE> "%s"' % qrdata
            print '...Now query from db'
            #error, data = query_code(qrdata)
            error, data  = draw_package_out(qrdata) #p2_receiver(symbol.data)
            if not error:
                print '-------------------------'
                print 'I should open Box-ID"%s"' % (data['container_id_that_storage_in'], )
                print '-------------------------'
            else:
                print '[ERROR] %s' % (error, )
        else:
            # do something useful with results
            print 'decoded', symbol.type, '"%s"' % symbol.data



if __name__ == '__main__':

    proc = init_zbar(query_handler)
    # leancloud_init('GfjXum4meVJkHhxG0inPJwz1', 'XFdSx2fxjRNzyO70nqxoeQOg')

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