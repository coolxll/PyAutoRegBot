#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015年10月25日

@author: Conan
'''
from me.coolxll.site.tongbanjie import Tongbanjie
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    times = 1
    for i in xrange(times):
        try:
            logging.info('Registering {} times'.format(i+1))
            t = Tongbanjie()
            t.reg('http://account.tongbanjie.com/web/invite/inviteRegister.htm?b0PaT0xMDY0NjAyODcmcD0xODYyMTM2OTM4Mg==',
                  '18621369382')
        except Exception as e:
            logging.exception(e)
