## A simple Remote procedure call (RPC) implementation for MP
The aim of this project is to realize a simple RPC implementation for MicroPython (MP) 
to allow the easy usage of classes runing on the MicroPython board but being 
controlled over some phy (Ethernet, Serial, WLAN...) and some marshalling (Json, XML, protobuf ..)
from the host (PC) side.

### Parameter passing
Parameters may be:
 - Primitive types (float, int, str, bytearray...)
 - Complex object instances
Further these types can be stored in list, tuples or dictionaries.

A rpc call can accept parameters of primitive types as input. Further it can 
return primitive types without any problem as these can be transfered between 
the client (PC) and the server (micropython board).

However parameters or return values which are instances of complex objects on
the client are implented as proxy on the server side. 
 - On host it must support the the methods which the object on the client
   has. Using 
 - On 

