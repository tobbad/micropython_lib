#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 21:16:59 2017

@author: badi
"""

import stm

class LLACC:
    ''' Class to allow more confortable low level access
    to register in the MCU. For each bit field in a register
    we therfore define a trippel:
        (ADDR, shift, mask)
    ADDR is the offset from the component base address
    shift describes how many positiont the bitfield has to be shifted down
          so that the bit filed lsb is shifted to bit 0
    mask defines the relevant bits in the register
         WHEN SHIFTED to the right till the lsb of the bit field
         is in bit 0 position.
          
    E.g. ADDR => |X|X|X|1|1|1|X|X| = (ADDR, 2, 0x07) 
    
    in the derived class the base address is defined as static variable
    BASE_ADDR.
    '''
    __value = None
    
    def register(self, desc, value=None):
        self.__value = stm.mem32[self.BASE_ADDR+desc[0]]
        if value is None:
            self.__value >>= desc[1]
            self.__value &= desc[2]
            return self.__value
        value &= desc[2]
        value <<+ desc[1]
        self.__value &= desc[2]<<desc[1]
        self.__value |= value
        stm.mem32[self.BASE_ADDR+desc[0]] = self.__value

class LCD(LLACC):
    
    BASE_ADDR = stm.LCD
    # 
    CR_BUFEN = (stm.LCD_CR, 8, 0x01)
    CR_MUX_SEG = (stm.LCD_CR, 7, 0x01)
    CR_BIAS = (stm.LCD_CR, 5, 0x03)
    CR_DUTY = (stm.LCD_CR, 2, 0x07)
    CR_VSEL = (stm.LCD_CR, 1, 0x01)
    CR_LCDEN = (stm.LCD_CR, 0, 0x01)
    FCR_PS = (stm.LCD_FCR, 22, 0x0F)
    FCR_DIV = (stm.LCD_FCR, 18, 0x0F)
    FCR_BLINK = (stm.LCD_FCR, 16, 0x03)
    FCR_BLINKF = (stm.LCD_FCR, 13, 0x07)
    FCR_CC = (stm.LCD_FCR, 10, 0x07)
    FCR_DEAD = (stm.LCD_FCR, 7, 0x07)
    FCR_PON = (stm.LCD_FCR, 4, 0x07)
    FCR_UDDIE = (stm.LCD_FCR, 3, 0x01)
    FCR_SOFIE = (stm.LCD_FCR, 1, 0x01)
    FCR_HD = (stm.LCD_FCR, 0, 0x01)
    SR_FCRSF =  (stm.LCD_SR, 5, 0x01)
    SR_RDY = (stm.LCD_SR, 4, 0x01)
    SR_UDD = (stm.LCD_SR, 3, 0x01)
    SR_UDR = (stm.LCD_SR, 2, 0x01)
    SR_SOF = (stm.LCD_SR, 1, 0x01)
    SR_ENS = (stm.LCD_SR, 0, 0x01)
    CLR_UDDC = (stm.LCD_CLR, 3, 0x01)
    CLR_SOFC = (stm.LCD_CLR, 1, 0x01)
    
    def __init__(self):
        self.register(self.FCR_PS, 0)
        self.register(self.FCR_DIV, 15)
        self.register(self.CR_DUTY, 3)
        self.register(self.CR_BIAS, 2)
        self.register(self.CR_VSEL, 0)
        self.register(self.FCR_CC, 5)
        self.register(self.FCR_DEAD, 0)
        self.register(self.FCR_PON, 4)
        self.register(self.FCR_HD, 0)
        self.register(self.FCR_BLINK, 0)
        self.register(self.FCR_BLINKF, 2)
        self.register(self.CR_MUX_SEG, 0)
    
    
        
        
    
    