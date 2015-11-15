# coding: utf-8
__author__ = 'wenop'

from fabric.api import *

env.hosts = ['root@192.168.1.51', ]
env.password = 'vvenop'

@task
def test0():
    local('dir')
    run('ls')