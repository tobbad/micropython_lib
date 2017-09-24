#!/usr/bin/env python
#
#

class SPI_stub:

    MSB = 1
    LSB = 2

    MASTER = 16
    SLAVE = 17

    class CONF:
        MODE = 1
        BAUDRATE = 2
        POLARITY = 3


    def __init__(self, bus=None):
        ''' Create a stub object to connect to the other side.
        If no bus is given start the server mode as soon as a
        com  is set.'''
        self.bus = bus
        self.com = None
        self.is_server = True if bus is None else False

    def com(selfself, datalink):
        self.com = datalink
        if self.is_server:
            self.server()

    def init(self, mode, baudrate=328125, polarity=1, phase=0, bits=8, firstbit=SPI.MSB, ti=False, crc=None):
        self.mode = mode
        self.baudrate=baudrate
        self.polarity= polarity
        self.phase= phase
        self.bits= bits
        self.firstbit=SPI.MSB
        self.ti= ti
        self.crc = crc

    def deinit(self)
        pass

    def recv(self, recv, timeout = 5000):
        pass

    def send(self, send, timeout = 5000):
        pass

    def send_recv(self, send, recv=None, timeout = 5000):
        pass



