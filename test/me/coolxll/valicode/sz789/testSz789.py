#/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015年10月24日

@author: Conan
'''
import unittest
from me.coolxll.valicode.sz789.sz789 import SZ789
from os.path import join,dirname


class Test(unittest.TestCase):


    def testSZ789(self):
        valicoder = SZ789()
        code,imageid = valicoder.rec_file(join(dirname(__file__),'test.jpg'))
        self.assertEqual(code, 'rueq', 'The Captcha is RUEQ')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testSZ789']
    unittest.main()