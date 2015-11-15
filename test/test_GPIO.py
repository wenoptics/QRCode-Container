#!/usr/bin/python.old
# coding: utf-8
__author__ = 'wenop'

import sys
sys.path.append('/usr/lib/python2.7/dist-packages/')
import RPi.GPIO as gpio

### 用灌电流方式

# 通电时间
defalut_interval = 2

testPinOut = 18
testPinIn = 23

gpio.setmode(gpio.BCM)
gpio.setup(testPinOut, gpio.OUT)
gpio.setup(testPinIn, gpio.IN, pull_up_down=gpio.PUD_UP)

def test_read():
    return gpio.input(testPinIn)

def activate(isEnable=True, containerPin=testPinOut):
    if isEnable:
        gpio.output(testPinOut, gpio.LOW)
    else:
        gpio.output(testPinOut, gpio.HIGH)


import time
def open_container(container_pin=testPinOut):
    print '- fire on'
    activate(True, containerPin=container_pin)
    time.sleep(defalut_interval)
    print '- fire off'
    activate(False, containerPin=container_pin)


if __name__ == '__main__':
    # open_container(18)
    lastState = None
    while True:
        val = test_read()
        if val != lastState:
            print val
            lastState = val
        time.sleep(0.5)


    # activate(True)
    # import time
    # time.sleep(2)
    # activate(False)

