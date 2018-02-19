import pyb
from mp_server import RPC_Server, RPC_USER
from serdes_json import SerDes
from datalink import Datalink
from machine import UART

#com = pyb.USB_VCP()
com =  UART(2, baudrate=115200)
dl = Datalink(com)
serdes = SerDes()
srv = RPC_Server(dl, serdes)
uobj=RPC_USER()
srv.register(uobj)
srv.start()
 
