# -*- coding: utf-8 -*-


class RPC_Proxy:
    
    def __init__(self, client):
        self._client = clien

    def __getattr__(self, name):
        
        
        

class RPC_Client:
    
    instance = None
    
    class __singleton:
        def __init__(self, datalink):
            self._dl = datalink
    
    def __init__(self, datalink, serdes):
        self._serdes = serdes
        if RPC_Client.instance is None:
            RPC_Client.instance = self.__singleton(datalink)
        else:
            pass
    
    def _write(self, data):
        self.instance._dl.write(data)
        
    def _read(self):
        return self.instance._dl.read_str()

    def call(self, method_name, *args):
        