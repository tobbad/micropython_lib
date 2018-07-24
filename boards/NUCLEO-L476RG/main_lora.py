#!/usr/bin/env python
#
# Main file for STM32F4DISCOVERY
#
import os
import sys

import pyb
from board import config
from dragino_LoRa_1_3 import config as sconfig
from sx127x import SX127X


reset = pyb.Pin(sconfig['NUGLEO_L476RG']['spi']['resetPin'], pyb.Pin.OUT_PP)
reset.value(1)
cs = pyb.Pin(sconfig['NUGLEO_L476RG']['spi']['spi_cs'], pyb.Pin.OUT_PP)
cs.value(1)

spi = pyb.SPI(sconfig['NUGLEO_L476RG']['spi']['spi_bus'], pyb.SPI.MASTER, baudrate=600000, polarity=sconfig['NUGLEO_L476RG']['spi']['spi_polarity'], phase=sconfig['NUGLEO_L476RG']['spi']['spi_phase'])

lora = SX127X(spi, cs, reset)