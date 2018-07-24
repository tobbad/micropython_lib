#!/usr/bin/env python
#
# Main file for STM32F4DISCOVERY
#
import os
import sys

import pyb
from board import config
from sx127x import SX127X

lis_cs = pyb.Pin(config['lis302dl']['spi_cs'], pyb.Pin.OUT_PP)
lis_cs.value(1)

reset = pyb.Pin(config['rf96']['resetPin'], pyb.Pin.OUT_PP)
reset.value(1)
cs = pyb.Pin(config['rf96']['spi_cs'], pyb.Pin.OUT_PP)
cs.value(1)

spi = pyb.SPI(config['rf96']['spi_bus'], pyb.SPI.MASTER, baudrate=500000, polarity=config['rf96']['spi_polarity'], phase=config['rf96']['spi_phase'])

dio_pins=(config['rf96']['DIO_0'], config['rf96']['DIO_1'], config['rf96']['DIO_2'], config['rf96']['DIO_3'])

lora = SX127X(spi, cs, reset, dio_pins)
