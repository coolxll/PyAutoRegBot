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
import json

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
    
    def reg_amoney(self,sequencial_id):
        self.session.setiPhoneWeixinUA()
        self.session.get("http://activity.zhenrongbao.com/aprizetree/share?contact_from=30103_2&sequence_id={}".format(sequencial_id))
        self.session.get("http://activity.zhenrongbao.com/aprizetree/register")
        resp = self.session.get("https://account.zhenrongbao.com/sso/gettoken?_access_token=&_=1472828588985&callback=jsonp1")
        respJson = self.parseJsonP(resp.text, 'jsonp1')
        token = respJson.get("data").get("token")
        filebuf = self.session.get("https://account.zhenrongbao.com/verify/qcode?_={}".format(int(time.time()))).content
        yzm,imageId = self.verify.rec_buf(filebuf)
        self.logger.debug("Verify Code:{}".format(yzm))
        mobileno = self.sms.getMobileNum()
        while mobileno == 'no_data':
            time.sleep(3)
            mobileno = self.sms.getMobileNum()
        logging.info("获取到手机号码{}".format(mobileno))
        resp = self.session.get("https://account.zhenrongbao.com/sso/checkregimagevcode?user_name={}&vcode={}&token={}&_access_token=&_={}&callback=jsonp2".format(
                        mobileno,yzm,token,int(time.time())))
        respJson = self.parseJsonP(resp.text, 'jsonp2')
        while respJson.get('error_no') != 0:
            self.verify.reportError(imageId)
            filebuf = self.session.get("https://account.zhenrongbao.com/verify/qcode?_={}".format(int(time.time()))).content
            yzm,imageId = self.verify.rec_buf(filebuf)
            resp = self.session.get("https://account.zhenrongbao.com/sso/checkregimagevcode?user_name={}&vcode={}&token={}&_access_token=&_={}&callback=jsonp2".format(
                        mobileno,yzm,token,int(time.time())))
            self.logger.debug("Verify Code:{}".format(yzm))
            respJson = self.parseJsonP(resp.text, 'jsonp2')
        resp = self.session.get("https://account.zhenrongbao.com/sso/sendregsmsvcode?type=0&mobile={}&token={}&operate=3&_access_token=&_={}&callback=jsonp3".format(
                        mobileno,token,int(time.time())))
        respJson = self.parseJsonP(resp.text, 'jsonp3')
        if respJson.get('error_no') != 0:
            print respJson.get('error_message')
        else:
            print respJson
        codemsg = self.sms.getVcodeAndReleaseMobile(mobileno)
        codemsg = self.parseCodeMsg(codemsg)
        resp = self.session.post("https://account.zhenrongbao.com/sso/register",{
                'user_name':mobileno,
                'passwd':'pass2015',
                'platform':'wap',
                'redirect':'http://activity.zhenrongbao.com/static/activity_account/sso/redirect.html',
                'callback':'ZrbAccount.callback',
                'd_id':'65d547dd41db3c38c6628444c31f3a03',
                'd_screen':'375_667',
                'd_timez':'8',
                'd_sys':'Win32',
                'code':codemsg,
                'recommender':'',
                'recommender_sequence_id':sequencial_id,
                'agreement':'true'
            })
        logging.info(resp.text)
        #self.session.get("http://activity.zhenrongbao.com/aprizetree/share?contact_from=30101&sequence_id={}".format(sequencial_id))
        r = self.session.get("http://activity.zhenrongbao.com/aprizetree/aftersuccess")
        r = self.session.post("http://activity.zhenrongbao.com/aprizetree/beforesuccess",{
            "_access_token":""
        }) 
        r = self.session.post("http://activity.zhenrongbao.com/aprizetree/beforesuccess",{
            "_access_token":""
        }) 
        r = self.session.post("http://activity.zhenrongbao.com/aprizetree/beforesuccess",{
            "_access_token":""
        }) 

    def aevelen(self,sequencial_id):
        self.session.setiPhoneWeixinUA()
        self.session.get("http://activity.zhenrongbao.com/aeleven/index?contact_from=30116_4&sequence_id={}".format(sequencial_id))
        self.regMobile(sequencial_id)
        self.session.get("http://activity.zhenrongbao.com/aeleven/beforesuccess")
        self.session.get("http://activity.zhenrongbao.com/aeleven/index?autoplay=1")
        self.session.get("http://activity.zhenrongbao.com/aeleven/save")

    def reg_amoney1(self,sequencial_id):
        self.session.setiPhoneWeixinUA()
        self.session.get("http://activity.zhenrongbao.com/amoneygame/share?contact_from=30106_3&sequence_id={}".format(sequencial_id))
        self.session.get("http://activity.zhenrongbao.com/amoneygame/register")
        resp = self.session.get("https://account.zhenrongbao.com/sso/gettoken?_access_token=&_=1472828588985&callback=jsonp1")
        respJson = self.parseJsonP(resp.text, 'jsonp1')
        token = respJson.get("data").get("token")
