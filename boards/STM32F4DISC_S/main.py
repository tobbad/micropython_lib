#
# Main file for STM32F4DISCOVERY
#
import pyb
from board import sys_config
from tetris import Tetris
from led_matrix_accel import Matrix

#matrix = LED_MATRIX(32, 32, 3, sys_config['led_matrix']['red'],  sys_config['led_matrix']['green'],  sys_config['led_matrix']['blue'],
#                    sys_config['led_matrix']['a'], sys_config['led_matrix']['b'], sys_config['led_matrix']['c'], sys_config['led_matrix']['d'], 
#                    sys_config['led_matrix']['clk'], sys_config['led_matrix']['latch'], sys_config['led_matrix']['oe'])   


matrix = Matrix.new(32,32, 3, sys_config['led_matrix']['line_sel'], sys_config['led_matrix']['color'], sys_config['led_matrix']['clk'], sys_config['led_matrix']['latch'], sys_config['led_matrix']['oe'])

ti=pyb.Timer(8)
matrix.timer(ti)

sw = []
for s, c in zip(sys_config['switch']['pins'], sys_config['switch']['conf']):
    sw.append(pyb.Pin(s, mode=c[0], pull = c[1]))

#game = Tetris(matrix, sw)
matrix.server()

def show(cnt=1):
    res = []
    for i in range(15*16*cnt):
        res.append(matrix.update())
    print(min(res), max(res), sum(res)/len(res), len(res))
    return res

def test(cnt=1):
    for col in (1,2,4,8):
        for y in range(32):
            for x in range(32):
                matrix.pixel((x,y), (col,0,0))
                show(cnt)
                matrix.pixel((x,y), (0,0,0))
    show()

def dia():
    for i in range(32):
        matrix.pixel((i,i),(15,15,15))
        if (i>0):
            matrix.pixel((i-1,i-1),(0,0,0))
        pyb.delay(100)   
    matrix.pixel((31,31),(0,0,0))
        
