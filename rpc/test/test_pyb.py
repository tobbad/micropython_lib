# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import unittest
from rpc.mp_server import SerDes
from common.datalink import Datalink
from rpc.pyb import dl_com
import json

        
class TestRemoteServer(unittest.TestCase):
    
    COM_DEV='/dev/ttyACM0'
    
    def setUp(self):
        self._com=dl_com(self.COM_DEV, baudrate=115200, timeout=1.0)
        self._com.reset_input_buffer()
        self._dl=Datalink(self._com)
        #self._dl.DEBUG=True
        self._serdes = SerDes()
    
    def teardown(self):
        self._com.close()
        
    def test_method_call_OK(self):
        para=[1,]
        send_id, data = self._serdes.req_to_data("existing_function", para)
        self._dl.write(data)
        data = self._dl.read_str()
        self.assertIsNotNone(data)
        id_recv, result_obt, error_obt = self._serdes.data_to_resp(data)
        self.assertEqual(result_obt, 'OK %d' % para[0])
        self.assertEqual(error_obt, None)
        
    def test_method_call_no_para_ok(self):
        send_id, data = self._serdes.req_to_data("existing_function_no_para")
        self._dl.write(data)
        data = self._dl.read_str()
        self.assertIsNotNone(data)
        id_recv, result_obt, error_obt = self._serdes.data_to_resp(data)
        self.assertIsNone(error_obt)
        self.assertEqual(result_obt, 'OK')
        self.assertEqual(error_obt, None)
        
    def test_method_call_param_not_OK(self):
        para=[1,2]
        send_id, data = self._serdes.req_to_data("existing_function", para)
        self._dl.write(data)
        data = self._dl.read_str()
        self.assertIsNotNone(data)
        id_recv, result_obt, error_obt = self._serdes.data_to_resp(data)
        self.assertIsNone(result_obt)
        self.assertEqual(id_recv, send_id)
        self.assertEqual(error_obt['code'], -32602)
        self.assertEqual(error_obt['message'], 'Invalid params')
        self.assertIsNone(error_obt['data'])
        
    def test_call_not_existing_function(self):
        send_id, data = self._serdes.req_to_data("not_existing_function", (1,))
        self._dl.write(data)
        data = self._dl.read_str()
        self.assertIsNotNone(data)
        id_recv, result_obt, error_obt = self._serdes.data_to_resp(data)
        self.assertEqual(result_obt, None)
        self.assertEqual(id_recv, send_id)
        self.assertEqual(error_obt['code'], -32601)
        self.assertEqual(error_obt['message'], 'Method not found')
        self.assertIsNone(error_obt['data'])

    def test_not_valid_json(self):
        methodName='print'
        exp_params=[1,2,"42"]
        jdata={'jsonrpc':'1.0', 'method':methodName, 'params':exp_params}
        data=json.dumps(jdata)
        self._dl.write(data)
        data = self._dl.read_str()
        self.assertIsNotNone(data)
        id_recv, result_obt, error_obt = self._serdes.data_to_resp(data)
        self.assertEqual(result_obt, None)
        self.assertEqual(error_obt['code'], -32700)
        self.assertEqual(error_obt['message'], 'Parse error')
        self.assertIsNone(error_obt['data'])

    def test_dir(self):
        send_id, data = self._serdes.req_to_data("get_objects")
        self._dl.write(data)
        data = self._dl.read_str()
        self.assertIsNotNone(data)
        id_recv, result_obt, error_obt = self._serdes.data_to_resp(data)
        
if __name__ == '__main__':
    unittest.main()