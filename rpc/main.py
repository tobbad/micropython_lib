import pyb
from mp_server import JRPC_SRV
from datalink import Datalink


com = Datalink(pyb.USB_VCP())
srv = JRPC_SRV(com)
srv.start()
 
