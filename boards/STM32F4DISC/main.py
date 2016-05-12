#
# Main file for STM32F4DISCOVERY
#
import pyb
from cs43l22 import CS43L22
from lis3xxx_spi import LIS302DL
from board import sys_config

spi = pyb.SPI(sys_config['lis302dl']['spi_bus'], pyb.SPI.MASTER,
              baudrate=600000, polarity=1, phase=1)
cs_accel = pyb.Pin(sys_config['lis302dl']['spi_cs'], pyb.Pin.OUT_PP)

acc = LIS302DL(spi, cs_accel)
print("Acceleration  (%5.3f, %5.3f, %5.3f)" % acc.xyz())


audioReset = pyb.Pin(sys_config['cs43l22']['resetPin'], pyb.Pin.OUT_PP)
i2c = pyb.I2C(sys_config['cs43l22']['i2c_bus'],
              pyb.I2C.MASTER, baudrate=100000)
snd = CS43L22(i2c, sys_config['cs43l22']['i2c_addr'], audioReset)
snd.init()
