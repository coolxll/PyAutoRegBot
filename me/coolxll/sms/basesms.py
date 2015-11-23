#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015年11月4日

@author: Conan
'''
import logging
import requests
import time

class BaseSms(object):
    '''
    SMS Base Class
    '''
    BASE_URL = ''
    logger = logging.getLogger(__name__)

    def __init__(self,pid=None):
        '''
        Constructor
        '''
        self.session = requests.Session()
        self.login()
        if pid:
            self.pid = pid
        
    def login(self,username,password):
        resp = self.session.post(self.BASE_URL + 'loginIn',{
            "uid":username,
            "pwd":password
        })
        if '|' in resp.text and username in resp.text:
            username,token = resp.text.split('|')
            self.username = username
            self.token = token
            return token
        else:
            self.logger.error(resp.text)
            
    def getMobileNum(self,pid):
        '''
        '''
        if not pid:
            pid = self.pid
        resp = self.session.post(self.BASE_URL + 'getMobilenum',{
            "pid":pid,
            "uid":self.username,
            "token":self.token
        })
        if '|' in resp.text:
            mobile,token = resp.text.split('|')
        return mobile
    
    def getVcodeAndReleaseMobile(self,mobile):
        while True:
            resp = self.session.post(self.BASE_URL + 'getVcodeAndReleaseMobile',{
                "mobile":mobile,
                "uid":self.username,
                "token":self.token,
                "author_uid":"coolxlldev"
            })
            if resp.text != 'not_receive':
                print resp.text
                return resp.text.split('|')[1]
                break
            #Sleep 0.5 seconds
            time.sleep(0.5)
    
    def releaseMobile(self,mobile):
        pass