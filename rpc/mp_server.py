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

class RPC_SRV:
    
    EXCLUDE = ("register", "start")
    
    def __init__(self, dl):
        self._dl=dl
        self._serdes = SerDes()
        self._objects=self._getmembers(self)
        
    def _getmembers(self, obj):
        res = {}
        exclude = []
        if "EXCLUDE" in dir(obj):
            exclude = obj.EXCLUDE
        for name in dir(obj):
            val = getattr(obj, name)
            if name[0] == '_':
                # Not include private functions
                continue
            if name in exclude:
                # Explicite exclude functions
                continue
            if not isinstance(val, type(self._getmembers)):
                # Only functions are callabel
                continue
            res[name]=val
        return res
    
    def _write(self, data):
        self._dl.write(data)
        
    def _read(self):
        return self._dl.read_str()
    
    def get_objects(self):
        return tuple(self._objects.keys())
   
    def register(self, srv_object):
        self._objects.update(self._getmembers(srv_object))
    
    def start(self):
        while True:
            result = None
            error = None
            data = self._read()
            if data is None or len(data)==0:
                continue
            req_id, method, params = self._serdes.data_to_req(data)
            if req_id is not None:
                print("ReqId[%4d]: %s(%s)" % (req_id, method, str(params)))
                if method in self._objects:
                    fun = self._objects[method]
                    try:
                        if len(params)==0:
                            result = fun()
                        else:
                            result = fun(*params)
                    except:
                        error={'code':-32602, 'message':"Invalid params", 'data':None}
                else:
                    error={'code':-32601, 'message':"Method not found", 'data':None}
            else:
                error={'code':-32700, 'message':"Parse error", 'data':None}
            data = self._serdes.resp_to_data(req_id, result=result, error=error)
            print("Send back: \"%s\"" % (data))
            self._write(data)


class RPC_USER:
    
    def __init__(self):
        pass
    
    def existing_function(self, para):
        return "OK %d" % para
   
    def existing_function_no_para(self):
        return "OK" 
        