#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015年10月24日

@author: Conan
'''
from requests.sessions import Session

class CustomSession(Session):
    '''
    classdocs
    '''
    
    last_url = ''
    
    def __init__(self):
        '''
        Constructor
        '''
        super(CustomSession, self).__init__()
        
    def setChromeUA(self):
        self.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'})
    
    def request(self, method, url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None):
        #Automatically Add Referer
        if self.last_url:
            self.headers.update({'Referer':self.last_url})
        return super(CustomSession, self).request(method, url,
                                                  params,
                                                  data,
                                                  headers,
                                                  cookies,
                                                  files,
                                                  auth,
                                                  timeout,
                                                  allow_redirects,
                                                  proxies,
                                                  hooks,
                                                  stream,
                                                  verify,
                                                  cert,
                                                  json)
        self.last_url = url
