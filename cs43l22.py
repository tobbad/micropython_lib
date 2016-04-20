import pyb
from pyb import I2C
from pyb import Pin

DEVICE_ADDR = 0x4a
BEEPTONE_ADDR = 0x1e

class CS43L22:
    def __init__(self, resetPin=None):
        if not resetPin:
            resetPin = pyb.Pin('PE3', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
        self.reset = resetPin
        self.reset.low()
        pyb.delay(100)
        self.reset.high()
        pyb.delay(1000)

        self.i2c = I2C(1, I2C.MASTER, baudrate=100000)

    def init(self):
        print([hex(i) for i in self.i2c.scan()])

        if self.i2c.is_ready(DEVICE_ADDR):
            print("ready")
            self.i2c.mem_write(0x99, DEVICE_ADDR, 0x00)
            self.i2c.mem_write(0x80, DEVICE_ADDR, 0x47)
            self.i2c.mem_write(0x80, DEVICE_ADDR, 0x32)
            self.i2c.mem_write(0x00, DEVICE_ADDR, 0x32)
            self.i2c.mem_write(0x00, DEVICE_ADDR, 0x00)
            self.i2c.mem_write(0x9e, DEVICE_ADDR, 0x02)

            pyb.delay(1000)

            # Volume
            self.i2c.mem_write(0x18, DEVICE_ADDR, 0x20)
            self.i2c.mem_write(0x18, DEVICE_ADDR, 0x21)
            self.i2c.mem_write(0x18, DEVICE_ADDR, 0x1a)
            self.i2c.mem_write(0x18, DEVICE_ADDR, 0x1b)

            self.i2c.mem_write(0x0f, DEVICE_ADDR, 0x1c)
            self.i2c.mem_write(0x06, DEVICE_ADDR, 0x1d)
            self.i2c.mem_write(0xc0, DEVICE_ADDR, BEEPTONE_ADDR)            

 
    def volume(self, value):
        pass