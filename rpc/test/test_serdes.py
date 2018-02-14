# -*- coding: utf-8 -*-
import json
import unittest
from micropython_lib.rpc.serdes_json import SerDes
from micropython_lib.common.datalink import Datalink
from micropython_lib.rpc.pyb import dl_com

class TestJsonSerDes(unittest.TestCase):
    
    def setUp(self):
        self.serdes = SerDes()
    
    def teardown(self):
        pass
        
    #
    # Test request object
    #
    def test_req2j_no_data(self):
        methodName = "Blabla"
        req_id, res = self.serdes.req_to_data("Blabla")
        self.assertIsInstance(res, str)
        jres=json.loads(res)
        self.assertEqual(jres['jsonrpc'],"2.0")
        self.assertEqual(jres['id'],0)
        self.assertEqual(jres['method'],methodName)
        self.assertIsInstance(jres['params'], list)

    def test_req2j_id_increment(self):
        methodName = "Blabla"
        req_id, res = self.serdes.req_to_data(methodName)
        jres=json.loads(res)
        self.assertEqual(jres['id'],0)
        req_id, res = self.serdes.req_to_data(methodName)
        jres=json.loads(res)
        self.assertEqual(jres['id'],1)
         
    def test_req2j_one_int(self):
        methodName = "Blabla"
        value = 1
        req_id, res = self.serdes.req_to_data(methodName, value)
        self.assertIsInstance(res, str)
        jres=json.loads(res)
        self.assertEqual(jres['jsonrpc'],"2.0")
        self.assertEqual(jres['method'],methodName)
        self.assertIsInstance(jres['params'], list)
        self.assertEqual(jres['params'][0], value)
        
    def test_req2j_serveral_primitiv_data(self):
        methodName = "Blabla"
        value = (1, 3.5, "abcd")
        req_id, res = self.serdes.req_to_data(methodName, value)
        self.assertIsInstance(res, str)
        jres=json.loads(res)
        self.assertEqual(jres['jsonrpc'],"2.0")
        self.assertEqual(jres['method'],methodName)
        self.assertIsInstance(jres['params'], list)
        for exp, opt  in zip(value, jres['params']):
            self.assertEqual(exp, opt)
        
    def test_req2j_serveral_primitiv_and_list(self):
        methodName = "Blabla"
        value = (1, 3.5, [1,2,3], "hhello")
        req_id, res = self.serdes.req_to_data(methodName, value)
        self.assertIsInstance(res, str)
        jres=json.loads(res)
        self.assertEqual(jres['jsonrpc'],"2.0")
        self.assertEqual(jres['method'],methodName)
        self.assertIsInstance(jres['params'], list)
        for exp, opt  in zip(value, jres['params']):
            self.assertEqual(exp, opt)
            
    def test_req2j_object(self):
        class simple:
            def __init__(self):
                pass
        inst = simple()
        res = self.serdes.resp_to_data(inst)
        self.assertIsNone(res)        
        
        
    #
    # Test responce to data conversion
    #
    def test_rsp2j_reponse_and_error(self):
        res = self.serdes.resp_to_data(0, 1 ,1)
        self.assertIsNone(res)        
        
    def test_rsp2j_reponse(self):
        res = self.serdes.resp_to_data(0, 1)
        self.assertIsInstance(res, str)
        jres=json.loads(res)
        self.assertIsInstance(jres['result'], int)
        
    def test_rsp2j_not_valid_error(self):
        res = self.serdes.resp_to_data(0, error=1)
        self.assertIsNone(res)        
        
    def test_rsp2j_missing_code_field(self):
        err={'message':0}
        res = self.serdes.resp_to_data(0, error=err)
        self.assertIsNone(res)        
        
    def test_rsp2j_ok(self):
        id_res=1278
        err={'code':0, 'message':"No, please not!", 'data':(1,2,3,4,("fdhgjdkf",4),3.5)}
        res = self.serdes.resp_to_data(id_res, error=err)
        self.assertIsInstance(res, str)
        jres=json.loads(res)
        self.assertIsInstance(jres['id'], int)
        self.assertEqual(jres['id'], id_res)
        self.assertIsInstance(jres['error']['code'], int)
        self.assertIsInstance(jres['error']['message'], str)
    
    #
    # Test conversion of request string to valid return data
    #
    def test_j2req_nojson(self):
        jdata={'bla':0}
        data=json.dumps(jdata)
        id_res, method, param = self.serdes.data_to_req(data)
        self.assertIsNone(id_res)
        
    def test_j2req_wronjsonrpc(self):
        jdata={'jsonrpc':'1.0', 'bla':0}
        data=json.dumps(jdata)
        id_res, method, param = self.serdes.data_to_req(data)
        self.assertIsNone(id_res)
        
    def test_j2req_noMethod(self):
        jdata={'jsonrpc':'2.0', 'bla':0}
        data=json.dumps(jdata)
        id_res, method, param = self.serdes.data_to_req(data)
        self.assertIsNone(id_res)
        
    def test_j2req_Method_not_string(self):
        jdata={'jsonrpc':'2.0', 'method':0}
        data=json.dumps(jdata)
        id_res, method, param = self.serdes.data_to_req(data)
        self.assertIsNone(id_res)
        
    def test_j2req_Method_no_param(self):
        methodName='print'
        jdata={'jsonrpc':'2.0', 'method':methodName}
        data=json.dumps(jdata)
        id_res, method, param = self.serdes.data_to_req(data)
        self.assertEqual(method, methodName)
        
    def test_j2req_Method_and_param(self):
        methodName='print'
        exp_params=[1,2,"42"]
        jdata={'jsonrpc':'2.0', 'method':methodName, 'params':exp_params}
        data=json.dumps(jdata)
        id_res, method, param = self.serdes.data_to_req(data)
        self.assertEqual(method, methodName)
        self.assertEqual(exp_params, param)
        
    def test_j2req_Method_and_param_and_id(self):
        methodName='print'
        exp_params=[1,2,"42"]
        id_exp = 56
        jdata={'jsonrpc':'2.0', 'method':methodName, 'params':exp_params, 'id':id_exp}
        data=json.dumps(jdata)
        id_res, method, param = self.serdes.data_to_req(data)
        self.assertEqual(method, methodName)
        self.assertEqual(exp_params, param)
        self.assertEqual(id_exp, id_res)
        
    #
    # Test responce object
    #
    def test_j2resp_nojson(self):
        jdata={'bla':0}
        data=json.dumps(jdata)
        id_res, result, error = self.serdes.data_to_resp(data)
        self.assertIsNone(id_res)
        
    def test_j2resp_wrong_json(self):
        jdata={'jsonrpc':'1.0'}
        data=json.dumps(jdata)
        id_res, result, error = self.serdes.data_to_resp(data)
        self.assertIsNone(id_res)
        
    def test_j2resp_jsonrpc_and_id_no_error_no_result(self):
        jdata={'jsonrpc':'2.0', 'id':1}
        data=json.dumps(jdata)
        id_res, result, error = self.serdes.data_to_resp(data)
        self.assertIsNone(id_res)
        
    def test_j2resp_jsonrpc_and_id_error_and_result(self):
        jdata={'jsonrpc':'2.0', 'id':1,'error':1, 'result':1}
        data=json.dumps(jdata)
        id_res, result, error = self.serdes.data_to_resp(data)
        self.assertIsNone(id_res)
        
    def test_j2resp_jsonrpc_id_error(self):
        exp_id=1
        exp_error=1
        jdata={'jsonrpc':'2.0', 'id':exp_id,'error':exp_error}
        data=json.dumps(jdata)
        id_res, result, error = self.serdes.data_to_resp(data)
        self.assertEqual(exp_id,id_res)
        self.assertEqual(None, result)
        self.assertEqual(exp_error,error)
        
    def test_j2resp_jsonrpc_id_result(self):
        exp_id=1
        exp_result=1
        jdata={'jsonrpc':'2.0', 'id':exp_id,'result':exp_result}
        data=json.dumps(jdata)
        id_res, result, error = self.serdes.data_to_resp(data)
        self.assertEqual(exp_id,id_res)
        self.assertEqual(exp_result,result)
        self.assertEqual(None,error)

        
if __name__ == '__main__':
    unittest.main()