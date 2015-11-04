#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015年11月4日

@author: Conan
'''
from me.coolxll import sms
from me.coolxll.sms.zmyzm.zhuoma import Zhuoma
from me.coolxll.util.myrequests import CustomSession
import logging
import re

class CGTZDZ(object):
    '''
    草根投资双11点赞活动
    '''
    
    BASE_URL = 'http://m.cgtz.com'
    CGTZDZ_ZHUOMA_PID = 813
    logger = logging.getLogger(__name__)
    def __init__(self, sms = None):
        '''
        '''
        self.session = CustomSession()
        self.session.setiPhoneUA()
        self.session.headers.update({
            'X-Requested-With':'XMLHttpRequest'})
        self.sms = Zhuoma()
        
    def parseCodeMsg(self,codemsg):
        pattern = re.compile(u'验证码：(?P<vmsg>\d{6})')
        result = re.search(pattern, codemsg)
        if result:
            return result.group("vmsg")
        return ""
        
    def dianzan(self,user):
        mobileno = self.sms.getMobileNum(self.CGTZDZ_ZHUOMA_PID)
        self.session.post(self.BASE_URL + '/activity/MobileDBLEleven.html', 
        {'user':user,'mobile':mobileno})
        r = self.session.post(self.BASE_URL + '/site/getvcode.html',{'mobile':mobileno})
        if r.json().get('success') == 1:
            self.logger.debug(r.json())
            self.logger.info(u'消息发送至{}成功'.format(mobileno))
        codemsg = self.sms.getVcodeAndReleaseMobile(mobileno)
        codemsg = self.parseCodeMsg(codemsg)
        self.logger.debug(u'验证码为{}'.format(codemsg))
        r = self.session.post(self.BASE_URL + '/activity/DoDBLElevenLike.html',
                          {'user':user,'mobile':mobileno,'code':codemsg})
        if r.json().get('success') == 1:
            self.logger.info(u'点赞成功')
        else:
            logging.info(r.json().get('msg'))