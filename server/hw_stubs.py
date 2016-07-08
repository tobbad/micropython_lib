#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    HW server stubs for different HW items on python board.
    Created on 8.7.2016
    @author: Tobias Badertscher

"""

class server:

    def __init__(self):
        ''' Create USB_VCP device on the python board as
        server for the client on the PC.'''
        self.com = pyb.USB_VCP()
        if not self.com.isconnected():
            print("No client connected")
        # This is a raw data stream .. os disable the CTRL-C interrupt
        self._com.setinterrupt(-1)


