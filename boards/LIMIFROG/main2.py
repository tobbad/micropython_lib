import pyb
from board import sys_config, board, display
from lsm6ds3 import LSM6DS3
from demos import gravity
#
# A large memory block is needed
# Therefore we allocated it very early
# before fragmentation of memory happends
frog = board()
disp = display(frog)
disp.on()

i2c = pyb.I2C(sys_config['lis3mdl']['i2c_bus'],
              pyb.I2C.MASTER, baudrate=100000)
mems = LSM6DS3(i2c, sys_config['lsm6ds3']['i2c_addr'])
print("Acceleration  (%.3e, %.3e, %.3e)" % mems.accel.xyz())
print("Rotation      (%.3e, %.3e, %.3e)" % mems.gyro.xyz())
print("Temperature   %.2f C" % mems.temperature())

gravity(disp, mems.accel)
