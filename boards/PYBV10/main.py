#
# Main file for STM32F4DISCOVERY
#
import pyb
from sx127x import SX127X
from mma7660 import MMA7660
from board import sys_config


i2c = pyb.I2C(sys_config['mma7660']['i2c_bus'],
              pyb.I2C.MASTER, baudrate=100000)

vdda = pyb.Pin(sys_config['mma7660']['avdd'], pyb.Pin.OUT_PP)

vdda.low()
pyb.delay(30)
vdda.high()
pyb.delay(30)

accel = MMA7660(i2c, sys_config['mma7660']['i2c_addr'])
print("Acceleration  (%.3e, %.3e, %.3e)" % accel.xyz())

spi = pyb.SPI(sys_config['sx127x']['spi_bus'], pyb.SPI.MASTER,
              baudrate=600000, polarity=1, phase=1)
cs = pyb.Pin(sys_config['sx127x']['spi_cs'], pyb.Pin.OUT_PP)

rf = SX127X(spi, cs)

while True:
    print("%3d, %3d, %3d" % ( accel.x(), accel.y(), accel.z()))
    pyb.delay(100)
