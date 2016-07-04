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

tetris = Tetris(matrix, sw)
conway = Game(matrix, sw[0])
#tetris.run(250)
#matrix.server()
