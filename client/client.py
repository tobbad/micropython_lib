#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Communication stub to talk with client on embedded side.
    Created on 9.7.2016
    @author: Tobias Badertscher

"""
import serial

class client:

    DEBUG = False
    ESC = None

    def __init__(self, com_dev_fname, debug = False):
        self.DEBUG=debug
        self._com = serial.Serial(com_dev_fname, timeout = 0.1)
        self._com.flushInput()

    def _l2str(self, data):
        hex_str = " ".join(["0x%02x" % (ord(i) ) for i in data])
        text_str = "".join(["%s" % (i if i.isalnum() else '.') for i in data])
        return hex_str +"\n" + text_str

    def clear_serial(self):
        data = 1
        while data:
            data=self._com.read()

    def read(self, cnt=10000):
        return self._com.read(cnt)

    def write(self, data):
        if self.DEBUG:
            bStr = " ".join(["0x%02x" % i for i in data])
            print("Send bytes: %s" % bStr)
        data = bytearray(data, 'latin-1')
        if self.ESC is None:
            self._com.write(data)
        else:
            for item in data:
                if item == self.ESC:
                    self._com.write(self.ESC)
                self._com.write(item)
        return

    def ioctl(self, cmd, data=None):
        self._com.write(self.ESC)
        self._com.write(cmd)
        self._com.write(len(data))
        self.write(data)

