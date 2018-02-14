# -*- coding: utf-8 -*-

from micropython_lib.rpc.serdes_json import SerDes


class RPC_Server:
    
    EXCLUDE = ("register", "start")
    
    def __init__(self, dl, serdes):
        self._dl=dl
        self._serdes = serdes
        self._objects=self._getmembers(self)
        self._handle_idx = 0
        self._lobj_inst = {}
        
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
    
    def _get_object_handle(self, lobj):
        message={'code':-32000, 'message':"Object created", 'data':self._handle_idx}
        self._lobj_inst[self._handle_idx] = lobj
        self._handle_idx +=1
        return message   
    
    def _write(self, data):
        self._dl.write(data)
        
    def _read(self):
        return self._dl.read_str()
    
    def _check_result(self, result, error):
        if result is None:
            return result, error
        elif isinstance(result, (int, str, float)):
            return result, error
        elif isinstance(result, (list, tuple, dict)):
            # ToDo replace references to object s by handle
            error = {'code':-32603, 'message':"Internal error", 'data':None}
            return None, error
        message=self._setup_object_handle(result)
        return None, message
    
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
            result, error = self._check_result(result, error)
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
        