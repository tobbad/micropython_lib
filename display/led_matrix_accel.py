

import pyb
import os
import struct
from led_matrix_server import Matrix_Server

class Matrix(pyb.ledmatrix.ledmatrix, Matrix_Server):
        
    DEBUG = False
        
    @staticmethod
    def new(width, height, depth, line_sel, color_sel, clk, le, oe):
        res = []
        for p in line_sel:
            res.append(pyb.Pin(p, mode = pyb.Pin.OUT_PP, pull = pyb.Pin.PULL_NONE))
        line_sel = res
        res = []
        for p in color_sel:
            res.append(pyb.Pin(p, mode = pyb.Pin.OUT_PP, pull = pyb.Pin.PULL_NONE))
        color_sel = res
        res = []
        for p in (clk, le, oe):
            res.append(pyb.Pin(p, mode = pyb.Pin.OUT_PP, pull = pyb.Pin.PULL_NONE))
        clk, le, oe = res
        return Matrix(width, height, depth, line_sel, color_sel, clk, le, oe)
    
    def __init__(self, width, height, depth, line_sel, color_sel, clk, le, oe):
        self._width = width
        self._height = height
        self._depth = depth

    def width(self):
        return self._width

    def height(self):
        return self._height
    
    def depth(self):
        return self._depth
    
    def clear(self):
        self.fill((0,0,0))
