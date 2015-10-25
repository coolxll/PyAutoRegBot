#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-10-24

@summary: Abstract Class of Validate Code Recognize

@author: Conan
'''
from abc import ABCMeta

class AbstractValidatorRecognizer(object):
    '''
    Base Class for valicode recognition
    '''
    __metaclass__ = ABCMeta

    def __init__(self, params):
        '''
        Constructor
        '''
        raise NotImplementedError('Unable to create abstract class')
    
    def rec_buf(self,filebuf):
        '''
        recognize by raw binary buf
        @return: valicode
        '''
        raise NotImplementedError('Unable to create abstract class')
    
    def rec_file(self,filepath):
        '''
        recognize by string file path
        @return: valicode
        '''
        raise NotImplementedError('Unable to create abstract class')