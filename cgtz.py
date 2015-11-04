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
    times = 10
    for _ in xrange(times):
        cgtz = CGTZDZ()
        cgtz.setProxy()
        cgtz.dianzan('bjHnguB')