#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015年10月24日

@author: Conan
'''
from me.coolxll.site.zhenrongbao import Zhenrongbao
import logging


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    times = 1
    z = Zhenrongbao()
    for _ in xrange(times):
        z.regwap('13812345678')
        
