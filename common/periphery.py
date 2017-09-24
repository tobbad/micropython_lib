#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Application layer which does the interpretation of high level packages.
    Created on 8.7.2016

    Packet looks as follows:
    | packet_type byte [One of Application.OPERATION] | data* N bytes

    OPERATIONS on server:
    OPEN: First datafield is one of Application.PERIPHERY
          rest of data is given to the constructor of the related low level
          device. A STATUS message is returned with the first data field as
          File descriptor (Byte value). The constructors for the supported devices
          is given as a factory to the constructor of the Application class.
    READ: First data field is the file descriptor obtained form open
          second data field is count of bytes
    WRITE: First data field is the file descriptor obtained form open
           Second ... nth data filed is data to write
    IOCTL: First data field is the file descriptor obtained form open
           Second...nth data field is controll information interpreted
           by the related low level device.
    CLOSE: First data field is the file descriptor obtained form open.
           The resources related to the file descriptor are released.

    Operation on the client:
    The low level device is calling the OPERATION functions

    Application on host <=> peri_stub (periphery = spi, i2c..) <=> Periphery <=> datalink host
                        <=> datalink device <=> Periphery <=> peri_stub <=> pyb.???

    peri_stub implements the basic open/read/write/ioctl/close interface and defines the constants
    of the specific device (E.G. spi specific stuff). To the host application it looks like e.g
    a pyb.SPI module and for the Periphery on the device it offers the open/read/write/ioctl/close
    interface.

    @author: Tobias Badertscher
"""
import struct


class Periphery:

    TYPE = {
        'SPI':1,
        'I2C':2
    }

    OPERATION = {
        'OPEN' : 1,
        'READ' : 2,
        'WRITE': 3,
        'IOCTL': 4,
        'CLOSE': 5,
    }

    STATUS = {
        'OK' : 0,
        'ERROR' : 1,
    }

    DEBUG = False

    def __init__(self, datalink, debug=False):
        ''' Constructor
        datalink: Datalink with minimal functions:
             read: Read available chars and return as list/tuple,
             write: Write list/tuple to the datalink
        debug: Either True or False: Output debug information.
        '''
        self.DEBUG = debug
        self.com = datalink
        self.do_run = True
        self.periphery = {}

    def _class_is_ok_for_register(self, p_class):
        needed = list(self.OPERATION.keys())
        for i in dir(p_class):
            if len(i)<2:
                continue
            if i[:2] == '__':
                continue
            if i.upper() in needed:
                needed.remove(i.upper())
        return len(needed)==0

    def register(self,  periphery_name,  periphery_class):
        ''' Register a class (periphery_class) as periphery_name
        to handle the periphery specific part of the communicatiion.

        Register must be done on the server side
        '''
        if not periphery_name in Periphery.TYPE:
            raise ValueError("Unknown periphery type %s" % (periphery_name))
        if not self._class_is_ok_for_register(periphery_class):
            raise ValueError("Class does not support needed interface.")
        self.periphery[periphery_name] = periphery_class

    def _do(self, request):
        if request[0] not in self.OPERATION.values():
            self.status(-1)


    def server(self):
        ''' While forever loop for a embedded device serving requests.
        '''
        while self.do_run:
            request = self.com.read()
            if request is None:
                continue
            self._do(request)

    def exit(self):
        self.do_run = False

    def open(self, periphery, data):
        pass

    def read(self,  file_desc):
        pass

    def write(self,  file_desc,  *data):
        pass

    def ioctl(self,  file_desc,  *data):
        pass

    def close(self,  file_desc):
        pass

    def status(self, data):
        data = [self.OPERATION['STATUS'], data]
        self.com.write(data)


