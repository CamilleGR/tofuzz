# tofuzz/models/fuzzed_request.py

import sys, os, requests
from argparse import Namespace

class fuzzed_request :


    def __init__ (self, method, url, body=None,params={}, headers={},torConfig=None, FUZZ_TOKEN="FUZZ") :
        self.method = method
        self.url = url 
        self.headers=headers
        self.torConfig=torConfig
        self.params=params
        self.FUZZ_TOKEN=FUZZ_TOKEN
        if not torConfig :
            self.useTor= False  
        self.body = body # Don't filter by method to allow weird requests 
    
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    
    def __str__(self):
        reqstr = f"{self.method} {self.url}"+os.linesep
        for k,v in self.headers.items() :
            reqstr +=  f"{k} : {v}{os.linesep}" 
        reqstr += os.linesep
        reqstr += str(self.body) if self.body else os.linesep
        return reqstr
    
    def execute(self) : 
        try : 
            proxies = {}

            if self.torConfig : 
                 proxies = {
                    'http': f'socks5://{self.torConfig["adress"]}:{self.torConfig["socks_port"]}',
                    'https': f'socks5://{self.torConfig["adress"]}:{self.torConfig["socks_port"]}'
                }

            response = requests.request(
                method=self.method,
                url=self.url,
                headers=self.headers,
                data=self.body,
                proxies=proxies
            )
            return response
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return Namespace(status_code=-1, text=str(e))

    def fuzz_query(self, payload) : 
        self.url = self.url.replace(self.FUZZ_TOKEN, payload) 
    
    def fuzz_body(self, payload) : 
        if type(self.body) is str :
            self.body = self.body.replace(self.FUZZ_TOKEN, payload) 
        elif type(self.body) is dict :
            for k,v in self.body.items() : 
                if self.FUZZ_TOKEN in v : 
                    self.body[k] = self.body[k].replace(self.FUZZ_TOKEN, payload)