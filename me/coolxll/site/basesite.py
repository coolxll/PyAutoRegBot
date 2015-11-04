#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015年11月4日

@author: Conan
'''
from me.coolxll.sms.zmyzm.zhuoma import Zhuoma
from me.coolxll.util.myrequests import CustomSession
from me.coolxll.valicode.sz789.sz789 import SZ789

class BaseSite(object):
    '''
    Base Site Class for inheritance
    '''

    BASE_URL = ''
    
    def __init__(self,sms=None):
        '''
        '''
        if sms:
            self.sms = sms
        else:
            self.sms = Zhuoma()
        self.session = CustomSession()
        self.session.setiPhoneUA()
        self.verify = SZ789()
        
    def parseCodeMsg(self,codemsg):
        pass