#
# Base class for all  i2c based sensors
#
import pyb
import struct

class sensor_i2c():

    ADDR_MODE_8, ADDR_MODE_16 = 8, 16
    WHOAMI_ANS_MASK = 0xFF

    def __init__(self, i2c_bus, i2c_addr, addr_size):
        self.i2c_addr = i2c_addr
        if addr_size not in (self.ADDR_MODE_8, self.ADDR_MODE_16):
            raise Exception("Address size not 8 or 16 not supported")
        self.addr_size  = addr_size
        self.com = pyb.I2C(i2c_bus, pyb.I2C.MASTER, addr = self.i2c_addr)
        whoami = self.read_u8(self.WHO_IAM_REG) & self.WHOAMI_ANS_MASK

        if whoami != self.WHOAMI_ANS:
            raise Exception("No sensor found @ 0x%02x" %(self.i2c_addr))

    def set_mode_16bit_addr(self, mode = True):
        if mode:
            self.addr_size  = self.ADDR_MODE_16
        else:
            self.addr_size  = self.ADDR_MODE_8
    
    def __buf2Str(self, data):
        return " ".join(["0x%02x" % i for i in data])

    def __read(self, reg_addr, cnt, signed = False, raw = False):
        ans = self.com.mem_read(data=cnt, addr=self.i2c_addr, memaddr=reg_addr, addr_size=self.addr_size)
        res = struct.unpack("B"*cnt, ans)
        if self.debug:
            print("Read (Dev 0x%02x) reg addr 0x%02x, data: %s" % (self.i2c_addr, reg_addr, self.__buf2str(res)))
        if not raw:
            res_conv = res[0]
            for i in range(1,cnt):
                res_conv+= res[i]<<(i*8)
            res = res_conv
            if signed:
                if res >= (1<<((cnt*8)-1)):
                    res -= 1<<(cnt*8)
        return res

    def read(self, addr, cnt=1):
        return self.__read(addr, cnt, raw = True)

    def read_u8(self, addr):
        return self.__read(addr, 1)

    def read_s8(self, addr):
        return self.__read(addr, 1, signed = True)

    def read_u16(self, addr):
        return self.__read(addr, 2)

    def read_s16(self, addr):
        return self.__read(addr, 2, signed = True)

    def read_u24(self, addr):
        return self.__read(addr, 3)

    def read_s24(self, addr):
        return self.__read(addr, 3, signed = True)

    def read_u32(self, addr):
        return self.__read(addr, 4)

    def read_s32(self, addr):
        return self.__read(addr, 4, signed = True)


    def __write(self, reg_addr, data):
        if self.debug:
            print("Write (Dev 0x%02x) reg addr 0x%02x, data: %s" % (self.i2c_addr, reg_addr, self.__buf2str(data)))
        self.com.mem_write(data=data, addr=self.i2c_addr, memaddr=reg_addr, addr_size=self.addr_size)

    def write_u8(self, addr, value):
        data = struct.pack("B", value)
        self.__write(addr, data)

    def write_u16(self, addr, value):
        data = struct.pack(">H", value)
        self.__write(addr, data)

if __name__ == '__main__':
    class DUMMY(sensor_i2c):
        WHOAMI_ANS = 0xB4
        WHO_IAM_REG = 0x09
        def __init__(self, i2c_addr = 0x29):
            super(DUMMY, self).__init__(addr)

    a = DUMMY(0x42)
    a.write_u16(0, 256)