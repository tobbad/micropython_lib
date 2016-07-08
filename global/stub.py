#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    General definitions for server and client
    Created on 8.7.2016
    @author: Tobias Badertscher

"""


class HW:

    SPI = 1
    I2C = 2
    GPIO =3


class Stub:

    SPI = 1
    I2C = 2
    GPIO = 3

    def __init__(self):
        pass

    def open(self, com):
        ''' Open a certain hw item for usage

        returns a class which knows qhat kind of hw device it is.
        '''
        raise ValueError("Must be implemented in derived class")

    def ioctl(self, ctl_item, value=None):
        '''Function for setting (if value !+None) or getting
        if value == None) certain control status on the hw
        device '''
        raise ValueError("Must be implemented in derived class")

    def read(self, cnt):
        ''' Read cerain count of bytes from device'''
        raise ValueError("Must be implemented in derived class")

    def write(self, data):
        ''' Write the given byte buffer to the hw device.'''
        raise ValueError("Must be implemented in derived class")

    def close(self):
        ''' Close the given hw_device on the server'''
        raise ValueError("Must be implemented in derived class")


class SPI_Stub(Stub):

    CTRL_MASTER = 0
    CTRL_SLAVE = 1
    CTRL_BAUDRATE = 2
    CTRL_POLARITY = 3
    CTRL_PHASE = 4
    CTRL_BITS = 5
    CTRL_FIRSTBIT = 6
    CTRL_FIRSTBIT_MSB = 7
    CTRL_FIRSTBIT_LSB = 8
    CTRL_RECV_TIMEOUT = 9





