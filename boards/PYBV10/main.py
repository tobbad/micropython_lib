#
# Main file for STM32F4DISCOVERY
#
import pyb
from sx127x import SX127x
from board import sys_config

spi = pyb.SPI(sys_config['sx127x']['spi_bus'], pyb.SPI.MASTER,
              baudrate=600000, polarity=1, phase=1)
cs = pyb.Pin(sys_config['sx127x']['spi_cs'], pyb.Pin.OUT_PP)

rf = SX127X(spi, cs)
