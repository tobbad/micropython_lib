#
#
#
import sensor_i2c
from LIS3MDL_const import *
from math import sqrt

class LIS3MDL(sensor_i2c.sensor_i2c):

    WHO_IAM_REG = 0x0F
    WHOAMI_ANS = 0x3D
    debug = False

    def __init__(self, bus=2, addr = 0x1C):
        super(LIS3MDL, self).__init__(bus, addr, self.ADDR_MODE_8)
        self.gauss2tesla = 1.0/10000.0

        # from https://github.com/pololu/lis3mdl-arduino/blob/master/LIS3MDL.cpp
        # 0x70 = 0b01110000
        # OM = 11 (ultra-high-performance mode for X and Y); DO = 100 (10 Hz ODR)
        self.write(CTRL_REG1_ADDR, 0x70)
        # 0x00 = 0b00000000
        # FS = 00 (+/- 4 gauss full scale)
        self.write(CTRL_REG2_ADDR, 0x00)
        self.__scale = 4.0

        # 0x00 = 0b00000000
        # MD = 00 (continuous-conversion mode)
        self.write(CTRL_REG3_ADDR, 0x00)
        # 0x0C = 0b00001100
        # OMZ = 11 (ultra-high-performance mode for Z)
        self.write(CTRL_REG4_ADDR, 0x0C)

    def x(self):
        val = self.read_s16(MAGNETO_X_LOW_REG|0x80) # 0x80 for auto increment of adresse
        # Return value in Tesla
        # (4 gauss scale) * (6842 LSB/gauss at 4 gauss scale)
        return val*self.__scale/SENSITIVITY_OF_MIN_SCALE*self.gauss2tesla

    def y(self):
        val = self.read_s16(MAGNETO_Y_LOW_REG|0x80) # 0x80 for auto increment of adresse
        return val*self.__scale/SENSITIVITY_OF_MIN_SCALE*self.gauss2tesla

    def z(self):
        val = self.read_s16(MAGNETO_Z_LOW_REG|0x80) # 0x80 for auto increment of adresse
        return val*self.__scale/SENSITIVITY_OF_MIN_SCALE*self.gauss2tesla

    def norm(self, vec=None):
        if vec == None:
            vec = self.vec()
        vec_a = sqrt(sum([i*i for i in vec]))
        return vec_a

    def vec(self):
        x = self.x()
        y = self.y()
        z = self.z()
        return x,y,z

    def vec_normalized(self):
        vec = self.vec()
        vec_a = self.norm(vec)
        return [i/vec_a  for i in vec]


