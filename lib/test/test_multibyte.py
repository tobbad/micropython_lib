#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest
# DUT
from micropython_lib.lib.multibyte import multibyte
from unittest.mock import MagicMock
import struct

class CHECK_READ(unittest.TestCase):

    DEBUG = False
        

    def setUp(self):
        self.dut = multibyte(None, None, None, True)
        self.dut.read_binary = MagicMock(name="read_binary")
        #reg_addr, cnt)

    def test_read_u8(self):
        ret_val = (0x42,)
        self.dut.read_binary.return_value = ret_val
        val = self.dut.read_u8(0)
        self.assertEqual(val, ret_val[0])

    def test_read_s8(self):
        ret_val = (0x80,)
        self.dut.read_binary.return_value = ret_val
        obt_val = self.dut.read_s8(0)
        exp_val = struct.unpack("b", struct.pack("B", ret_val[0]))[0]
        self.assertEqual(exp_val, obt_val)

    def test_read_u16(self):
        ret_val = (0x12, 0x34)
        self.dut.read_binary.return_value = ret_val
        val = self.dut.read_u16(0)
        self.assertEqual(val, ret_val[0]+256*ret_val[1])

    def test_read_u16_r(self):
        ret_val = (0x12, 0x34)
        self.dut.read_binary.return_value = ret_val
        val = self.dut.read_u16_r(0)
        self.assertEqual(val, ret_val[1]+256*ret_val[0])

    def test_read_s16(self):
        exp_val =  -2345
        data = struct.pack('h', exp_val)
        self.dut.read_binary.return_value = (data[0], data[1])
        obt_val = self.dut.read_s16(0)
        self.assertEqual(exp_val, obt_val)

    def test_read_u24(self):
        exp_val = (0x12, 0x34, 0x56)
        self.dut.read_binary.return_value = exp_val
        val = self.dut.read_u24(0)
        self.assertEqual(val, exp_val[0]+256*(exp_val[1]+256*exp_val[2]))

    def test_read_u24_r(self):
        exp_val = (0x12, 0x34, 0x56)
        self.dut.read_binary.return_value = exp_val
        val = self.dut.read_u24_r(0)
        self.assertEqual(val, exp_val[2]+256*(exp_val[1]+256*exp_val[0]))

    def test_read_s24(self):
        exp_val =  -234543
        data = struct.pack('i', exp_val)
        self.dut.read_binary.return_value = (data[0], data[1], data[2])
        obt_val = self.dut.read_s24(0)
        self.assertEqual(exp_val, obt_val)

    def test_read_u32(self):
        exp_val = (0x12, 0x34, 0x56, 0x78)
        self.dut.read_binary.return_value = exp_val
        val = self.dut.read_u32(0)
        self.assertEqual(val, exp_val[0]+256*(exp_val[1]+256*(exp_val[2]+256*exp_val[3])))

    def test_read_u32_r(self):
        exp_val = (0x12, 0x34, 0x56, 0x78)
        self.dut.read_binary.return_value = exp_val
        val = self.dut.read_u32_r(0)
        self.assertEqual(val, exp_val[3]+256*(exp_val[2]+256*(exp_val[1]+256*exp_val[0])))

    def test_read_s32(self):
        exp_val =  -234543
        data = struct.pack('i', exp_val)
        self.dut.read_binary.return_value = (data[0], data[1], data[2], data[3])
        obt_val = self.dut.read_s32(0)
        self.assertEqual(exp_val, obt_val)

class CHECK_WRITE(unittest.TestCase):

    DEBUG = False
        

    def setUp(self):
        self.dut = multibyte(None, None, None, True)
        self.dut.write_binary = MagicMock(name="write_binary")
        #reg_addr, cnt)


    def test_write_u8(self):
        exp_val = 0x42
        line_val = struct.pack('B', exp_val)
        self.dut.write_u8(0, exp_val)
        self.dut.write_binary.assert_called_once_with(0, line_val)

    def test_write_s8(self):
        exp_val = -100
        line_val = struct.pack('b', exp_val)
        self.dut.write_s8(0, exp_val)
        self.dut.write_binary.assert_called_once_with(0, line_val)

    def test_write_u16(self):
        exp_val = 0x12*256+0x34
        line_val = struct.pack('H', exp_val)
        lvstr="["+ ", ".join(["0x%02x" %i for i in line_val]) + "]"
        print(lvstr)
        self.dut.write_u16(0, exp_val)
        self.dut.write_binary.assert_called_once_with(0, line_val)

    def test_write_u16_r(self):
        exp_val = 0x12*256+0x34
        line_val = struct.pack('H', 0x12+0x34*256)
        lvstr="["+ ", ".join(["0x%02x" %i for i in line_val[::-1]]) + "]"
        self.dut.write_u16_r(0, exp_val)
        self.dut.write_binary.assert_called_once_with(0, line_val)


if __name__ == '__main__':
    unittest.main()
