#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015年10月24日

@author: Conan
'''
from me.coolxll.config.config import AIMA_USERNAME,AIMA_PASSWORD
import logging
import time
from me.coolxll.sms.basesms import BaseSms

class Aima(BaseSms):
    '''
    Aima for receiving verify sms
    '''
    
    BASE_URL = 'http://api.f02.cn/http.do?action='
    logger = logging.getLogger(__name__)

    def __init__(self):
        '''
        Initialize
        '''
        super(Aima,self).__init__()
        
    def login(self,username=AIMA_USERNAME,password=AIMA_PASSWORD):
        return super(Aima,self).login(username,password)
            
    def getMobileNum(self,pid=None,username=AIMA_USERNAME):
        return super(Aima,self).getMobileNum(pid,username)
    
    def getVcodeAndReleaseMobile(self,mobile,username=AIMA_USERNAME):
        while True:
            resp = self.session.post(self.BASE_URL + 'getVcodeAndReleaseMobile',{
                "mobile":mobile,
                "uid":username,
                "token":self.token,
                "author_uid":"coolxlldev"
            })
            if resp.text != 'not_receive':
                print resp.text
                return resp.text.split('|')[1]
                break
            #Sleep 0.5 seconds
            time.sleep(0.5)
    
    def releaseMobile(self,mobile,username=AIMA_USERNAME):
        resp = self.session.post(self.BASE_URL + 'cancelSMSRecv',{
            "uid":username,
            "token":self.token,
            "mobile":mobile
        })
        return resp.text