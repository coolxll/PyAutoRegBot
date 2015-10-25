#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015年10月25日

@author: Conan
'''
from me.coolxll.site.tongbanjie import Tongbanjie
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    times = 1
    for _ in xrange(times):
        t = Tongbanjie()
        t.reg('http://account.tongbanjie.com/web/invite/inviteRegister.htm?b0PaT0xMDY0NjAyODcmcD0xODYyMTM2OTM4Mg==',
              '13800000000')