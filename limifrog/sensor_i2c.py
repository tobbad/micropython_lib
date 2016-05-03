#
# Base class for all  i2c based sensors
#
import pyb
import struct
class sensor_i2c():

    ADDR_MODE_8, ADDR_MODE_16 = 8, 16

    def __init__(self, bus, addr, addr_size):
        self.addr = addr
        if addr_size not in (self.ADDR_MODE_8, self.ADDR_MODE_16):
            raise Exception("Address size not 8 or 16 not supported")
        self.addr_size  = addr_size
        self.com = pyb.I2C(bus, pyb.I2C.MASTER, addr = self.addr)
        whoami = self.read(self.WHO_IAM_REG)
        if whoami != self.WHOAMI_ANS:
            raise Exception("No sensor found @ 0x%02x" %(self.addr))


    def set_mode_16bit_addr(self, mode = True):
        if mode:
            self.addr_size  = self.ADDR_MODE_16
        else:
            self.addr_size  = self.ADDR_MODE_8

    def read(self, addr, cnt=1):
        ans = self.com.mem_read(data=cnt, addr=self.addr, memaddr=addr, addr_size=self.addr_size)
        res = struct.unpack("B"*cnt, ans)
        if self.debug:
            print("Read addr 0x%02x, data(hex): %s" % (addr, " ".join(["0x%02x" % i for i in res])))
        if cnt == 1:
            res = res[0]
        return res

    def read_u16(self, addr):
        res = self.read(addr, 2)
        return (res[1]<<8) + res[0]

    def read_s16(self, addr):
        res = self.read_u16(addr)
        if res>=(1<<15):
            res -= (1<<16)
        return res

    def read_u24(self, addr):
        res = self.read(addr, 3)
        return (res[2]<<16) | (res[1]<<8) | res[0]

    def read_s24(self, addr):
        res = self.read_u24(addr)
        if res>=(1<<23):
            res -= (1<<24)
        return res


    def __write(self, addr, data):
        if self.debug:
            print("Write addr %02x, data: %s" % (addr, " ".join(["0x02%x" % i for i in data])))
        self.com.mem_write(data=data, addr=self.addr, memaddr=addr, addr_size=self.addr_size)

    def write(self, addr, value):
        data = struct.pack("B", value)
        self.__write(addr, data)

    def write_u16(self, addr, value):
        data = struct.pack(">H", value)
        self.__write(addr, data)

if __name__ == '__main__':
    class DUMMY(sensor_i2c):
        WHOAMI_ANS = 0xB4
        WHO_IAM_REG = 0x09
        def __init__(self, addr = 0x29):
            super(DUMMY, self).__init__(addr)

    a = DUMMY(0x42)
    a.write_u16(0, 256)