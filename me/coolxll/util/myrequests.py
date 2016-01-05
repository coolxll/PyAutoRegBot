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
    
    def setiPhoneUA(self):
        self.headers.update({'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4'})
    
    def setiPhoneWeixinUA(self):
        self.headers.update({'User-Agent':'mozilla/5.0 (iphone; cpu iphone os 5_1_1 like mac os x) applewebkit/534.46 (khtml, like gecko) mobile/9b206 micromessenger/5.0op'})
        
    def setProxy(self):
        #Fiddler Proxy for Debug usage
        proxies = {
              "http": "http://localhost:8899",
              "https": "http://localhost:8899",
            }
        self.proxies.update(proxies)
        self.verify = False
    
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
        self.last_url = url
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