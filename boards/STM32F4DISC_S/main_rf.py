#!/usr/bin/env python
#
# Main file for STM32F4DISCOVERY
#
import os
import sys

import pyb
from board import sys_config
from at86rf215 import AT86RF215
import bitbang


reset = pyb.Pin(sys_config['at86rf215']['reset'], pyb.Pin.OUT_PP)
reset.value(1)
cs = pyb.Pin(sys_config['at86rf215']['spi_cs'], pyb.Pin.OUT_PP)
cs.value(1)

spi = pyb.SPI(sys_config['at86rf215']['spi_bus'], pyb.SPI.MASTER, baudrate=600000, polarity=sys_config['at86rf215']['spi_polarity'], phase=sys_config['at86rf215']['spi_phase'])
sck = pyb.Pin(sys_config['at86rf215']['spi_bit_bang']['sck'], pyb.Pin.OUT_PP)
mosi = pyb.Pin(sys_config['at86rf215']['spi_bit_bang']['mosi'], pyb.Pin.OUT_PP)
bb_cs = pyb.Pin(sys_config['at86rf215']['spi_bit_bang']['nss'], pyb.Pin.OUT_PP)
bb_cs_p3 = pyb.Pin(sys_config['at86rf215']['spi_bit_bang_P3']['nss'], pyb.Pin.OUT_PP)
miso = pyb.Pin(sys_config['at86rf215']['spi_bit_bang']['miso'])

spi_bb = bitbang.SPI(sck, mosi, miso,
                     polarity=sys_config['at86rf215']['spi_polarity'],
                     phase=sys_config['at86rf215']['spi_phase'])
at86 = AT86RF215(spi, cs)
at86 = AT86RF215(spi_bb, bb_cs)
at86 = AT86RF215(spi_bb, bb_cs_p3)
at86.read(0x0d)
