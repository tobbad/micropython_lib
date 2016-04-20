#
#
#
import sensor_i2c
from LPS25H_const import *
from math import log

class LPS25H(sensor_i2c.sensor_i2c):

    WHOAMI_ANS = 0xBD
    WHO_IAM_REG = 0x0F
    debug = False

    def __init__(self, addr = 0x5C):
        super(LPS25H, self).__init__(2, addr, self.ADDR_MODE_8)
        self.__t = -273.15
        self.__p  = 0.0
        self.__p0 = 1013.25     # mBar
        self.__hs = 7988.203
        # 0xB0 = 0b10110000
        # PD = 1 (active mode);  ODR = 011 (12.5 Hz pressure & temperature output data rate)
        # Not very energy efficient but shows the device works.
        self.write(CTRL_REG1_ADDR, 0xB0)

    def __measure(self):
        self.__t = 42.5+self.read_s16(TEMP_OUT_L|(1<<7))/480.0
        self.__p = self.read_s24(PRESS_OUT_XL|(1<<7))/4096.0

    def pressure(self):
        self.__measure()
        return self.__p

    def height(self):
            self.__measure()
            height =self.__hs*log(self.__p0/self.__p)
            return height

    def temperature(self):
        self.__measure()
        return self.__t
