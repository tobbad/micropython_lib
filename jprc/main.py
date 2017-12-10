import pyb
from mp_server import JRPC_SRV


com = pyb.USB_VCP()
srv = JRPC_SRV(com)
srv.start()
 
