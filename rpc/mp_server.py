# -*- coding: utf-8 -*-

import pyb
import ujson

class JRPC_SRV:
    
    __BUF_SIZE=100
    
    def __init__(self, com):
        self._com=com
        
    def _write(self, data):
        self._com.write(data)
        
    def _read(self):
        data=self._com.read()
        return data
    
    def start(self):
        self._write(b"")
        while True:
            buf = self._read()
            if buf is not None:
                self._write(buf)
                #print("%d bytes data." % (len(buf)) )
            #pyb.delay(1000)
            #print("Tick")
        
