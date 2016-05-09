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
        self.addr_size = addr_size

    def init(self):
        for reg, val in self.DEFAULT_CONF:
            self.write_u8(reg, val)

    def id(self):
        myId = self.read_binary(self.WHO_IAM_REG, 1)[0]
        myId &= self.WHO_IAM_ANSWER_MASK
        return myId

    def exists(self):
        '''
        Check if device on the bus exists:
        Keep it separate from constructor to allow setup the chip before asking
        for identity as needed for example in 3 wire SPI communication.
        '''
        whoami = self.id()
        if whoami != self.WHO_IAM_ANSWER:
            raise Exception("No sensor found %s" % (self))

    def set_mode_16bit_addr(self, mode=True):
        if mode:
            self.addr_size = self.ADDR_MODE_16
        else:
            self.addr_size = self.ADDR_MODE_8

    def write(self, addr, value):
        self.write_binary(addr, value)

    def read(self, addr):
        return self.read_binary(addr, 1)[0]

    def buf2Str(self, data):
        return " ".join(["0x%02x" % i for i in data])

    def unit(self):
        return "NA"

    def __str__(self):
        raise Exception("Function must be defined in derived class")


class COM_I2C(COM_SERIAL):

    MULTIPLEBYTE_CMD = 0x80

    def set_multi_byte(self, addr):
        return (addr | self.MULTIPLEBYTE_CMD)

    def read_binary(self, reg_addr, byte_cnt):
        if byte_cnt > 1:
            reg_addr = self.set_multi_byte(reg_addr)
        ans = self.com.mem_read(data=byte_cnt, addr=self.selector,
                                memaddr=reg_addr, addr_size=self.addr_size)
        res = struct.unpack("B"*byte_cnt, ans)
        if self.DEBUG:
            print("Read (%s) reg addr 0x%02x, data: %s" %
                  (self, reg_addr, self.buf2Str(res)))
        return res

    def write_binary(self, reg_addr, data):
        if self.DEBUG:
            print("Write (%s) reg addr 0x%02x, data: %s" %
                  (self, reg_addr, self.buf2Str(data)))
        self.com.mem_write(data=data, addr=self.selector,
                           memaddr=reg_addr, addr_size=self.addr_size)

    def __str__(self):
        return "I2C @ 0x%02x" % self.selector


class COM_SPI(COM_SERIAL):

    READ_CMD = 0x80
    MULTIPLEBYTE_CMD = 0x40

    def __init__(self, communication, dev_selector, addr_size, msb_first):
        super(COM_SPI, self).__init__(communication, dev_selector,
                                      addr_size, msb_first)
        self.__bidi_mode = False
        self.__use_dir = 'dir' in self.__dict__

    @property
    def bidi_mode(self):
        return self.__bidi_mode

    @bidi_mode.setter
    def bidi_mode(self, mode):
        self.__bidi_mode = mode

    def set_multi_byte(self, addr):
        return (addr | self.MULTIPLEBYTE_CMD)

    def read_binary(self, reg_addr, byte_cnt):
        reg_addr |= self.READ_CMD
        if byte_cnt > 1:
            reg_addr = self.set_multi_byte(reg_addr)
        self.selector.low()
        if self.__bidi_mode and self.__use_dir:
            if self.DEBUG:
                print("Set one line mode")
            self.com.dir(self.com.DIRECTION_ONE_LINE)
        else:
            if self.DEBUG:
                print("Set two line mode")
            if self.__use_dir:
                self.com.dir(self.com.DIRECTION_TWO_LINES)
        self.com.send(reg_addr)
        buf = self.com.recv(byte_cnt)
        self.selector.high()
        if self.DEBUG:
            print("Read (%s) reg addr 0x%02x, data: %s" %
                  (self, reg_addr, self.buf2Str(buf)))
        return buf

    def write_binary(self, reg_addr, data):
        if len(data) > 1:
            reg_addr |= self.MULTIPLEBYTE_CMD
        self.selector.low()
        if self.__bidi_mode:
            if self.DEBUG:
                print("Set one line mode")
            if self.__use_dir:
                self.com.dir(self.com.DIRECTION_ONE_LINE)
        else:
            if self.DEBUG:
                print("Set two line mode")
            if self.__use_dir:
                self.com.dir(self.com.DIRECTION_TWO_LINES)
        self.com.send(reg_addr)
        for b in data:
            self.com.send(b)
        if self.DEBUG:
            print("Write (%s) reg addr 0x%02x, data: %s" %
                  (self, reg_addr, self.buf2Str(data)))
        self.selector.high()

    def __str__(self):
        res = "SPI CS=Pin(%s)%s" % (self.selector.name(),
                                    ", BiDi" if self.__bidi_mode else "")
        return res
