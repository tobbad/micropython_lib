# -*- coding: utf-8 -*-

import json

class SerDes:
    
    __REQ_ID=0
    
    def __init__(self):
        pass
    
    def data_to_req(self, data):
        if data is None or len(data)==0:
            return None,  None,  None
        try:
            res = json.loads(data)
        except ValueError:
            print("ValueError")
            return None,  None,  None
        if not 'jsonrpc' in res:
            return None,  None,  None
        if res['jsonrpc'] != "2.0":
            return None,  None,  None
        if not 'method' in res:
            return None,  None,  None
        if not isinstance(res['method'], str):
            return None,  None,  None
        if not 'id' in res:
            res['id']="Null"
        if 'params' not in res:
            res['params']=None
        return res['id'], res['method'], res['params']

    def data_to_resp(self, data):
        if data is None or len(data)==0:
            return None,  None,  None
        try:
            res = json.loads(data)
        except ValueError:
            return None,  None,  None
        if not 'jsonrpc' in res:
            return None,  None,  None
        if not 'id' in res:
            return None,  None,  None
        if res['jsonrpc'] != "2.0":
            return None,  None,  None
        if 'result' in res and 'error' in res:
            return None,  None,  None
        if not 'result' in res and not 'error' in res:
            return None,  None,  None
        if 'result' in res:
            res['error']=None
        else:
            res['result']=None
        return res['id'], res['result'], res['error']

    def req_to_data(self, methodName, params=None):
        req_id = self.__REQ_ID
        self.__REQ_ID+=1
        if isinstance(params, (int, float, str)):
            params=[params,]
        params = list() if params is None else list(params)
        data={"jsonrpc":"2.0",
              "id":req_id ,
              "method":methodName,
              'params':params}
        return req_id, json.dumps(data)

    def resp_to_data(self, req_id, result=None, error=None):      
        data={"jsonrpc":"2.0",
              "id":req_id }
        if (result is not None) and error is not None:
            return None
        if result is not None:
            data['result']=result
        else:
            if not isinstance(error, dict):
                return None
            if 'code' not in error:
                return None
            data['error']=error
        return json.dumps(data)
