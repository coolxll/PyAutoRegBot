#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015年11月11日

@author: Conan
'''
import unittest

from me.coolxll.sms.zmyzm.zhuoma import Zhuoma
import logging

class Test(unittest.TestCase):


    def testSendSMS(self):
        logging.basicConfig(level=logging.DEBUG)
        zm = Zhuoma()
        zm.sendSms(3444, '18439515046', 'test')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testSendSMS']
    unittest.main()