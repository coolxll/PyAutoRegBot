#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015年10月24日

@author: Conan
'''
import logging
import re
from me.coolxll.util.myrequests import CustomSession
from me.coolxll.valicode.sz789.sz789 import SZ789
from me.coolxll.sms.f02.aima import Aima
import random

ZHENRONGBAO_AIMA_PID = 9687
class Zhenrongbao(object):
    
    BASE_URL = "https://www.zhenrongbao.com"
    logger = logging.getLogger(__name__)
    def  __init__(self):
        '''
        TODO: sms support strange, include sms in the constructor
        '''
        self.session = CustomSession()
        self.sms = Aima()
        self.verify = SZ789()
        
    def parseCodeMsg(self,codemsg):
        pattern = re.compile(u'您的验证码为(?P<vmsg>\d{6})')
        result = re.search(pattern, codemsg)
        if result:
            return result.group("vmsg")
        return ""
    
    def regwap(self,invitemobile):
        self.session.setiPhoneUA()
        self.session.get(self.BASE_URL + '/wap/register')
        while True:
            filebuf = self.session.get(self.BASE_URL + "/verification/qcode?rand={}".format(random.random())).content
            yzm,imageId = self.verify.rec_buf(filebuf)
            self.logger.debug("Verify Code:{}".format(yzm))
            mobileno = self.sms.getMobileNum(ZHENRONGBAO_AIMA_PID)
            resp = self.session.post(self.BASE_URL + '/wap/preresetpassword',{
                "user_name":mobileno,
                "qcode":yzm,
                "_access_token":""
            })
            if resp.json().get('error_no') == 0:
                self.logger.info('Zhenrongbao Verify Code Success')
                break
            else:
                self.logger.error('Zhenrongbao Verify Code parse error')
                self.verify.reportError(imageId)
        self.sendCodeAndRegister(mobileno, invitemobile)
        
    def reg(self,invitemobile):
        self.session.setChromeUA()
        self.session.get(self.BASE_URL + "/account/register")
        while True:
            filebuf = self.session.get(self.BASE_URL + "/verification/qcode").content
            yzm,imageId = self.verify.rec_buf(filebuf)
            self.logger.debug("Verify Code:{}".format(yzm))
            mobileno = self.sms.getMobileNum(ZHENRONGBAO_AIMA_PID)
            resp = self.session.post(self.BASE_URL + "/account/preregisteruser",{
                "user_name":mobileno,
                "qcode":yzm
            })
            if resp.json().get('error_no') == 0:
                self.logger.info('Zhenrongbao Verify Code Success')
                break
            else:
                self.logger.error('Zhenrongbao Verify Code parse error')
                self.verify.reportError(imageId)
        self.sendCodeAndRegister(mobileno, invitemobile)
    
    def sendCodeAndRegister(self,mobileno,invitemobile):
        #self.session.get(self.BASE_URL + "/account/registering")
        resp = self.session.post(self.BASE_URL + "/account/sendidentitycodenew",{
            "mobile":mobileno,
            "type":0,
            "_access_token":""
        })
        if not resp.json().get("error_message"):
            self.logger.info("Send verify message to {} success".format(mobileno))
        else:
            self.logger.error(resp.json().get("error_message"))
            self.sms.releaseMobile(mobileno)
            return
        codemsg = self.sms.getVcodeAndReleaseMobile(mobileno)
        codemsg = self.parseCodeMsg(codemsg)
        resp = self.session.post(self.BASE_URL + '/account/registerusernew', {
            "user_name":mobileno,
            "code":codemsg,
            "passwd":"pass2015",
            "recommender":invitemobile
        })
        if resp.json().get("error_no") == 0:
            self.logger.info("Register New User Successful, Username {}".format(mobileno))
        