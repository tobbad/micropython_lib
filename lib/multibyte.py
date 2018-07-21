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

    def __read(self, reg_addr, cnt, signed=False, lsb_first=True):
        data = [ i for i in self.read_binary(reg_addr, cnt)]
        if not lsb_first:
            data.reverse()
        res_conv = data[0]
        for i in range(1, cnt):
            res_conv += data[i] << (i*8)
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

    def read_u16_r(self, addr):
        return self.__read(addr, 2, lsb_first=False)

    def read_s16(self, addr):
        return self.__read(addr, 2, signed=True)

    def read_u24(self, addr):
        return self.__read(addr, 3)

    def read_u24_r(self, addr):
        return self.__read(addr, 3, lsb_first=False)

    def read_s24(self, addr):
        return self.__read(addr, 3, signed=True)

    def read_u32(self, addr):
        return self.__read(addr, 4)

    def read_u32_r(self, addr):
        return self.__read(addr, 4, lsb_first=False)

    def read_s32(self, addr):
        return self.__read(addr, 4, signed=True)

    def __write(self, addr, value, cnt, msb_first=False):
        data = []
        for i in range(cnt):
            data.append(value & 0xFF)
            value >>= 8
        if msb_first:
            data.reverse()
        for a, v in zip(range(addr, addr+cnt), data):
            self.write_u8(a, v)

    def write_u8(self, addr, value):
        data = struct.pack("B", value)
        self.write_binary(addr, data)

    def write_s8(self, addr, value):
        data = struct.pack("b", value)
        self.write_binary(addr, data)

    def write_u16(self, addr, value):
        data = struct.pack("<H", value)
        print("u16   0x%04x" % value, "[ 0x%02x" % data[0], "0x%02x ]"% data[1])
        self.write_binary(addr, data)

    def write_u16_m(self, addr, value):
        data = struct.pack(">H", value)
        print("u16_m 0x%04x" % value, "[ 0x%02x" % data[0], "0x%02x ]"% data[1])
        self.write_binary(addr, data)

    def write_u24_m(self, addr, value):
        self.__write(addr, value, 3, msb_first=True)
