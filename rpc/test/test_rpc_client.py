# -*- coding: utf-8 -*-\
import sys
print(sys.path)
import unittest
from micropython_lib.rpc.mp_client import RPC_Client

class TestSerDes(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def teardown(self):
        pass

    def test_create(self):
        self.fail("Fail")

        
if __name__ == '__main__':
    unittest.main()