#!/usr/bin/env python

""" A simple beacon transmitter class to send a 1-byte message (0x0f) in regular time intervals. """

# Copyright 2015 Mayer Analytics Ltd.
#
# This file is part of pySX127x.
#
# pySX127x is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# pySX127x is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You can be released from the requirements of the license by obtaining a commercial license. Such a license is
# mandatory as soon as you develop commercial activities involving pySX127x without disclosing the source code of your
# own applications, or shipping pySX127x with a closed source product.
#
# You should have received a copy of the GNU General Public License along with pySX127.  If not, see
# <http://www.gnu.org/licenses/>.

#
# Modified 19.5.2016 to support python board in micropython
# T. Badertscher
#


import sys
from sx127x_a import *
from board import sys_config


class LoRaBeacon(SX127X):

    tx_counter = 0

    def __init__(self, spi, cs, reset, dio_pins, verbose=False):
        super().__init__(spi, cs, reset, dio_pins, verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([1,0,0,0,0,0])

    def on_rx_done(self):
        print("\nRxDone")
        print(self.get_irq_flags())
        print(map(hex, self.read_payload(nocheck=True)))
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

    def on_tx_done(self):
        self.set_mode(MODE.STDBY)
        self.clear_irq_flags()
        sys.stdout.flush()
        self.tx_counter += 1
        sys.stdout.write("\rtx #%d" % self.tx_counter)
        pyb.delay(100)
        self.write_payload([0x0f])
        self.set_mode(MODE.TX)

    def on_cad_done(self):
        print("\non_CadDone")
        print(self.get_irq_flags())

    def on_rx_timeout(self):
        print("\non_RxTimeout")
        print(self.get_irq_flags())

    def on_valid_header(self):
        print("\non_ValidHeader")
        print(self.get_irq_flags())

    def on_payload_crc_error(self):
        print("\non_PayloadCrcError")
        print(self.get_irq_flags())

    def on_fhss_change_channel(self):
        print("\non_FhssChangeChannel")
        print(self.get_irq_flags())

    def start(self):
        sys.stdout.write("\rstart")
        self.tx_counter = 0
        self.write_payload([0x0f])
        self.set_mode(MODE.TX)
        while True:
            pyb.delay(1)


spi = pyb.SPI(sys_config['sx127x']['spi_bus'], pyb.SPI.MASTER,
              baudrate=600000, polarity=1, phase=1)
cs = pyb.Pin(sys_config['sx127x']['spi_cs'], pyb.Pin.OUT_PP)
reset = pyb.Pin(sys_config['sx127x']['reset'], pyb.Pin.OUT_PP)
dio_pins = ['Y6', 'Y7', 'Y8', 'Y4']

lora = LoRaBeacon(spi, cs, reset, dio_pins, verbose=False)

lora.set_pa_config(pa_select=1)
#lora.set_rx_crc(True)
#lora.set_agc_auto_on(True)
#lora.set_lna_gain(GAIN.NOT_USED)
#lora.set_coding_rate(CODING_RATE.CR4_6)
#lora.set_implicit_header_mode(False)
#lora.set_pa_config(max_power=0x04, output_power=0x0F)
#lora.set_pa_config(max_power=0x04, output_power=0b01000000)
#lora.set_low_data_rate_optim(True)
#lora.set_pa_ramp(PA_RAMP.RAMP_50_us)


#print(lora)
#assert(lora.get_lna()['lna_gain'] == GAIN.NOT_USED)
assert(lora.get_agc_auto_on() == 1)

#lora.start()
