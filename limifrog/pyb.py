
import struct

class I2C(object):

    MASTER = 1

    def __init__(self, busNr, mode, addr=0x12, baudrate=400000, gencall=False):
        self.busNr = busNr
        self.dev={}
        self.dev[addr]={}
        self.dev[addr][0x09]= [0xB4,]

    def check(self, addr, memaddr):
        ret = True
        if not addr in self.dev:
            self.dev[addr]={}
            ret = False
        if not memaddr in self.dev[addr]:
            self.dev[addr][memaddr]=[]
            ret = False
        return ret

    def mem_read(self,data, addr, memaddr, timeout=5000, addr_size=8):
        res = self.check(addr, memaddr)
        if res:
            return struct.pack("B",self.dev[addr][memaddr][-1])
        else:
            return struct.pack("B",0)

    def mem_write(self, data, addr, memaddr, timeout=5000, addr_size=8):
        res = self.check(addr, memaddr)
        self.dev[addr][memaddr].append(data)
