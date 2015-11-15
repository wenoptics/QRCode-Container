# coding: utf-8
__author__ = 'wenop'

import sys
sys.path.append('/usr/lib/python2.7/dist-packages/')
import RPi.GPIO as gpio

# 通电时间
defalut_interval = 2

PinOut_activate_by_high = 24
PinOut_activate_by_low = 18
PinIn = 23

def GPIO_init():
    gpio.setmode(gpio.BCM)
    gpio.setup(PinOut_activate_by_high, gpio.OUT)
    gpio.setup(PinOut_activate_by_low, gpio.OUT)
    gpio.setup(PinIn, gpio.IN, pull_up_down=gpio.PUD_UP)


# 检测箱体门传感器
def read_sensor_states():
    return gpio.input(PinIn)


def activate(isEnable=True):
    if isEnable:
        gpio.output(PinOut_activate_by_low, gpio.LOW)
        gpio.output(PinOut_activate_by_high, gpio.HIGH)
    else:
        gpio.output(PinOut_activate_by_low, gpio.HIGH)
        gpio.output(PinOut_activate_by_high, gpio.LOW)


import time
def open_container():
    print '- fire on'
    activate(True)
    time.sleep(defalut_interval)
    print '- fire off'
    activate(False)

GPIO_init()