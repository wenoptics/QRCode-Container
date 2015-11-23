# coding: utf-8
from core import bmob_sms

__author__ = 'wenop'

ret = bmob_sms.push_msg_to_receiver('13102102731', 'wenop_dd')
print ret