# -*- coding: utf-8 -*-
#
# Unit test for LoraWan MAC
#
import unittest

from micropython_lib.display.led_matrix  import LED_MATRIX
from mock.pyb.Pin import Pin

class DISPLAY_HW:

    def __init__(self):
        self.addr = list( Pin(i, ))


class Create(unittest.TestCase):

    def test_Create(self):
        modem = DUMMY_RF()
        lora = LORAWAN(modem)
        self.assertIsNotNone(lora)




if __name__ == '__main__':
    unittest.main()