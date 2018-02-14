# -*- coding: utf-8 -*-

import socket

class PhySocket:
    
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connection, self._client_address = None, None
        
    def rx(self, server_address):
        self._sock.bind(server_address)
        self._sock.listen()
        
    def tx(self, server_address):
        self._sock.connect(server_address)
        
    def read(self):
        self._connection, self._client_address = self._sock.accept()
        print("New connection")
        try:
            res=()
            while True:
                data = self._connection.recv(16)
                if data:
                    res+=data
                else:
                    break
        finally:
            self.close()
        return "".join(res)
 
    def close(self):
        print("Close connection")
        self._connection.close()
        self._connection, self._client_address = None, None
   
    def write(self, data):
        if self._connection is None:
            return
        try:
            self._connection.sendall(data)
        finally:
            self.close()
            
    def any(self):
        return True