#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2016年4月19日

@author: Conan
'''
from me.coolxll.sms.basesms import BaseSms
import logging
from me.coolxll.config.config import JIUMA_USERNAME, JIUMA_PASSWORD
import time

class JiuMa(BaseSms):
    
    '''
    Jiuma for receiving verify sms
    '''
    
    BASE_URL = 'http://api.9mli.com/http.aspx?action='
    logger = logging.getLogger(__name__)

    def __init__(self, pid):
        '''
        '''
        super(JiuMa,self).__init__(pid)
        
    def login(self,username=JIUMA_USERNAME,password=JIUMA_PASSWORD):
        return super(JiuMa,self).login(username,password)
    
    def getMobileNum(self,pid=None):
        return super(JiuMa,self).getMobileNum(pid)
    
    def getVcodeAndReleaseMobile(self,mobile):
        while True:
            resp = self.session.post(self.BASE_URL + 'getVcodeAndReleaseMobile',{
                "mobile":mobile,
                "uid":self.username,
                "token":self.token,
                "author_uid":"coolxll",
                "pid":self.pid
            })
            if resp.text != 'not_receive':
                print resp.text
                return resp.text.split('|')[1]
                break
            #Sleep 0.5 seconds
            time.sleep(1)
    
    def releaseMobile(self,mobile):
        resp = self.session.post(self.BASE_URL + 'ReleaseMobile',{
            "uid":self.username,
            "token":self.token,
            "mobile":mobile
        })
        return resp.text
    
    def sendSms(self,pid,mobileno,content):
        resp = self.session.post(self.BASE_URL + 'getMobilenum',{
                "mobile":mobileno,
                "uid":self.username,
                "pid":pid,
                "token":self.token
        })
        logging.debug(resp.text)
        resp = self.session.post(self.BASE_URL + 'sendSms',{
                "uid":self.username,
                "pid":pid,
                "mobile":mobileno,
                "content":content,
                "token":self.token
        })
        logging.debug(resp.text)
        while True:
            resp = self.session.post(self.BASE_URL + 'getSmsStatus',{
                    "uid":self.username,
                    "pid":pid,
                    "mobile":mobileno,
                    "token":self.token
            })
            logging.debug(resp.text)
            if resp.text == 'succ':
                break