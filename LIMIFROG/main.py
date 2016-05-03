
import pyb
from lis3mdl import LIS3MDL
from lps25h import LPS25H
from board import const

i2c = pyb.I2C(const['lis3mdl']['i2c_bus'], pyb.I2C.MASTER, baudrate=100000)

mag = LIS3MDL(i2c, const['lis3mdl']['i2c_addr'])
print(mag.xyz())

p = LPS25H(i2c, const['lps25h']['i2c_addr'])
print("%5.3e %s, %.1f m, T = %.1f C" % (p.value(), p.unit(), p.height(), p.temperature()))
