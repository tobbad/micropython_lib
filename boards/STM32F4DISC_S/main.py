#
# Main file for STM32F4DISCOVERY
#
import pyb
from board import sys_config
from led_matrix import LED_MATRIX

matrix = LED_MATRIX(32, 32, sys_config['led_matrix']['red'],  sys_config['led_matrix']['green'],  sys_config['led_matrix']['blue'],
                    sys_config['led_matrix']['a'], sys_config['led_matrix']['b'], sys_config['led_matrix']['c'], sys_config['led_matrix']['d'], 
                    sys_config['led_matrix']['clk'], sys_config['led_matrix']['latch'], sys_config['led_matrix']['oe'])   

#while True:
#    matrix.update()
