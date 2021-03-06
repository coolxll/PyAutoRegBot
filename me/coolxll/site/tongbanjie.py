#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015年10月25日

@author: Conan
'''
from me.me.coolxll.util.myrequestsport CustomSession
from me.coolxll.sms.f02.aima import Aima
from me.coolxll.valicode.sz789.sz789 import SZ789
import time
import logging
import re
from me.coolxll.sms.zmyzm.zhuoma import Zhuoma
from me.coolxll.site.basesite import BaseSite

TONGBANJIE_AIMA_PID = 1428
TONGBANJIE_ZHUOMA_PID = 5042

class Tongbanjie(BaseSite):
    '''
    classdocs
    '''
    logger = logging.getLogger(__name__)
    BASE_URL = 'http://account.tongbanjie.com'
    def __init__(self,sms=None):
        '''
        Constructor
        '''
        super(Tongbanjie,self).__init__()
        self.session.headers.update({
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
        })
        
    def getVerifyCode(self,timestamp):
        r = self.session.get(self.BASE_URL + "/generateImageCode?t={}".format(timestamp))
        filebuf = r.content
        yzm,imageId = self.verify.rec_buf(filebuf)
        return yzm,imageId
    
    def parseCodeMsg(self,codemsg):
        pattern = re.compile(u'您的注册验证码为：(?P<vmsg>\d{4})')
        result = re.search(pattern, codemsg)
        if result:
            return result.group("vmsg")
        return ""
    
    def reg(self,invitelink,invitephone):
        timestamp = str(int(time.time()*1000))
        self.session.get(invitelink)
        code,imageId = self.getVerifyCode(timestamp)
        TONGBANJIE_PID = 0
        if isinstance(self.sms, Aima):
            TONGBANJIE_PID = TONGBANJIE_AIMA_PID
        elif isinstance(self.sms, Zhuoma):
            TONGBANJIE_PID = TONGBANJIE_ZHUOMA_PID
        mobileno = self.sms.getMobileNum(TONGBANJIE_PID)
        self.logger.info('Get Mobile No for Tongbanjie:{}'.format(mobileno))
        r = self.session.post(self.BASE_URL + '/web/invite/inviteValidatephone',{
            'phone':mobileno,
            'invitePhone':invitephone
        })
        token = r.json().get('token')
        while True:
            r = self.session.post(self.BASE_URL + '/web/invite/inviteValidatepicture',{
                'pictureCode':code,
                't':timestamp
            })
            if r.json().get('status') == 0:
                self.logger.info('Verify code Success')
                break
            else:
                self.logger.error('Verify code parse Error')
                self.verify.reportError(imageId)
                timestamp = str(int(time.time()*1000))
                code,imageId = self.getVerifyCode(timestamp)
        r = self.session.post(self.BASE_URL + '/web/invite/sendInviteSmscode',{
            'phone':mobileno,
            'token':token
        })
        token = r.json().get('data')
        codemsg = self.sms.getVcodeAndReleaseMobile(mobileno)
        codemsg = self.parseCodeMsg(codemsg)
        r = self.session.post(self.BASE_URL + '/web/invite/checkInviteRegister',{
            'phone':mobileno,
            'verifiCode':codemsg,
            'password':'pass2015',
            'invitePhone':invitephone, #大小写是个坑
            'token':token
        })
        if r.json().get('status') == 8:
            self.logger.info('Tongbanjie Register Successful')
        