#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest
# DUT
from micropython_lib.lib.port import Port
from unittest.mock import MagicMock

class Pin:
    
    PULL_NONE = 16
    IN  = 0
    OUT_PP =1

    def __init__(self, port, pin):
        self._port = port
        self._pin = pin
        self._value = 0
        self._mode = 255

    def value(self, value = None):
        if value is not None:
            self._value = 1 if value > 0 else 0
        else: 
            return self._value

    def init(self, mode, pull=PULL_NONE, af=-1):
        self._mode = mode
     
    def mode(self):
        return self._mode
        
        
    def pvalue(self):
        return self.value()*1<<self._pin

    def __str__(self):
        pass

#@unittest.skip("Skipping control")
class CHECK_CREATE(unittest.TestCase):

    DEBUG = False

    def test_create_8(self):
        pins = tuple(Pin(0,0) for i in range(8))
        port = Port(pins)
        self.assertNotEqual(port,  None)

    def test_create_16(self):
        pins = tuple(Pin(0,0) for i in range(16))
        port = Port(pins)
        self.assertNotEqual(port,  None)

    def test_create_not_8_16(self):
        for i in range(32):
            if i in (8,16):
                continue
            pins = tuple(Pin(0,0) for i in range(i))
            self.assertRaises(Exception,  Port, pins)

class CHECK_READ(unittest.TestCase):

    DEBUG = False

    def _set_pin(self, size, value):
        pins = []
        for i in range(size):
            pin = Pin(0, i)
            pin.value(value & 0x01)
            value >>= 1
            pins.append(pin)
        return pins

    def check_pin_modes(self, pins, exp_mode):
        modes = [ p.mode() is exp_mode for p in pins]
        return all(modes)
        

    def setUp(self):
        pass


    def test_read_match_8(self):
        for i in range(256):
            pins = self._set_pin(8, i)
            port = Port(pins)
            port.mode(Port.READ)
            res = port.read()
            self.assertEqual(res, i)
            self.assertEqual(self.check_pin_modes(pins, Pin.IN), True)

    def test_read_match_16(self):
        for i in range(16):
            pins = self._set_pin(16, 1<<i)
            port = Port(pins)
            port.mode(Port.READ)
            res = port.read()
            self.assertEqual(res, 1<<i)
            self.assertEqual(self.check_pin_modes(pins, Pin.IN), True)

class CHECK_WRITE(unittest.TestCase):

    DEBUG = False

    def check_pins(self):
        value = 0
        for p in self._pins:
            value+= p.pvalue()
        return value

    def create_pins(self, size):
        self._pins = []
        for i in range(size):
            self._pins.append(Pin(0, i))
        return

    def check_pin_modes(self, pins, exp_mode):
        modes = [ p.mode() is exp_mode for p in pins]
        return all(modes)


    def clear_pins(self):
        for p in self._pins:
            p.value(0)
        return


    def test_write_match_8(self):
        self.create_pins(8)
        port = Port(self._pins)
        port.mode(Port.WRITE)
        for i in range(256):
            self.clear_pins()
            port.write(i)
            res = self.check_pins()
            self.assertEqual(res, i)
            self.assertEqual(self.check_pin_modes(self._pins, Pin.OUT_PP), True)

    def test_write_match_16(self):
        self.create_pins(16)
        port = Port(self._pins)
        port.mode(Port.WRITE)
        for i in range(16):
            self.clear_pins()
            port.write(1<<i)
            res = self.check_pins()
            self.assertEqual(res, 1<<i)
            self.assertEqual(self.check_pin_modes(self._pins, Pin.OUT_PP), True)

if __name__ == '__main__':
    unittest.main()
