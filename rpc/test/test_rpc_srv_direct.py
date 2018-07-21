# -*- coding: utf-8 -*-
#
# (C) 2017 Tobias Badertscher <info@baerospace.ch>
#
# SPDX-License-Identifier:    BSD-3-Clause
import unittest
from serdes_json import SerDes
from common.datalink import Datalink
from rpc.pyb import dl_com
import json

ser_des = SerDes()

class TestRemoteServer(unittest.TestCase):

    COM_DEV='/dev/ttyACM0'
    DEBUG = False

    def setUp(self):
        self._com=dl_com(self.COM_DEV, baudrate=115200, timeout=1.0)
        self._com.reset_input_buffer()
        self._dl=Datalink(self._com)
        #self._dl.DEBUG=True
        self._serdes = ser_des

    def teardown(self):
        self._com.close()

    def test_method_call_OK(self):
        para=[1,]
        send_id, data = self._serdes.req_to_data("existing_function", para)
        self._dl.write(data)
        data = self._dl.read_str()
        self.assertIsNotNone(data)
        id_recv, result_obt, error_obt = self._serdes.data_to_resp(data)
        self.assertEqual(send_id, id_recv)
        self.assertEqual(result_obt, 'OK %s' % str(para[0]))
        self.assertEqual(error_obt, None)

    def test_call_mapped_function_OK(self):
        para=[1,]
        send_id, data = self._serdes.req_to_data("fun.mapped", para)
        self._dl.write(data)
        data = self._dl.read_str()
        self.assertIsNotNone(data)
        id_recv, result_obt, error_obt = self._serdes.data_to_resp(data)
        self.assertEqual(send_id, id_recv)
        self.assertEqual(result_obt, "map_fun_call %s" % str(para[0]))
        self.assertEqual(error_obt, None)

    def test_call_not_mapped_function_OK(self):
        para=[1,]
        send_id, data = self._serdes.req_to_data("function_not_mapped", para)
        self._dl.write(data)
        data = self._dl.read_str()
        self.assertIsNotNone(data)
        id_recv, result_obt, error_obt = self._serdes.data_to_resp(data)
        self.assertEqual(send_id, id_recv)
        self.assertEqual(result_obt, "Not_mapped_fun_call %s" % str(para[0]))
        self.assertEqual(error_obt, None)

    def test_method_call_mapped_method_OK(self):
        para=[42,]
        send_id, data = self._serdes.req_to_data("prop.get", para)
        self._dl.write(data)
        data = self._dl.read_str()
        self.assertIsNotNone(data)
        id_recv, result_obt, error_obt = self._serdes.data_to_resp(data)
        self.assertEqual(send_id, id_recv)
        self.assertEqual(result_obt, "prop(%s)" % str(para[0]))
        self.assertEqual(error_obt, None)

    def test_method_call_no_para_ok(self):
        send_id, data = self._serdes.req_to_data("existing_function_no_para")
        self._dl.write(data)
        data = self._dl.read_str()
        self.assertIsNotNone(data)
        id_recv, result_obt, error_obt = self._serdes.data_to_resp(data)
        self.assertEqual(send_id, id_recv)
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
        self.assertEqual(send_id, id_recv)
        self.assertIsNone(result_obt)
        self.assertEqual(id_recv, send_id)
        self.assertEqual(error_obt['code'], -32602)
        self.assertEqual(error_obt['message'], 'Invalid params')
        self.assertIsNone(error_obt['data'])

    def test_method_call_param_is_ctrlC(self):
        para=["\x03", ]
        send_id, data = self._serdes.req_to_data("existing_function", para)
        self._dl.write(data)
        data = self._dl.read_str()
        self.assertIsNotNone(data)
        id_recv, result_obt, error_obt = self._serdes.data_to_resp(data)
        self.assertEqual(send_id, id_recv)
        self.assertIsNone(error_obt)
        self.assertEqual(result_obt, 'OK %s' % str(para[0]))
        self.assertEqual(error_obt, None)

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

    def test_get_objects(self):
        send_id, data = self._serdes.req_to_data("system.listMethods")
        self._dl.write(data)
        data = self._dl.read_str()
        self.assertIsNotNone(data)
        id_recv, result_obt, error_obt = self._serdes.data_to_resp(data)
        self.assertEqual(send_id, id_recv)
        self.assertIsNotNone(result_obt)
        self.assertIsNone(error_obt)

    def test_get_stat_list(self):
        send_id, data = self._serdes.req_to_data("stat.list")
        self._dl.write(data)
        data = self._dl.read_str()
        self.assertIsNotNone(data)
        id_recv, result_obt, error_obt = self._serdes.data_to_resp(data)
        self.assertEqual(send_id, id_recv)
        self.assertIsNotNone(result_obt)
        self.assertIsNone(error_obt)

    def test_get_stat_prop_temp(self):
        send_id, data = self._serdes.req_to_data("stat.prop", 'temp')
        self._dl.write(data)
        data = self._dl.read_str()
        self.assertIsNotNone(data)
        id_recv, result_obt, error_obt = self._serdes.data_to_resp(data)
        self.assertEqual(send_id, id_recv)
        self.assertIsNotNone(result_obt)
        self.assertEqual(result_obt, 23.5)
        self.assertIsNone(error_obt)

    def test_send_any_char(self):
        for i in range(255):
            data = bytes([i])
            self._com.write(data)



if __name__ == '__main__':
    unittest.main(failfast=True)
