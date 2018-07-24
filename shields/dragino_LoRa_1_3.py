#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Dragino LoRa Shield v 1.3 
    Created on 10.5.2018
    @author: Tobias Badertscher

"""
import pyb

conf={}

config= {'NUGLEO_L476RG':{  
        # SPI must connected with SV2/3/4 to the arduino connector:
        # Jumpers must plugged in on the left side.
        'spi':{'spi_bus':1, 'spi_cs':'PB6',  'resetPin':'PC7', 'spi_polarity':0 , 'spi_phase':0},
        # Following are ARDUINO pin names 
        # and must be mapped to the boards 
        # real port name
        'DI0':{'a_pin':'D2', 
              'name':'DI0',
              'mode':pyb.Pin.IN,
              'pull':pyb.Pin.PULL_NONE},
        'DI1':{'a_pin':'D6', 
              'name':'DI1',
              'mode':pyb.Pin.IN,
              'pull':pyb.Pin.PULL_NONE},
        'DI2':{'a_pin':'D7', 
              'name':'DI2',
              'mode':pyb.Pin.IN,
              'pull':pyb.Pin.PULL_NONE},
        'DI5':{'a_pin':'D8', 
              'name':'DI5',
              'mode':pyb.Pin.IN,
              'pull':pyb.Pin.PULL_NONE},
        }
    }