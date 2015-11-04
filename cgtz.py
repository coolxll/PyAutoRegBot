#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015年11月4日

@author: Conan
'''
import logging
from me.coolxll.site.cgtzdz import CGTZDZ

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    times = 3
    for _ in xrange(times):
        cgtz = CGTZDZ()
        #分享链接里面的最后几位
        #http://m.cgtz.com/activity/DBLElevenLike.html?shareuser=bjHnguB
        cgtz.dianzan('bjHnguB')