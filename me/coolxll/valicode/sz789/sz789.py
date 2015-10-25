#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-10-24

@author: Conan
'''

import ctypes
from os.path import join, dirname
from me.coolxll.valicode.IValidateCodeRecognize import AbstractValidatorRecognizer
from me.coolxll.valicode.sz789.config import username,password

dll = ctypes.windll.LoadLibrary(join(dirname(__file__),'dc.dll'))

class SZ789(AbstractValidatorRecognizer):
    
    def __init__(self):
        self.sz789 = dcVerCode(username, password)
        
    def rec_buf(self,filebuf):
        return self.sz789.recByte(filebuf)
    
    def rec_file(self, filepath):
        return self.sz789.recYZM(filepath)
    
    def reportError(self,imageId):
        return self.sz789.reportErrA(imageId)
class dcVerCode:
    #user QQ超人打码账号
    #pwd QQ超人打码密码
    #softId 软件ID 缺省为0,作者务必提交softId,以保证分成
    def __init__(self,user,pwd,softId="18162"):
        self.user = user
        self.pwd = pwd
        self.softId = softId

    #获取账号剩余点数
    #成功返回剩余点数
    #返回"-1"----网络错误
    #返回"-5"----账户密码错误
    def getUserInfo(self):
        p = dll.GetUserInfo(self.user,self.pwd)
        if p:
            return ctypes.string_at(p,-1)
        return ''

    #解析返回结果,成功返回(验证码,验证码ID),失败返回错误信息
    #点数不足:Error:No Money!
    #账户密码错误:Error:No Reg!
    #上传失败，参数错误或者网络错误:Error:Put Fail!
    #识别超时:Error:TimeOut!
    #上传无效验证码:Error:empty picture!
    #账户或IP被冻结:Error:Account or Software Bind!
    #软件被冻结:Error:Software Frozen!
    def parseResult(self,result):
        l = result.split('|')
        if len(l)==3:
            return (l[0],l[2])
        return (result,'')

    #recByte 根据图片二进制数据识别验证码,返回验证码,验证码ID
    #buffer 图片二进制数据
    def recByte(self,buf):
        p = dll.RecByte_A(buf,len(buf),self.user,self.pwd,self.softId)
        if p:
            s = ctypes.string_at(p,-1)
            return self.parseResult(s)
        return ''

    #recYZM 根据验证码路径识别,返回验证码,验证码ID
    #path 图片路径
    def recYZM(self,path):
        p = dll.RecYZM_A(path,self.user,self.pwd,self.softId)
        if p:
            s = ctypes.string_at(p,-1)
            return self.parseResult(s)
        return ''

    #reportErr 提交识别错误验证码
    #imageId 验证码ID
    def reportErr(self,imageId):
        dll.ReportError(self.user,imageId)

    #reportErr 提交识别错误验证码
    #返回"-1",提交失败,返回"1",提交成功
    def reportErrA(self,imageId):
        return dll.ReportError_A(self.user,imageId)
    
