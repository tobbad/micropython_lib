# -*- coding: utf-8 -*-
#
# Unit test for LoraWan MAC
#
import unittest

from micropython_lib.lib.modem import RADIO_IF, LORAWAN

class DUMMY_RF(RADIO_IF):

    def __init__(self):
        super().__init__()


class Create(unittest.TestCase):

    def test_Create(self):
        modem = DUMMY_RF()
        lora = LORAWAN(modem)
        self.assertIsNotNone(lora)




if __name__ == '__main__':
    unittest.main()
