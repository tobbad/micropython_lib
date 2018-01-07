#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Unit test stub module
#
import unittest
# DUT
from micropython_lib.common.datalink import Datalink
# Helper
from micropython_lib.mock.stack_phy import Phy
from micropython_lib.mock.helper import calc_crc
import crcmod.predefined
import struct
import random
from micropython_lib.rpc.pyb import dl_com


#@unittest.skip("Skipping control")
class CHECK_CONTROL(unittest.TestCase):

    DEBUG = False

    def setUp(self):
        self.phy = Phy()
        self.dut = Datalink(self.phy)

    def test_write_ack(self):
        self.phy.set_ack(self.dut)
        obt = self.dut.write([42, ])
        self.assertEqual(obt,  True)

    def test_write_nack(self):
        self.phy.set_nack(self.dut)
        obt = self.dut.write([42, ])
        self.assertEqual(obt,  False)

    def test_write_no_answer(self):
        retry_cnt = self.dut.retry_cnt
        obt = self.dut.write([42, ])
        self.assertIsNone(obt)
        self.assertEqual(self.phy.any_check_cnt, retry_cnt )



#@unittest.skip("Skipping write")
class CHECK_WRITE(unittest.TestCase):

    DEBUG = False

    def setUp(self):
        self.phy = Phy()
        self.data = [ random.randint(0,255) for i in range(10) ]
        self.dut = Datalink(self.phy)

    def test_crc_list(self):
        exp = calc_crc(self.data)
        obt = self.dut.crc(self.data)
        if self.DEBUG:
            print("Exp: 0x%02x Obtained: 0x%02x" % (exp, obt))
        self.assertEqual(obt, exp)

    def test_write_no_escape(self):
        for exp in range(256):
            if exp in self.dut.ESC_MAP.keys():
                continue
            self.phy.set_ack(self.dut)
            self.dut.write([exp, ])
            res = self.phy.get_written()
            exp_len = 5
            crc = calc_crc([exp,])
            if crc in self.dut.ESC_MAP.keys():
                exp_len+=1
            self.assertEqual(exp_len, len(res))
            self.assertEqual(res[0], self.dut.ESCAPE['SOF'])
            self.assertEqual(res[-1], self.dut.ESCAPE['EOF'])
            for e,o in zip([self.dut.PACKET_TYPE['DATA'], exp, ], res[1:-1]):
                self.assertEqual(e, o)

    def test_write_escape(self):
        for esc, val in self.dut.ESC_MAP.items():
            self.phy.set_ack(self.dut)
            self.dut.write([esc, ])
            res = self.phy.get_written()
            exp_len = 6
            crc = calc_crc([esc,])
            if crc in self.dut.ESC_MAP.keys():
                exp_len+=1
            self.assertEqual(exp_len, len(res))
            self.assertEqual(res[0], self.dut.ESCAPE['SOF'])
            self.assertEqual(res[1], self.dut.PACKET_TYPE['DATA'])
            self.assertEqual(res[2], val[0])
            self.assertEqual(res[3], val[1])
            self.assertEqual(res[-1], self.dut.ESCAPE['EOF'])

    def test_write_no_answer(self):
        val = 42
        state = self.dut.write([val, ])
        self.assertIsNone(state)


#@unittest.skip("Skipping read")
class CHECK_READ(unittest.TestCase):

    DEBUG = False

    def setUp(self):
        self.phy = Phy()
        self.data = [ random.randint(0,255) for i in range(10) ]
        self.dut = Datalink(self.phy)
        self.phy.set_ack(self.dut)
        self.dut.write([0x1B, ])
        self.phy_out = self.phy.get_written()

    def test_ignore_everything_before_sof(self):
        ignore_data = [41, 42, 43, 44,  0x04]
        self.phy.set_readable(ignore_data)
        self.phy.set_readable(self.phy_out)
        self.phy.set_ack(self.dut)
        #
        # Test
        #
        obt = self.dut.read()
        #
        # Evaluate
        #
        self.assertEqual(1, len(obt))

    def test_read_ack(self):
        for val in range(256):
            self.phy.clear()
            self.phy.set_ack(self.dut)
            self.dut.write([val, ])
            phy_out = self.phy.get_written()
            self.phy.set_readable(phy_out)
            #
            # Test
            #
            obt = self.dut.read()
            #
            # Evaluate
            #
            self.assertEqual(1, len(obt))
            for e,o in zip([val,], obt):
                self.assertEqual(e, o)
            ans_pkt = self.phy.get_written()
            self.assertEqual(ans_pkt[2], self.dut.STATES['ACK'])

    def test_read_corrupted_no_nack_or_ack(self):
        self.phy.clear()
        self.phy.set_ack(self.dut)
        self.dut.write([42, ])
        phy_out = self.phy.get_written()
        self.phy.set_readable(phy_out[0:-3])
        #
        # Test
        #
        obt = self.dut.read()
        #
        # Evaluate
        #
        ans_pkt = self.phy.get_written()
        self.assertIsNone(ans_pkt)
        self.assertIsNone(obt)

    def test_read_wrong_crc_nack(self):
        self.phy.set_ack(self.dut)
        self.dut.write([42, ])
        phy_out = self.phy.get_written()
        phy_out[-2]=0
        self.phy.set_readable(phy_out)
        #
        # Test
        #
        obt = self.dut.read()
        #
        # Evaluate
        #
        ans_pkt = self.phy.get_written()
        self.assertEqual(ans_pkt[2], self.dut.STATES['NACK'])
        self.assertIsNone(obt)

    def test_write_read_long(self):
        data = [i for i in range(256)]
        self.phy.clear()
        self.phy.set_ack(self.dut)
        self.dut.write(data)
        phy_out = self.phy.get_written()
        self.phy.set_readable(phy_out)
        #
        # Test
        #
        obt = self.dut.read()
        #
        # Evaluate
        #
        self.assertEqual(len(data), len(obt))
        for e,o in zip(data, obt):
            self.assertEqual(e, o)

    def test_echo(self):
        self.phy.set_readable(self.phy_out)
        #self.phy.set_ack(self.dut)
        self.dut.echo()

class Test_Remote(unittest.TestCase):

    SER_DEV='/dev/ttyACM0'
    
    def setUp(self):
        self._com=dl_com(self.SER_DEV, baudrate=115200)
        self._dl=Datalink(self._com)
    
    def teardown(self):
        self._com.close()
    
    def test_send_receive(self):
        data = "Hello world"
        self._dl.write(data)
        obt=self._dl.read_str()
        self.assertEqual(data, obt)

if __name__ == '__main__':
    unittest.main()
