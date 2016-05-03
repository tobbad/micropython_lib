
import pyb
from lis3mdl import LIS3MDL
from board import const

i2c = pyb.I2C(const['lis3mdl']['i2c_bus'], pyb.I2C.MASTER, baudrate=100000)

mag = LIS3MDL(i2c, const['lis3mdl']['i2c_addr'])
print(mag.xyz())

