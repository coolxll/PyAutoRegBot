#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015年10月24日

@author: Conan
'''
from me.coolxll.config.config import SHENMA_USERNAME as USERNAME,SHENMA_PASSWORD as PASSWORD
import logging
import time
from me.coolxll.sms.basesms import BaseSms

class Shenma(BaseSms):
    '''
    Shenma for receiving verify sms
    '''
    
    BASE_URL = 'http://api.iyylw.com/'
    logger = logging.getLogger(__name__)

    def __init__(self,pid=None):
        '''
        Initialize
        '''
        super(Shenma,self).__init__(pid)
        
    def login(self,username=USERNAME,password=PASSWORD):
        resp = self.session.post(self.BASE_URL + 'login',{
            "user":username,
            "pwd":password
        })
        respJson = resp.json()
        if respJson.get('code') == 0:
            self.username = username
            self.token = respJson.get('token')
            return self.token
        else:
            self.logger.error(respJson.get('msg'))
            
    def getMobileNum(self,pid=None):
        if not pid and self.pid:
            pid = self.pid
        resp = self.session.post(self.BASE_URL + 'get_mobile',{
            "token":self.token,
            "pid":pid,
            "author":'smyzmdev'
        })
        respJson = resp.json()
        if respJson.get('code') == 0:
            mobileno = respJson.get('mobile_list')
            return mobileno
        else:
            self.logger.error(respJson.get('msg'))
    
    def getVcodeAndReleaseMobile(self,mobile):
        while True:
            resp = self.session.post(self.BASE_URL + 'get_sms',{
                "mobile":mobile,
                "token":self.token,
                "pid":self.pid,
                "author_uid":"coolxlldev"
            })
            respJson = resp.json()
            if respJson.get('code') != 207:
                print respJson.get('sms_content')
                return respJson.get('sms_content')
                break
            #Sleep 2 seconds
            time.sleep(2)
    
    def releaseMobile(self,mobile,username=USERNAME):
        pass
    
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