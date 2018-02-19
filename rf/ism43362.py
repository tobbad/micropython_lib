# -*- coding: utf-8 -*-
#
# Driver for the ISM43362 WIFI moduel from Inventek Systems
# http://www.inventeksys.com/products-page/wifi-modules/ism4336-m3g-l44-e-embedded-serial-to-wifi-module/
# This is an AT command controlled WIFI module

import pyb


class ISM43362:

    END_OF_CMD = '\r'
    POST_PAD_TX_BYTE = '\n'
    POST_PAD_RX_BYTE = '\r'
    DEBUG = True
    BUFSIZE = 32
    TIMEOUT = 10

    def __init__(self, communication, dev_selector, reset, ready, wakeup):
        self._com = communication
        self._sel = dev_selector
        self._sel.value(1)
        self._reset = reset
        self._wakeup = wakeup
        self._ready = ready
        self._buf = bytearray(self.BUFSIZE)
        self._timeout_ms = self.TIMEOUT
        #self.init()

    def wakeup(self):
        self._wakeup.value(1) # edge triggered
        pyb.delay(10)
        self._wakeup.value()

    def reset(self):
        self._reset.value(0)
        pyb.delay(10)
        self._reset.value(1)
        pyb.delay(500)

    def enable(self):
        self._sel.value(0)
        pyb.delay(10)

    def disable(self):
        self._sel.value(1)
        pyb.delay(10)

    def isCmdDataReady(self):
        return self._ready.value()==1

    def waitForReady(self, timeout):
        tickstart = pyb.milis()
        while not self.isCmdDataReady():
            if (pyb.milis()-tickstart)> timeout:
                return -1
        return 0

    def flushRxFifo(self):
        while self._com.any():
            self._com.read(1)

    def init(self):
        ''' As done in the mbed project for wifi communication '''
        self.reset()
        self.wakeup()
        self.enable()
        cnt=0
        data=()
        while self.isCmdDataReady():
            tmp=self._com.send_recv(self._buf, timeout=self._timeout_ms)
            if self.DEBUG:
                print("Init rx %s" % tmp)
            data+= tmp[0], tmp[1]
        if self.DEBUG:
            print("Init RX finished %s " % data)
        if len(data)<6:
            return -1
        if (data[0] != 0x15) or (data[1] != 0x15) or \
           (data[2] != '\r') or (data[3] != '\n') or \
           (data[4] != '>' ) or (data[5] != ' '):
            self.disable()
            return -1
        self.disable()
        return 0

    def write(self, data, timeout=10):
        if len(data)%2==1:
            data+=self.POST_PAD_TX_BYTE
        if self.waitForReady(timeout)<0:
            return -1
        if self.DEBUG:
            print("SPI Send %s" % data)
        self.enable()
        self._com.send(data, timeout)
        self.disable()
        return len(data)

    def read(self, buffer, timeout=10):
        tmp = bytearray(2)
        length = len(buffer)
        bIdx=0
        tickstart = pyb.milis()
        self.flushRxFifo()
        self.disable()
        if self.waitForReady(timeout)<0:
            return -1
        self.enable()
        while self.isCmdDataReady():
            self._com.recv(tmp, timeout=timeout)
            if self.DEBUF:
                print("SPI Recived %s" % tmp )
            if tmp[1] == 0x15:
                pyb.delay(1)
            if not self.isCmdDataReady():
                if tmp[1] == 0x15:
                    if bIdx < length:
                        buffer[bIdx] = tmp[0]
                    else:
                        self.disable()
                        return -1
                    bIdx +=1
                    break
            if bIdx+1 < length:
                buffer[bIdx] = tmp[0]
                buffer[bIdx+1] = tmp[1]
                bIdx+=2
            else:
                self.disable()
                return -1
            if (pyb.milis()-tickstart > timeout):
                self.disable()
                return -1
        self.disable()
        if self.DEBUG:
            print("SPI finished rx: %s" % buffer[0:bIdx] )
        return bIdx

    def ATCmd(self, cmd, rBuffer):
        cmd+= self.END_OF_CMD
        if self.write(cmd) > 0:
            return self.read(rBuffer)
        return -1
