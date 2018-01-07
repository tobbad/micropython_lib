import pyb
from mp_server import RPC_SRV, RPC_USER
from datalink import Datalink
from machine import UART

#com = pyb.USB_VCP()
com =  UART(2, baudrate=115200)
dl = Datalink(com)
srv = RPC_SRV(dl)
uobj=RPC_USER()
srv.register(uobj)
srv.start()
 
