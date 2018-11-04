# -*- coding: utf-8 -*-
''' I2C driver for the MGC3130 used on the skywritter board.

    Part of the code is copied from the Raspberry Pi code for the
    skywritter-hat: https://github.com/pimoroni/skywriter-hat/

    Copyright (c) 2018 Baerospace
    MIT License
'''

from i2cspi import COM_I2C
from multibyte import multibyte
from time import sleep_ms
import pyb
from micropython import schedule

SW_ADDR = 0x42
SW_RESET_PIN = 17
SW_XFER_PIN = 27

SW_HEADER_SIZE = 4

SW_DATA_DSP = 0b0000000000000001
SW_DATA_GESTURE = 0b0000000000000010
SW_DATA_TOUCH = 0b0000000000000100
SW_DATA_AIRWHEEL = 0b0000000000001000
SW_DATA_XYZ = 0b0000000000010000

SW_SYSTEM_STATUS = 0x15
SW_REQUEST_MSG = 0x06
SW_FW_VERSION = 0x83
SW_SET_RUNTIME = 0xA2
SW_SENSOR_DATA = 0x91

class MGC3X30(COM_I2C, multibyte):
    
    def __init__(self, reset_pin, transfer_pin, communication, dev_selector):
        super().__init__(communication, dev_selector,
                         self.ADDR_MODE_8,
                         self.TRANSFER_MSB_FIRST)
        self._reset = reset_pin
        #self._trfr = pyb.ExtInt(transfer_pin.name(), pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, self._data_ready_cb)
        self.reset()
        
    def reset(self):
        self._reset.value(0)
        sleep_ms(100)
        self._reset.value(1)
        sleep_ms(500)
        
    def _poll(self):
        print("New data")
    
    def _data_ready_cb(self):
        ''' Called when ther is new data on the device.'''
        sleep_ms(1)
        #self._trfr.value(0)
        #self.com.read_binary(0, 26)
        #self._trfr.value(1)
        #schedule(self._poll)

        
