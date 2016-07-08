#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    HW client stubs for different HW items on python board.
    Created on 8.7.2016
    @author: Tobias Badertscher

"""

from stub import SPI_Stub


class SPI(SPI_Stub):

    MSB = SPI_Stub.CTRL_FIRSTBIT_MSB
    LSB = SPI_Stub.CTRL_FIRSTBIT_LSB

    def __init__(self, bus, *para):
        pass

    def init(self, mode, baudrate=328125, prescaler=None, polarity=1, phase=0, bits=8, firstbit=SPI.MSB, crc=None):
        if prescaler != None:
            raise Exception("Not supported")
        if crc != None:
            raise Exception("Not supported")
        self.open(self.SPI)
        self.ioctl(self, self.CTRL_BAUDRATE, baudrate)
        self.ioctl(self, self.CTRL_POLARITY, polarity)
        self.ioctl(self, self.CTRL_PHASE, phase)
        self.ioctl(self, self.CTRL_BITS, bits)
        self.ioctl(self, self.CTRL_FIRSTBIT, firstbit)

    def recv(self, recv, timeout=5000):
        self.ioctl(self.CTRL_RECV_TIMEOUT, timeout)
        cnt = 0
        if isinstance(recv, int):
            cnt = recv
        elif isinstance(recv, (str, bytearray)):
            cnt = len(recv)
        else:
            raise Exception("Not supported type %s for recv" % (type(recv)))
        data = self.read(cnt)
        for idx,d in enumerate(data):
            recv[idx] = d
        return data


    def send(self, send, timeout=5000):
        self.ioctl(self.CTRL_RECV_TIMEOUT, timeout)
        data = []
        if isinstance(send, int):
            data = [recv,)
        elif isinstance(send, (list, tuple)):
            cnt = len(recv)
        else:
            raise Exception("Not supported type %s for recv" % (type(recv)))
        return self.write(data)

    def send_recv(self, send, recv=None, timeout=5000):
        self.ioctl(self.CTRL_RECV_TIMEOUT, timeout)
        self.send(send)
        if recv == None:
            return self.recv(send)
        else:
            return self.recv(recv)

