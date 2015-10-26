#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015年10月24日

@author: Conan
'''
import requests
from me.coolxll.config.config import AIMA_USERNAME,AIMA_PASSWORD
import token
import logging
import time

class Aima(object):
    '''
    Aima for receiving verify sms
    '''
    
    BASE_URL = 'http://api.f02.cn/http.do?action='
    logger = logging.getLogger(__name__)

    def __init__(self):
        '''
        Initialize
        '''
        self.session = requests.Session()
        self.login()
        
    def login(self,username=AIMA_USERNAME,password=AIMA_PASSWORD):
        resp = self.session.post(self.BASE_URL + 'loginIn',{
            "uid":username,
            "pwd":password
        })
        if '|' in resp.text and username in resp.text:
            username,token = resp.text.split('|')
            self.token = token
            return token
        else:
            self.logger.error(resp.text)
            
    def getMobileNum(self,pid,username=AIMA_USERNAME):
        '''
        '''
        resp = self.session.post(self.BASE_URL + 'getMobilenum',{
            "pid":pid,
            "uid":username,
            "token":self.token
        })
        if '|' in resp.text:
            mobile,token = resp.text.split('|')
        return mobile
    
    def getVcodeAndReleaseMobile(self,mobile,username=AIMA_USERNAME):
        while True:
            resp = self.session.post(self.BASE_URL + 'getVcodeAndReleaseMobile',{
                "mobile":mobile,
                "uid":username,
                "token":self.token,
                "author_uid":"coolxlldev"
            })
            if resp.text != 'not_receive':
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