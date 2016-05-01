#
# Base class for all  i2c based sensors
#
import pyb
import struct


class COM_SERIAL():

    WHO_IAM_ANSWER_MASK = 0xFF
    ADDR_MODE_8, ADDR_MODE_16 = 8, 16
    DEBUG = False
    TRANSFER_MSB_FIRST = True
    TRANSFER_LSB_FIRST = False
    
    def __init__(self, communication, dev_selector, addr_size, msb_first):
        if addr_size not in (self.ADDR_MODE_8, self.ADDR_MODE_16):
            raise Exception("Address size not 8 or 16 not supported")
        self.com = communication
        self.selector = dev_selector
        self.addr_size  = addr_size
        whoami = self.read_binary(self.WHO_IAM_REG, 1)[0] & self.WHO_IAM_ANSWER_MASK
        if whoami != self.WHO_IAM_ANSWER:
            raise Exception("No sensor found @ 0x%02x" %(self.i2c_addr))
       
    def set_mode_16bit_addr(self, mode = True):
        if mode:
            self.addr_size  = self.ADDR_MODE_16
        else:
            self.addr_size  = self.ADDR_MODE_8

    def buf2Str(self, data):
        return " ".join(["0x%02x" % i for i in data])


class COM_I2C(COM_SERIAL):

    def read_binary(self, reg_addr, byte_cnt):
        ans = self.com.mem_read(data=byte_cnt, addr=self.selector, memaddr=reg_addr, addr_size=self.addr_size)
        res = struct.unpack("B"*byte_cnt, ans)
        if self.DEBUG:
            print("Read (Dev 0x%02x) reg addr 0x%02x, data: %s" % (self.selector, reg_addr, self.buf2Str(res)))
        return res

    def write_binary(self, reg_addr, data):
        if self.DEBUG:
            print("Write (Dev 0x%02x) reg addr 0x%02x, data: %s" % (self.selector, reg_addr, self.buf2Str(data)))
        self.com.mem_write(data=data, addr=self.selector, memaddr=reg_addr, addr_size=self.addr_size)

class COM_SPI(COM_SERIAL):
    
    READWRITE_CMD = 0x80
    MULTIPLEBYTE_CMD = 0x40

    def read_binary(self, reg_addr, byte_cnt):
        reg_addr |= self.READWRITE_CMD
        if byte_cnt > 1:
            reg_addr |= self.MULTIPLEBYTE_CMD
        self.selector.low()
        self.com.send(reg_addr)
        buf = self.com.recv(byte_cnt)
        self.selector.high()
        if self.DEBUG:
            print("Read (Dev %s) reg addr 0x%02x, data: %s" % (self.selector, reg_addr, self.buf2Str(res)))
        return buf

    def write_binary(self, reg_addr, data):
        if len(data) > 1:
            reg_addr |= self.MULTIPLEBYTE_CMD
        self.selector.low()
        self.com.send(reg_addr)
        for b in data:
            self.com.send(b)
        if self.DEBUG:
            print("Write (Dev %s) reg addr 0x%02x, data: %s" % (self.selector, reg_addr, self.buf2Str(data)))
        self.selector.high()

if __name__ == '__main__':
    class DUMMY(sensor_i2c):
        WHOAMI_ANS = 0xB4
        WHO_IAM_REG = 0x09
        def __init__(self, i2c_addr = 0x29):
            super(DUMMY, self).__init__(addr)

    a = DUMMY(0x42)
    a.write_u16(0, 256)