#
#
#
from i2cspi import COM_I2C
from multibyte import multibyte
from lps25h_const import *

from math import log

class LPS25H(COM_I2C, multibyte):
    ''' Pressure sensor'''

    WHO_IAM_ANSWER = 0xBD
    WHO_IAM_REG = 0x0F

    DEFAULT_CONF = [
        # 0xB0 = 0b10110000
        # PD = 1 (active mode);  ODR = 011 (12.5 Hz pressure & temperature output data rate)
        # Not very energy efficient but shows the device works.
        (CTRL_REG1_ADDR, 0xB0)]

    def __init__(self, communication, dev_selector):
        super(LPS25H, self).__init__(communication, dev_selector, self.ADDR_MODE_8, self.TRANSFER_MSB_FIRST)
        self.init()
        self.__t = -273.15
        self.__p  = 0.0
        self.__p0 = 1013.25     # mBar
        self.__hs = 7988.203

    def __measure(self):
        self.__t = 42.5+self.read_s16(TEMP_OUT_L|(1<<7))/480.0
        self.__p = self.read_s24(PRESS_OUT_XL|(1<<7))/4096.0

    def value(self):
        self.__measure()
        return self.__p

    def unit(self):
        return 'Pa'

    def height(self):
        self.__measure()
        height =self.__hs*log(self.__p0/self.__p)
        return height

    def temperature(self):
        self.__measure()
        return self.__t