#         print token
        filebuf = self.session.get("https://account.zhenrongbao.com/verify/qcode?_={}".format(int(time.time()))).content
        yzm,imageId = self.verify.rec_buf(filebuf)
        self.logger.debug("Verify Code:{}".format(yzm))
        mobileno = self.sms.getMobileNum()
        while mobileno == 'no_data':
            time.sleep(3)
            mobileno = self.sms.getMobileNum()
        logging.info("获取到手机号码{}".format(mobileno))
        resp = self.session.get("https://account.zhenrongbao.com/sso/checkregimagevcode?user_name={}&vcode={}&token={}&_access_token=&_={}&callback=jsonp2".format(
                        mobileno,yzm,token,int(time.time())))
        respJson = self.parseJsonP(resp.text, 'jsonp2')
        while respJson.get('error_no') != 0:
            self.verify.reportError(imageId)
            filebuf = self.session.get("https://account.zhenrongbao.com/verify/qcode?_={}".format(int(time.time()))).content
            yzm,imageId = self.verify.rec_buf(filebuf)
            resp = self.session.get("https://account.zhenrongbao.com/sso/checkregimagevcode?user_name={}&vcode={}&token={}&_access_token=&_={}&callback=jsonp2".format(
                        mobileno,yzm,token,int(time.time())))
            self.logger.debug("Verify Code:{}".format(yzm))
            respJson = self.parseJsonP(resp.text, 'jsonp2')
        resp = self.session.get("https://account.zhenrongbao.com/sso/sendregsmsvcode?type=0&mobile={}&token={}&operate=3&_access_token=&_={}&callback=jsonp3".format(
                        mobileno,token,int(time.time())))
        respJson = self.parseJsonP(resp.text, 'jsonp3')
        if respJson.get('error_no') != 0:
            print respJson.get('error_message')
        else:
            print respJson
        codemsg = self.sms.getVcodeAndReleaseMobile(mobileno)
        codemsg = self.parseCodeMsg(codemsg)
        resp = self.session.post("https://account.zhenrongbao.com/sso/register",{
                'user_name':mobileno,
                'passwd':'pass2015',
                'platform':'wap',
                'redirect':'http://activity.zhenrongbao.com/static/activity_account/sso/redirect.html',
                'callback':'ZrbAccount.callback',
                'd_id':'afb5a01d6c4aac6c9a71c10c86b138e0',
                'd_screen':'375_667',
                'd_timez':'8',
                'd_sys':'Win32',
                'code':codemsg,
                'recommender':'',
                'recommender_sequence_id':sequencial_id,
                'agreement':'true'
            })
        #logging.info(resp.text)
        #self.session.get("http://activity.zhenrongbao.com/aprizetree/share?contact_from=30101&sequence_id={}".format(sequencial_id))
        r = self.session.get("http://activity.zhenrongbao.com/amoneygame/index")
    def reg(self,invitemobile):
        self.session.setChromeUA()
        self.session.get(self.BASE_URL + "/account/register")
            #filebuf = self.session.get(self.BASE_URL + "/verification/qcode").content
            #yzm,imageId = self.verify.rec_buf(filebuf)
            #self.logger.debug("Verify Code:{}".format(yzm))
        mobileno = self.sms.getMobileNum()
        while mobileno == u'False:Session 过期':
            time.sleep(3)
            mobileno = self.sms.getMobileNum()
        self.logger.info("获取到号码{}".format(mobileno))
        self.sendCodeAndRegister(mobileno, invitemobile)
        return mobileno
    
    def sendCodeAndRegister(self,mobileno,recommender):
        #self.session.get(self.BASE_URL + "/account/registering")
        resp = self.session.post(self.BASE_URL + "/account/checksendregsmsvcode",{
            "mobile":mobileno,
            "_access_token":"",
            "d_id":"a22afcb604eb105169864eb61b742625",   #"cb7a7f5d72cc91172dc9c5e3197d4139",
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
            "d_id":"a22afcb604eb105169864eb61b742625",
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
            "d_id":"a22afcb604eb105169864eb61b742625",
            "d_screen":"1920_1080",
            "d_timez":"8",
            "d_sys":"Win32",
            "recommender":recommender,
            "platform":"pc"
        })
        if resp.json().get("error_no") == 0:
            self.logger.info("Register New User Successful, Username {}".format(mobileno))
    
       
    def parseJsonP(self,jsonpStr,callback):
        return json.loads(jsonpStr.lstrip(callback + '(') .rstrip(')'))

    def regMobile(self, sequencial_id):
        self.session.get("http://activity.zhenrongbao.com/aprizetree/register")
        resp = self.session.get(
            "https://account.zhenrongbao.com/sso/gettoken?_access_token=&_=1472828588985&callback=jsonp1")
        respJson = self.parseJsonP(resp.text, 'jsonp1')
        token = respJson.get("data").get("token")
        filebuf = self.session.get("https://account.zhenrongbao.com/verify/qcode?_={}".format(int(time.time()))).content
        yzm, imageId = self.verify.rec_buf(filebuf)
        self.logger.debug("Verify Code:{}".format(yzm))
        mobileno = self.sms.getMobileNum()
        while mobileno == 'no_data':
            time.sleep(3)
            mobileno = self.sms.getMobileNum()
        logging.info("获取到手机号码{}".format(mobileno))
        resp = self.session.get(
            "https://account.zhenrongbao.com/sso/checkregimagevcode?user_name={}&vcode={}&token={}&_access_token=&_={}&callback=jsonp2".format(
                mobileno, yzm, token, int(time.time())))
        respJson = self.parseJsonP(resp.text, 'jsonp2')
        while respJson.get('error_no') != 0:
            self.verify.reportError(imageId)
            filebuf = self.session.get(
                "https://account.zhenrongbao.com/verify/qcode?_={}".format(int(time.time()))).content
            yzm, imageId = self.verify.rec_buf(filebuf)
            resp = self.session.get(
                "https://account.zhenrongbao.com/sso/checkregimagevcode?user_name={}&vcode={}&token={}&_access_token=&_={}&callback=jsonp2".format(
                    mobileno, yzm, token, int(time.time())))
            self.logger.debug("Verify Code:{}".format(yzm))
            respJson = self.parseJsonP(resp.text, 'jsonp2')
        resp = self.session.get(
            "https://account.zhenrongbao.com/sso/sendregsmsvcode?type=0&mobile={}&token={}&operate=3&_access_token=&_={}&callback=jsonp3".format(
                mobileno, token, int(time.time())))
        respJson = self.parseJsonP(resp.text, 'jsonp3')
        if respJson.get('error_no') != 0:
            print respJson.get('error_message')
        else:
            print respJson
        codemsg = self.sms.getVcodeAndReleaseMobile(mobileno)
        codemsg = self.parseCodeMsg(codemsg)
        resp = self.session.post("https://account.zhenrongbao.com/sso/register", {
            'user_name': mobileno,
            'passwd': 'pass2015',
            'platform': 'wap',
            'redirect': 'http://activity.zhenrongbao.com/static/activity_account/sso/redirect.html',
            'callback': 'ZrbAccount.callback',
            'd_id': '65d547dd41db3c38c6628444c31f3a03',
            'd_screen': '375_667',
            'd_timez': '8',
            'd_sys': 'Win32',
            'code': codemsg,
            'recommender': '',
            'recommender_sequence_id': sequencial_id,
            'agreement': 'true'
        })
        logging.info(resp.text)
        