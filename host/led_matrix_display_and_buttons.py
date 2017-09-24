#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import math
import numpy as np
import threading

   
class Matrix:
    
    TILESIZE = 25
    COLOR={'red':(255,0,0), 'green':(0,255,0)}
    
    def __init__(self, width, height, *args):
        self.led_cnt = (width, height)
        self.size = (width*self.TILESIZE, height*self.TILESIZE)
        # key bindings
        self.move_map = {pygame.K_LEFT: (-1, 0),
                    pygame.K_RIGHT: (1, 0),
                    pygame.K_UP: (0, -1),
                    pygame.K_DOWN: (0, 1)}
        self.speed = 1
        self.radius = 10
        self.screen = None
        self.board = np.zeros((self.led_cnt[0], self.led_cnt[1],3), dtype = 'uint8')
            
    def pixel(self, pos, color=None):
        if color:
            coord = pos[0]*self.TILESIZE+self.radius, pos[1]*self.TILESIZE+self.radius
            pygame.draw.circle(self.screen, color, map(int, coord), self.radius)
            pygame.display.flip()
            self.board[pos[0]][pos[1]] = color
        else:
            return self.board[pos[0]][pos[1]]

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.size[0], self.size[1]))
        self.clock = pygame.time.Clock()
        run = True
        pos = (self.size[0]/2, self.size[1]/2)
        while run:
            for e in pygame.event.get():
                if e.type == pygame.QUIT: run = False
            
    def fill_it(self):
        self.screen.fill((0, 0, 0))
        for y in range(self.led_cnt[1]):
            for x in range(self.led_cnt[0]):
                self.pixel((x,y), (self.COLOR['red']))


        self.clock.tick(60)
        
    def t_run(self):
        t = threading.Thread(target=self.run)
        t.start()

  
  

  
if __name__ == '__main__':
    m = Matrix(32, 32, 8)
    m.t_run()
    while True:
        for i in range(m.size[0]):
            m.pixel((i,i), (i*15, 0, 0))
