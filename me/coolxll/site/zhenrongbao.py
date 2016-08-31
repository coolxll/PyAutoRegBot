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
from me.coolxll.sms.zmyzm.zhuoma import Zhuoma
from me.coolxll.site.basesite import BaseSite
import time

ZHENRONGBAO_AIMA_PID = 9687
ZHENRONGBAO_ZHUOMA_PID = 3444

class Zhenrongbao(BaseSite):
    
    BASE_URL = "https://www.zhenrongbao.com"
    logger = logging.getLogger(__name__)
    def  __init__(self,sms=None):
        '''
        TODO: sms support strange, include sms in the constructor
        '''
        super(Zhenrongbao,self).__init__(sms)
        
    def parseCodeMsg(self,codemsg):
        pattern = re.compile(u'您的验证码为(?P<vmsg>\d{6})')
        result = re.search(pattern, codemsg)
        if result:
            return result.group("vmsg")
        return ""
    
    def regwap(self,invitemobile):
        self.session.setiPhoneUA()
        self.session.get(self.BASE_URL + '/wap/register')
        mobileno = ''
        while True:
            filebuf = self.session.get(self.BASE_URL + "/verification/qcode?rand={}".format(random.random())).content
            yzm,imageId = self.verify.rec_buf(filebuf)
            self.logger.debug("Verify Code:{}".format(yzm))
            ZHENRONGBAO_PID = 0
            if isinstance(self.sms, Aima):
                ZHENRONGBAO_PID = ZHENRONGBAO_AIMA_PID
            elif isinstance(self.sms, Zhuoma):
                ZHENRONGBAO_PID = ZHENRONGBAO_ZHUOMA_PID
            if not mobileno:
                mobileno = self.sms.getMobileNum()
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
        return mobileno
        
    def reg(self,invitemobile):
        self.session.setChromeUA()
        self.session.get(self.BASE_URL + "/account/register")
            #filebuf = self.session.get(self.BASE_URL + "/verification/qcode").content
            #yzm,imageId = self.verify.rec_buf(filebuf)
            #self.logger.debug("Verify Code:{}".format(yzm))
        mobileno = self.sms.getMobileNum()
        while mobileno == 'no_data':
            time.sleep(3)
            mobileno = self.sms.getMobileNum()
        self.sendCodeAndRegister(mobileno, invitemobile)
        return mobileno
    
    def sendCodeAndRegister(self,mobileno,recommender):
        #self.session.get(self.BASE_URL + "/account/registering")
        resp = self.session.post(self.BASE_URL + "/account/checksendregsmsvcode",{
            "mobile":mobileno,
            "_access_token":"",
            "d_id":"cb7a7f5d72cc91172dc9c5e3197d4139",
            "platform":"pc",
            "d_screen":"1920_1080",
            "d_timez":"8",
            "d_sys":"Win32"
        })
        resp = self.session.post(self.BASE_URL + "/account/sendidentitycodenew",{
            "mobile":mobileno,
            "type":0,
            "operate":3,
            "_access_token":"",
            "d_id":"cb7a7f5d72cc91172dc9c5e3197d4139",
            "platform":"pc",
            "d_screen":"1920_1080",
            "d_timez":"8",
            "d_sys":"Win32"
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
            "_access_token":"",
            "d_id":"cb7a7f5d72cc91172dc9c5e3197d4139",
            "d_screen":"1920_1080",
            "d_timez":"8",
            "d_sys":"Win32",
            "recommender":recommender,
            "platform":"pc"
        })
        if resp.json().get("error_no") == 0:
            self.logger.info("Register New User Successful, Username {}".format(mobileno))
        