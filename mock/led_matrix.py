 


#!/usr/bin/env python

import struct
import serial
import numpy as np


class Matrix(object):

    DEBUG = False
        
    def __init__(self, width, height, depth, *para):
        self._width = width
        self._height = height
        self._depth = depth
        assert(depth<256)
        self._board = np.zeros((self._width, self._height, 3), dtype = 'uint8')

    def width(self):
        return self._width

    def height(self):
        return self._height
    
    def depth(self):
        return self._depth

    def pixel(self, pos, color=None):
        if color:
            self.dprint("Set Pixel[%d][%d] = (%d, %d, %d)" % (pos[0], pos[1], color[0], color[1], color[2]))              
            self._board[pos[0]][pos[1]] = color
        else:
            return self._board[pos[0]][pos[1]]
    
    def fill(self, color):
        self._board[:][:] = color

    def clear(self):
        self.fill((0,0,0))
        
    def text(self, text, coord, color):
        pass
 
    def show(self):
        pass
 
    def update(self):
        return 1
    
    def board(self):
        return self._board
 
    def dprint(self, *args):
        if self.DEBUG:
            print(args[0])
