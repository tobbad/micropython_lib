
import pyb
from lis3mdl import LIS3MDL
from lps25h import LPS25H
from lsm6ds3 import LSM6DS3
from board import const

i2c = pyb.I2C(const['lis3mdl']['i2c_bus'], pyb.I2C.MASTER, baudrate=100000)

mag = LIS3MDL(i2c, const['lis3mdl']['i2c_addr'])
x,y,z = mag.xyz()
print("Magnetic field = (%.3e, %.3e, %.3e) %s" % (x,y,z, mag.unit()))

p = LPS25H(i2c, const['lps25h']['i2c_addr'])
print("%5.3e %s, %.1f m, T = %.1f C" % (p.value(), p.unit(), p.height(), p.temperature()))

accel = LSM6DS3(i2c, const['lsm6ds3']['i2c_addr'])
print("Acceleration  (%.3e, %.3e, %.3e)" % accel.accel())
print(accel.gyro())
