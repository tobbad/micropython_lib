# -*- coding: utf-8 -*-
#
# Unit test stub module
#
import unittest
# DUT
from micropython_lib.common.stub import Stub
# Helper
import crcmod.predefined
import struct
import random


class CHECK_CRC(unittest.TestCase):
    
   
    DEBUG = True
    
    def setUp(self):
        self.data = [ random.randint(0,255) for i in range(10) ]
        self.dut = Stub()
        self.crc8 = crcmod.predefined.mkCrcFun('crc-8-wcdma')

    def test_crc8_list(self):
        fmt = ("%dB" % len(self.data))
        data_bin = struct.pack(fmt, *self.data)
        exp = self.crc8(data_bin)
        obt = self.dut.crc8(self.data)
        if self.DEBUG:
            print("Exp: 0x%02x Obtained: 0x%02x" % (exp, obt))
        self.assertEqual(obt, exp)



if __name__ == '__main__':
    unittest.main()
