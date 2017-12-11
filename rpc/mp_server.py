# -*- coding: utf-8 -*-

import pyb
import ujson

class JRPC_SRV:
    
    __BUF_SIZE=100
    
    def __init__(self, com):
        self._com=com
        self._buf=bytearray(100)
        
        
    def _write(self, data):
        self._com.write(data)
        
    def _read(self, buffer):
        cnt=self._com.readinto(buffer)
        return cnt if cnt is not None else 0
    

    def start(self):
        self._write(b"")
        while True:
            cnt = self._read(self._buf)
            if cnt>0:
                self._write(self._buf)
                print("%d bytes data" % (cnt) )
            pyb.delay(1000)
            print("Tick")
        
