#!/usr/bin/env python
#
# Main file for STM32F4DISCOVERY
#
from datalink import Datalink
import pyb

com = pyb.USB_VCP()
com.setinterrupt(-1)
dlink = Datalink(com)

def echo(cnt = -1):
    while cnt!=0:
        data = dlink.read()
        if data is None:
            pyb.delay(5)
        else:
            dlink.write(data)
        cnt -= 1

def recv(cnt = -1):
    while cnt!=0:
        dlink.read()
        cnt -= 1
  

def send():
    val=0
    while True:
        dlink.write(val)
        val = (val+1)%256
        pyb.delay(50)

echo(-1)    
