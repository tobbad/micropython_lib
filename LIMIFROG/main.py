
import pyb
from board import sys_config, board
from lis3mdl import LIS3MDL
from lps25h import LPS25H
from lsm6ds3 import LSM6DS3
from vl6180x import VL6180X

frog = board()
print(frog)

i2c = pyb.I2C(sys_config['lis3mdl']['i2c_bus'], pyb.I2C.MASTER, baudrate=100000)

mag = LIS3MDL(i2c, sys_config['lis3mdl']['i2c_addr'])
x,y,z = mag.xyz()
print("Magnetic field = (%.3e, %.3e, %.3e) %s" % (x,y,z, mag.unit()))

p = LPS25H(i2c, sys_config['lps25h']['i2c_addr'])
print("Pressure %5.3e %s, Height %.1f m, Temperature = %.1f C" % (p.value(), p.unit(), p.height(), p.temperature()))

mems = LSM6DS3(i2c, sys_config['lsm6ds3']['i2c_addr'])
print("Acceleration  (%.3e, %.3e, %.3e)" % mems.accel())
print("Rotation      (%.3e, %.3e, %.3e)" % mems.gyro())
print("Temperature   %.2f C" % mems.temperature())

dist = VL6180X(i2c, sys_config['vl6180x']['i2c_addr'])
val = dist.dev_id()
print("Distance sensor:")
print("\n".join(["  %s: %s" % (k,v) for k,v in val.items()]))
print("Distance      %.1f %s" % (dist.value(), dist.unit()))
