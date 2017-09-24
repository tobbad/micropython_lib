#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Unit test stub module
#
import unittest
# DUT
from micropython_lib.common.periphery import Periphery
# Helper
from micropython_lib.mock.stack_datalink import Datalink
from micropython_lib.mock.stack_factory import Factory
import random
from mock import MagicMock

class Dum_Per:
    
    def __init__(self):
        pass
    
    def open(self):
        pass

    def read(self):
        pass

    def write(self):
        pass

    def ioctl(self):
        pass

    def close(self):
        pass

    def close(self):
        pass

class empty:
    
    pass


#@unittest.skip("Skipping control")
class CHECK_REGISTER(unittest.TestCase):

    DEBUG = False

    def setUp(self):
        self.datalink = Datalink()
        self.dut = Periphery(self.datalink)
        

    def test_register_not_existing_periphery_type(self):
        p_type = 42
        p_class = None
        self.assertRaises(ValueError,  self.dut.register, p_type,  p_class)

    def test_register_not_existing_class(self):
        p_type = 'SPI'
        p_class = None
        self.assertRaises(ValueError,  self.dut.register, p_type,  p_class)

    def test_register_class_with_necessary_functions_succeed(self):
        meth = ('open', 'read', 'write','ioctl','close')
        p_type = 'SPI'
        for i in range(2**len(meth)):
            self.mock = empty()
            for m_idx in range(5):
                if (i & (1<<m_idx)) != 0:
                    self.mock.__dict__[meth[m_idx]] = MagicMock()
            if i<31:
                self.assertRaises(ValueError,  self.dut.register, p_type,  self.mock)
            else:
                self.dut.register(p_type,  self.mock)


class CHECK_SERVER(unittest.TestCase):
    ''' Tests for checking if the server works correct:
    - Check if only correct commands are handled.
    - Check if EXIT command works.
    - Check open call on low level device.
    '''
    
    
    DEBUG = False
    
    def setUp(self):
        self.mock = empty()
        self.mock.open = MagicMock()
        self.mock.read = MagicMock()
        self.mock.write = MagicMock()
        self.mock.ioctl = MagicMock()
        self.mock.close = MagicMock()
        self.dut = Periphery(self.mock)
    
    def test_non_existing_operation(self):
        err_status = [self.dut.OPERATION['STATUS'],-1]
        test_data = [-1 ,max(self.dut.OPERATION.values())+1 ]
        self.mock.read = MagicMock()
        self.mock.read.return_value =test_data
        self.mock.write = MagicMock()
        for d in test_data:
            self.dut._do([d,])
            self.mock.write.assert_called_with(err_status)
        

if __name__ == '__main__':
    unittest.main()
