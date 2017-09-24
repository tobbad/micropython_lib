#!/usr/bin/python3
# -*- coding: utf-8 -*-
import struct
from micropython_lib.common.datalink import Datalink
from micropython_lib.mock.helper import calc_crc

class Phy:

    DEBUG = False

    def __init__(self, debug = False):
        self.DEBUG = debug
        self.clear()
    #
    # Official minimal communication  interface
    #
    def read(self):
        data = self.from_data.pop(-1)
        self.read_cnt += 1
        if self.DEBUG:
            print("Read data from dummy ", data)
        return data

    def write(self, data):
        if not isinstance(data,  (bytes,  bytearray)):
            raise TypeError("object with buffer protocol required")
        if self.DEBUG:
            print("New data to phy ", data)
        self.to_data.insert(0, data)

    def any(self):
        self.any_check_cnt += 1
        return len(self.from_data)>0
    #
    # Helper/Mock functions
    #
    def clear(self):
        self.to_data = [] # Data to the physical layer
        self.from_data = [] # Data from the physical layer
        self.read_cnt = 0
        self.any_check_cnt = 0

    def set_state(self, dut, state):
        res = [Datalink.ESCAPE['SOF'], Datalink.PACKET_TYPE['CONTROL'], Datalink.STATES[state]]
        crc = calc_crc([dut.STATES[state],])
        crc = dut.ESC_MAP.get(crc, [crc,])
        res.extend(crc)
        res.append(Datalink.ESCAPE['EOF'])
        self.set_readable(res)

    def set_ack(self, dut):
        self.set_state(dut,'ACK')

    def set_nack(self, dut):
        self.set_state(dut,'NACK')

    def get_written(self):
        data = None
        if len(self.to_data)>0:
            data = self.to_data.pop(-1)
            fmt = "%dB" % len(data)
            data = list(struct.unpack(fmt, data))
        return data

    def get_all_written(self):
        res = []
        data = self.get_written()
        while data is not None:
            res.append(data)
            data = self.get_written()
        return res

    def set_readable(self, data):
        if self.DEBUG:
            print("Set data %s" % str(data))
        fmt = "%dB" % len(data)
        data = struct.pack(fmt, *data)
        self.from_data.insert(0, data)

    def __str__(self):
        res =  ("Status of dummy",)
        for idx, item in enumerate(self.from_data):
            res += ("From data[%2d]: %s" % (idx, ", ".join(["0x%02x" % i for i in item])),)
        for idx, item in enumerate(self.to_data):
            res += ("To data  [%2d]: %s" % (idx, ", ".join(["0x%02x" % i for i in item])),)
        return "\n".join(res)
