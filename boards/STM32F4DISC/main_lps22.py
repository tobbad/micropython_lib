#!/usr/bin/env python
#
# Main file for STM32F4DISCOVERY
#
import os
import sys

import pyb
from board import sys_config
from lps22hb import LPS22HB

i2c=pyb.I2C(sys_config['pmod']['p7']['i2c_bus'],  pyb.I2C.MASTER, baudrate=100000)

sen = LPS22HB(i2c,  0x5C)
