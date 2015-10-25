#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015年10月24日

@author: Conan
'''
import requests
from me.coolxll.sms.f02.config import username,password
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
        
    def login(self,username=username,password=password):
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
            
    def getMobileNum(self,pid,username=username):
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
    
    def getVcodeAndReleaseMobile(self,mobile,username=username):
        while True:
            resp = self.session.post(self.BASE_URL + 'getVcodeAndReleaseMobile',{
                "mobile":mobile,
                "uid":username,
                "token":self.token,
                "author_uid":"coolxll"
            })
            if resp.text != 'not_receive':
                return resp.text.split('|')[1]
                break
            #Sleep 0.5 seconds
            time.sleep(0.5)