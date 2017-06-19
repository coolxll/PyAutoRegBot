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
from me.coolxll.sms.iyylw.shenma import Shenma
from me.coolxll.sms.shjmpt.shenhua import Shenhua
from me.coolxll.sms.ninemli.jiuma import JiuMa

if __name__ == '__main__':
    logfile = open('zhenrongbao_no.log','ab')
    logging.basicConfig(level=logging.DEBUG)
    times = 2
    for _ in xrange(times):
        #z = Zhenrongbao(sms=Aima()) #if need to use Aima as SMS
        sms = Shenhua(1731)
        z = Zhenrongbao(sms) #Default sms platform change to Zhuoma
        # z.session.setProxy()
        #18916550925 612fa1533d9b1685817807ecf4231223
        #18621369382 4c164b29b0a09a512917b04a344d3b6d
#         mobileno = z.regwap('612fa1533d9b1685817807ecf4231223') #zlf
#         logfile.write(mobileno + ',')
#         mobileno = z.regwap('4c164b29b0a09a512917b04a344d3b6d') #xll
#         logfile.write(mobileno + ',')
        z.session.verify=False 
        mobileno = z.reg(18621369382)
        logfile.write(mobileno + '\r\n')
    logfile.close()
        
