#!/usr/bin/python3

from zybo import ZYBO
from micropython_lib.rf.at86rf215 import AT86RF215
import time

dev_name = '/dev/ttyUSB1'

if __name__ == '__main__':
    zybo = ZYBO(dev_name)
    at86 = AT86RF215(zybo.spi, None)
    at86.
    print(at86.chip_mode())
    at86.chip_mode('RF_MODE_BBRF')
    print(at86.chip_mode())
    print(at86.transceiver_state('RF09'))
    at86.transceiver_command('RF09', 'RF_TX')
    time.sleep(1)
    print(at86.transceiver_state('RF09'))
