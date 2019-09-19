#
#
#
from i2cspi import COM_I2C
from multibyte import multibyte
from math import pow

CTRL_REG1_ADDR = const(0x10)
TEMP_OUT_L = const(0x2B)
PRESS_OUT_XL = const(0x28)





class LPS22XX(COM_I2C, multibyte):
    ''' Pressure sensor'''

    DEFAULT_CONF = [
        # 0x4E = 0b01001110
        # ODR = 100 (50 Hz pressure & temperature output data rate)
        # EN_LPFG = 1  Enable low pass filtering
        # LPFP_CFG = 1 Lowpass update rate is ODR/20 ~= 2.5 updates/2
        # BDU = 1 Avoid update of pressure data registers between reading of
        #         PRESS_OUT_L and PRESS_OUT_H
        # SIM = 0 SPI 4Wire mode (Not used)
        # Not very energy efficient but shows the device works.
        (CTRL_REG1_ADDR, 0x4e)]

    def __init__(self, communication, dev_selector):
        super().__init__(communication, dev_selector,
                         addr_size=self.ADDR_MODE_8,
                         msb_first=self.TRANSFER_MSB_FIRST)
        self.init()
        self.__t = -273.15
        self.__p = 0.0
        self.__p0 = 1013.25     # mBar
        self.__T0 = 288.15
        self.__Tgrad = 0.0065
        self.__exp = 1.0/5.255

    def __measure(self):
        self.__t = self.read_s16(TEMP_OUT_L)/100.0
        self.__p = self.read_s24(PRESS_OUT_XL)/4096.0

    def value(self):
        self.__measure()
        return self.__p

    def unit(self):
        return 'mBar'

    def height(self):
        ''' Using international hight formula '''
        self.__measure()
        height = self.__T0/self.__Tgrad
        height *= (1.0 - pow(self.__p/self.__p0, self.__exp))
        return height

    def temperature(self):
        self.__measure()
        return self.__t


class LPS22HB(LPS22XX, COM_I2C, multibyte):
    ''' Pressure sensor'''

    WHO_IAM_ANSWER = 0xB1
    WHO_IAM_REG = 0x0F

    DEFAULT_CONF = [
        # 0x4E = 0b01001110
        # ODR = 100 (50 Hz pressure & temperature output data rate)
        # EN_LPFG = 1  Enable low pass filtering
        # LPFP_CFG = 1 Lowpass update rate is ODR/20 ~= 2.5 updates/2
        # BDU = 1 Avoid update of pressure data registers between reading of
        #         PRESS_OUT_L and PRESS_OUT_H
        # SIM = 0 SPI 4Wire mode (Not used)
        # Not very energy efficient but shows the device works.
        (CTRL_REG1_ADDR, 0x4e)]


class LPS22HH(LPS22XX, COM_I2C, multibyte):
    ''' Pressure sensor'''

    WHO_IAM_ANSWER = 0xB3
    WHO_IAM_REG = 0x0F

    DEFAULT_CONF = [
        # 0x4E = 0b01001110
        # ODR = 100 (50 Hz pressure & temperature output data rate)
        # EN_LPFG = 1  Enable low pass filtering
        # LPFP_CFG = 1 Lowpass update rate is ODR/20 ~= 2.5 updates/2
        # BDU = 1 Avoid update of pressure data registers between reading of
        #         PRESS_OUT_L and PRESS_OUT_H
        # SIM = 0 SPI 4Wire mode (Not used)
        # Not very energy efficient but shows the device works.
        (CTRL_REG1_ADDR, 0x4e)]

