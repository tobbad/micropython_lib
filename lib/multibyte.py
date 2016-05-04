#
# Base class for handling multibyte read/write
# An other inhereted class must support read/write
# functions which returns/accepts a binary array.
#
import struct


class multibyte():

    def __init__(self, com, selector, addr_size, msb_first):
        self.msb_first = msb_first
        if self.msb_first is False:
            raise Exception("LSB first not supported yet")

    def __read(self, reg_addr, cnt, signed=False, raw=False):
        res = self.read_binary(reg_addr, cnt)
        if not raw:
            res_conv = res[0]
            for i in range(1, cnt):
                res_conv += res[i] << (i*8)
            res = res_conv
            if signed:
                if res >= (1 << ((cnt*8)-1)):
                    res -= 1 << (cnt*8)
        return res

    def read_u8(self, addr):
        return self.__read(addr, 1)

    def read_s8(self, addr):
        return self.__read(addr, 1, signed=True)

    def read_u16(self, addr):
        return self.__read(addr, 2)

    def read_s16(self, addr):
        return self.__read(addr, 2, signed=True)

    def read_u24(self, addr):
        return self.__read(addr, 3)

    def read_s24(self, addr):
        return self.__read(addr, 3, signed=True)

    def read_u32(self, addr):
        return self.__read(addr, 4)

    def read_s32(self, addr):
        return self.__read(addr, 4, signed=True)

    def write_u8(self, addr, value):
        data = struct.pack("B", value)
        self.write_binary(addr, data)

    def write_s8(self, addr, value):
        data = struct.pack("b", value)
        self.write_binary(addr, data)

    def write_u16(self, addr, value):
        data = struct.pack(">H", value)
        self.write_binary(addr, data)
