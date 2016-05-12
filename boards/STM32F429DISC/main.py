# main.py -- put your code here!

import pyb
from l3GD20 import L3GD20

cs_gyro = pyb.Pin('PC1', pyb.Pin.OUT_PP)

for pol in (0, 1):
    for ph in (0, 1):
        print("Polarity: %d, Phase %d" % (pol, ph))
        spi = pyb.SPI(5, pyb.SPI.MASTER, baudrate=600000,
                      polarity=pol, phase=ph)
        gyro = L3GD20(spi, cs_gyro)

spi = pyb.SPI(5, pyb.SPI.MASTER, baudrate=600000, polarity=1, phase=1)
gyro = L3GD20(spi, cs_gyro)
