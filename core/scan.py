# coding: utf-8
__author__ = 'wenop'

import zbar


def sample_handler(proc, image, closure):
    # extract results
    for symbol in image.symbols:
        # do something useful with results
        print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data



def init_zbar(data_handle , device=r'/dev/video0', show_preview=False):

    # create a Processor
    proc = zbar.Processor()

    # configure the Processor
    proc.parse_config('enable')

    # configure the prescale
    proc.set_prescale(210, 210)

    # initialize the Processor, with no display
    proc.init(device, show_preview)

    # setup a callback
    proc.set_data_handler(data_handle)

    # disable the preview window
    proc.visible = show_preview

    return proc
