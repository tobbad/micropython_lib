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
    '''
    This is the implemtation of the low level communication protocol
    between the server <-> client.
    
    We pack in following schema:
    
    PACKET_TYPE [4 Hi Bits] | FILE_DESC [4 Low Bits] (0 for open) | MSG_ID [4 Bit] | DATA_LENGTH [4 Bit] | DATA | CRC_OVER_LENGTH_AND_REST 
    
    FILE_DESC : Is an integer, returned by the client and identifies a certain end point.
    
    PACKET_TYPE : STATUS= 0,
                  OPEN  = 1,
                  READ  = 2,
                  WRITE = 3,
                  IOCTRL= 4,
                  CLOSE = 5,
                  ACK   = 6,
    IOCTRL DATA PACKAGE is interpreted by the individual endpoints (SPI/I2C...).
    
    Open establishes a connection to a certain endpoint. It calles the create function on 
    the hw_stub and returns a certain device.
    
    The minimal packet length is  2 bytes =  16 bits. 
    The maximal packet length is 17 bytes = 236 Bits
    '''

    SPI = 1
    I2C = 2
    GPIO = 3

    CRC_QUOTIENT = 0xD9     # This is the quotient for CRC-8 WCDMA 

    def __init__(self):
        self.__msg_id = 0
    
    
    def add_to_crc(self, byte, crc):
        b2 = byte
        if (byte < 0):
            b2 = byte + 256
        for i in range(8):
            odd = ((b2^crc) & 0x01) == 0x01
            crc >>= 1
            b2 >>= 1
            if (odd):
                crc ^= self.CRC_QUOTIENT 
        return crc

    def crc8(self, data):
        ''' Calculate CRC from polynom x^8+x^7+x^6+x^4+x^2+1
        '''
        crc = 0x00
        for byte in data:
            crc = self.add_to_crc(byte, crc)
            print(byte,crc)
        return crc
    

    def pack(self, pkt_type, data, file_desc=-1):
        ''' 
        Pack given data to format described above.
        
        Returns a bytearray.
        '''
        pass

    def unpack(self):
        ''' 
        Pack given data to format described above.
        
        Returns a bytearray.
        '''
        pkt_type, data, file_desc = 0,0,-1
        
        
        return pkt_type, data, file_desc
        

    def open(self, com):
        ''' Open a certain hw item for usage

        returns a class which knows what kind of hw device it is.
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





