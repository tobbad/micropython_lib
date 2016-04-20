# main.py -- put your code here!

import pyb
from f4dSetup import setupPins


setupPins()
i2c = pyb.I2C(1, pyb.I2C.MASTER)
scan = i2c.scan()
b = bytearray(1)
i2c.mem_read(b, scan[-1], 0)

