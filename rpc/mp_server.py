# -*- coding: utf-8 -*-

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
        