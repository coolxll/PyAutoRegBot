#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015年10月24日

@author: Conan
'''
from me.coolxll.config.config import SHENHUA_USERNAME as USERNAME,SHENHUA_PASSWORD as PASSWORD
import logging
import time
from me.coolxll.sms.basesms import BaseSms

class Shenhua(BaseSms):
    '''
    Shenhua for receiving verify sms
    '''
    
    BASE_URL = 'http://api.shjmpt.com:9002/pubApi/'
    logger = logging.getLogger(__name__)

    def __init__(self,pid=None):
        '''
        Initialize
        '''
        super(Shenhua,self).__init__(pid)
        
    def login(self,username=USERNAME,password=PASSWORD):
        resp = self.session.post(self.BASE_URL + 'uLogin',params = {
            "uName":username,
            "pWord":password,
            "Developer":'yzsmwj89ruhBtx%2beP185sQ%3d%3d'
        })
        token = resp.text.split('&')[0]
        self.username = username
        self.token = token
        return token
            
    def getMobileNum(self,pid=None):
        if not pid and self.pid:
            pid = self.pid
        resp = self.session.get(self.BASE_URL + 'GetPhone',params = {
            "token":self.token,
            "ItemId":pid
        })
        return resp.text.rstrip(';')
    
    def getVcodeAndReleaseMobile(self,mobile):
        while True:
            resp = self.session.get(self.BASE_URL + 'GMessage',params = {
                "Phone":mobile,
                "token":self.token,
                "ItemId":self.pid
            })
            if resp.text != u'False:没有状态或短信，请5秒后再试试':
                msg,pid,mobile,smscontent = resp.text.split('&')
                if smscontent != '':
                    self.logger.info(smscontent)
                    return smscontent
            #Sleep 5 seconds
            time.sleep(5)
    
    def releaseMobile(self,mobile,username=USERNAME):
        pass
    
    def sendSms(self,pid,mobileno,content):
        resp = self.session.post(self.BASE_URL + 'getMobilenum',params = {
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