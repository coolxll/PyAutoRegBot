#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015年10月24日

@author: Conan
'''
from me.coolxll.config.config import ZHUOMA_USERNAME,ZHUOMA_PASSWORD
import logging
import time
from me.coolxll.sms.basesms import BaseSms

class Zhuoma(BaseSms):
    '''
    Zhuoma for receiving verify sms
    '''
    
    BASE_URL = 'http://api.zmyzm.com/apiGo.do?action='
    logger = logging.getLogger(__name__)

    def __init__(self,pid=None):
        '''
        Initialize
        '''
        super(Zhuoma,self).__init__()
        
    def login(self,username=ZHUOMA_USERNAME,password=ZHUOMA_PASSWORD):
        return super(Zhuoma,self).login(username,password)
            
    def getMobileNum(self,pid=None,username=ZHUOMA_USERNAME):
        return super(Zhuoma,self).getMobileNum(pid,username)
    
    def getVcodeAndReleaseMobile(self,mobile,username=ZHUOMA_USERNAME):
        while True:
            resp = self.session.post(self.BASE_URL + 'getVcodeAndReleaseMobile',{
                "mobile":mobile,
                "uid":username,
                "token":self.token,
                "author_uid":"coolxlldev1988"
            })
            if resp.text != 'not_receive':
                logging.debug(resp.text)
                return resp.text.split('|')[1]
                break
            #Sleep 0.5 seconds
            time.sleep(0.5)
    
    def releaseMobile(self,mobile,username=ZHUOMA_USERNAME):
        pass