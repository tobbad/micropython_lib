#!/usr/bin/env python
#
# Main file for STM32F4DISCOVERY
#
import os
import sys

if os.uname()[0] == 'Linux':
    sys.path.append('../../display')
    from led_matrix_client import Matrix
    matrix = Matrix('/dev/ttyACM0')
    sys.path.append('../../mock')
    sys.path.append('../../applications')
else:
    from board import sys_config
    from led_matrix_accel import Matrix
    matrix = Matrix.new(32,32, 1, sys_config['led_matrix']['line_sel'], sys_config['led_matrix']['color'], sys_config['led_matrix']['clk'], sys_config['led_matrix']['latch'], sys_config['led_matrix']['oe'])
    from micropyGPS import MicropyGPS

from tetris import Tetris
from conway import Game
import pyb

#matrix = LED_MATRIX(32, 32, 3, sys_config['led_matrix']['red'],  sys_config['led_matrix']['green'],  sys_config['led_matrix']['blue'],
#                    sys_config['led_matrix']['a'], sys_config['led_matrix']['b'], sys_config['led_matrix']['c'], sys_config['led_matrix']['d'],
#                    sys_config['led_matrix']['clk'], sys_config['led_matrix']['latch'], sys_config['led_matrix']['oe'])

ti=pyb.Timer(8)
matrix.timer(ti)

sw = []
for s, c in zip(sys_config['switch']['pins'], sys_config['switch']['conf']):
    sw.append(pyb.Pin(s, mode=c[0], pull = c[1]))

#tetris = Tetris(matrix, sw)
#conway = Game(matrix, sw[0])
#game.run(250)
#matrix.server()


def gps():

    new_data = False
    # Callback Function
    def pps_callback(line):
        global new_data  # Use Global to trigger update
        new_data = True

    # Instantiate the micropyGPS object
    my_gps = MicropyGPS()

    # Setup the connection to your GPS here
    # This example uses UART 3 with RX on pin Y10
    # Baudrate is 9600bps, with the standard 8 bits, 1 stop bit, no parity
    # Also made the buffer size very large (1000 chars) to accommodate all the characters that stack up
    # each second
    uart = pyb.UART(sys_config['pmod']['p3']['uart'], 9600, read_buf_len=1000)

    # Release Reset
    reset = pyb.Pin(sys_config['pmod']['p3']['reset'], pyb.Pin.OUT_PP)
    reset.high()

    # Create an external interrupt on pin X8
    pps_pin = pyb.Pin(sys_config['pmod']['p3']['one_pps'], pyb.Pin.IN, pull=pyb.Pin.PULL_UP)
    extint = pyb.ExtInt(pps_pin, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, pps_callback)

    # Main Infinite Loop
    while 1:
        # Do Other Stuff Here.......

        # Update the GPS Object when flag is tripped
        if new_data:
            while uart.any():
                my_gps.update(chr(uart.readchar()))  # Note the conversion to to chr, UART outputs ints normally
            #print('UTC Timestamp:', my_gps.timestamp)
            print('Date:', my_gps.date_string('long'))
            print('Latitude:', my_gps.latitude_string())
            print('Longitude:', my_gps.longitude_string())
            print('Horizontal Dilution of Precision:', my_gps.hdop)
            print('Satellites in use:', my_gps.satellites_in_use)
            print()
            new_data = False  # Clear the flag

