import pyb
import sensor_i2c


BEEPTONE_ADDR = 0x1e

class CS43L22(sensor_i2c.sensor_i2c):

    WHO_IAM_REG = 0x01
    WHOAMI_ANS = 0xE0
    WHOAMI_ANS_MASK = 0xF8
    debug = False
  
    
    def __init__(self, i2c_bus=1, i2c_addr = 0x4A, resetPin='PD4', i2sPin={'mck':'PC7', 'sck':'PC10', 'sd':'PC12','ws':'PA4'}):
        # Release reset from the device
        self.reset = pyb.Pin(resetPin, pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
        self.reset.low()
        pyb.delay(10)
        self.reset.high()
        pyb.delay(10)
        super(CS43L22, self).__init__(i2c_bus, i2c_addr, self.ADDR_MODE_8)
        for name, loc in i2sPin:
            pyb.Pin(loc, pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
        

    def init(self):
        print([hex(i) for i in self.i2c.scan()])

        if self.i2c.is_ready(self.__DEVICE_ADDR):
            print("ready")
            self.i2c.mem_write(0x99, self.__DEVICE_ADDR, 0x00)
            self.i2c.mem_write(0x80, self.__DEVICE_ADDR, 0x47)
            self.i2c.mem_write(0x80, self.__DEVICE_ADDR, 0x32)
            self.i2c.mem_write(0x00, self.__DEVICE_ADDR, 0x32)
            self.i2c.mem_write(0x00, self.__DEVICE_ADDR, 0x00)
            self.i2c.mem_write(0x9e, self.__DEVICE_ADDR, 0x02)

            pyb.delay(1000)

            # Volume
            self.i2c.mem_write(0x18, self.__DEVICE_ADDR, 0x20)
            self.i2c.mem_write(0x18, self.__DEVICE_ADDR, 0x21)
            self.i2c.mem_write(0x18, self.__DEVICE_ADDR, 0x1a)
            self.i2c.mem_write(0x18, self.__DEVICE_ADDR, 0x1b)

            self.i2c.mem_write(0x0f, self.__DEVICE_ADDR, 0x1c)
            self.i2c.mem_write(0x06, self.__DEVICE_ADDR, 0x1d)
            self.i2c.mem_write(0xc0, self.__DEVICE_ADDR, BEEPTONE_ADDR)            

 
 
 
 
    def volume(self, value):
        pass