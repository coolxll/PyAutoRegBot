#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015年10月24日

@author: Conan
'''
import unittest
from me.coolxll.sms.f02.aima import Aima
from me.coolxll.sms.shjmpt.shenhua import Shenhua


class Test(unittest.TestCase):


    def test_shenhua(self):
        sh = Shenhua(1731)
        mobile = sh.getMobileNum()
        text = sh.getVcodeAndReleaseMobile(mobile)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testf02']
    unittest.main()