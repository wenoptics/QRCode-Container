#!/usr/bin/python
# coding: utf-8
__author__ = 'wenop'

from apicloudCore import *
from group_GPIO import open_container, read_sensor_states

def p1_deliver():
    print 'now login'
    user = user_login('apicloud', '123456')

    print 'now create new package'
    package = new_package_for_user(user)

    print 'find a empty container for you'
    container = get_an_empty_container()
    if not container:
        print 'no available container.'
        return

    # now open container
    print 'open container for you...'
    open_container()

    print 'waiting for closing...'
    lastState = None
    while lastState!=1:
        lastState = read_sensor_states()
        import time
        time.sleep(0.5)
    print 'container closed.'

    entry = store_package_in_container(package, container)

    storageCode = entry.get('code')
    if storageCode:
        print 'storage code is:', storageCode
    else:
        print 'storage failed'


def p2_receiver(code):
    ret = draw_package_out(code)
    print ret

    if ret is None:
        return ('Item not found', None)

    print '[INFO] Opening container for you...'
    open_container()

    return (None, ret)



if __name__ == "__main__":
    p1_deliver()
    #p2_receiver()