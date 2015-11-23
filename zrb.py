#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015年10月24日

@author: Conan
'''
from me.coolxll.site.zhenrongbao import Zhenrongbao
import logging
from me.coolxll.sms.f02.aima import Aima
from me.coolxll.sms.zmyzm.zhuoma import Zhuoma


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    times = 1
    for _ in xrange(times):
        #z = Zhenrongbao(sms=Aima()) #if need to use Aima as SMS
        sms = Zhuoma(3444) #3444 为真融宝的项目ID
        z = Zhenrongbao(sms) #Default sms platform change to Zhuoma
        #微信分享链接最后的地址，形如
        #http://activity.zhenrongbao.com/arecommendcoupon/newentry?sequence_id=4c164b29b0a09a512917b04a344d3b6d
        z.regwap('612fa1533d9b1685817807ecf4231223')
        
