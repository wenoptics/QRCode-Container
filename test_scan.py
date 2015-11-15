#!/usr/bin/python
# coding: utf-8
__author__ = 'wenop'

from sys import argv
import zbar

# create a Processor
proc = zbar.Processor()

# configure the Processor
proc.parse_config('enable')

# configure the prescale
proc.set_prescale(210, 210)

# initialize the Processor
device = '/dev/video0'
if len(argv) > 1:
    device = argv[1]
proc.init(device, False)

# setup a callback
def my_handler(proc, image, closure):
    # extract results
    for symbol in image.symbols:
        # do something useful with results
        print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data

proc.set_data_handler(my_handler)

# disable the preview window
proc.visible = False

# initiate scanning
proc.active = True
try:
    # keep scanning until user provides key/mouse input
    proc.user_wait()
except zbar.WindowClosed, e:
    pass
