#!/usr/bin/env python
""" Conway's Game of Life, drawn to the led_matrix
"""
#from conway import Game ; g=Game(matrix);g.run(250)
from pyb import rng, delay


class Game():
    
    CELL_DEAD, CELL_DYING, CELL_ALIVE, CELL_NEWBORN = range(4)
    COLOR_DEAD, COLOR_DYING, COLOR_ALIVE, COLOR_NEWBORN = (0,0,0) , (1,0,0), (0,1,0), (0,0,1)
    DEBUG = True
    
    def __init__(self, display, new_game_pin = None):
        self.disp = display
        self.boring = False
        self.board = [[[self.CELL_DEAD for y in range(self.disp.height())] for x in range(self.disp.width()) ] for cnt in range(2)]
        self.board_idx = 0
        self.total_alive = 0
        self.new_game_pin = new_game_pin
        self.clear_board()
        self.disp.clear()
        self.states = self.CELL_DEAD, self.CELL_DYING, self.CELL_ALIVE, self.CELL_NEWBORN
        
    def clear_board(self):
        for x, column in enumerate(self.board[self.board_idx]):
            for y, cell in enumerate(column):
                self.board[0][x][y] = self.CELL_DEAD
                self.board[1][x][y] = self.CELL_DEAD
       
   
    def seed(self, seed_cnt):
        for i in range(seed_cnt):
            x = rng() % self.disp.width()
            y = rng() % self.disp.height()
            self.board[self.board_idx][x][y] = self.CELL_NEWBORN
        
    def draw(self):
        for x, column in enumerate(self.board[self.board_idx]):
            for y, cell in enumerate(column):
                color = self.COLOR_DEAD
                if cell == self.CELL_DYING:
                    color = self.COLOR_DYING
                elif cell == self.CELL_ALIVE:
                    color = self.COLOR_ALIVE
                elif cell == self.CELL_NEWBORN:
                    color = self.COLOR_NEWBORN
                self.disp.pixel((x,y),  color)
        
    def rule(self, my_state, cnt_alive, cnt_dead):
        result = self.CELL_DEAD
        if my_state in ( self.CELL_DEAD, self.CELL_DYING):
            if cnt_alive == 3:
                result = self.CELL_NEWBORN
        else:
            if cnt_alive < 2:
                result = self.CELL_DYING
            elif cnt_alive in (2,3):
                result = self.CELL_ALIVE
            elif cnt_alive > 3:
                result = self.CELL_DYING
        if my_state in (self.CELL_ALIVE, self.CELL_NEWBORN):
            self.total_alive +=1
        if my_state != result:
            self.total_changed +=1
        return result
        
    def cell_evaluate(self, x0, y0):
        cnt_dead = 0
        cnt_alive = 0
        my_state = self.board[self.board_idx][x0][y0]
        for y in range(y0-1, y0+2):
            y = y % self.disp.height()
            for x in range(x0-1, x0+2):
                x = x %self.disp.width()
                if x==x0 and y==y0:
                    continue
                cnt_dead += 1 if self.board[self.board_idx][x][y] in (self.CELL_DYING, self.CELL_DEAD) else 0
                cnt_alive += 1 if self.board[self.board_idx][x][y] in (self.CELL_NEWBORN, self.CELL_ALIVE) else 0
        return self.rule(my_state, cnt_alive, cnt_dead)
       
    def run(self, cnt = 250):
        self.disp.start()
        while True:
            self.disp.clear()
            self.boring = False
            self.board_idx = 0
            self.clear_board()
            self.seed(cnt)
            self.draw()
            delay(100)
            generation = 0
            while not self.boring:
                print("Generation %d -> %d" % (generation, generation+1))
                self.total_alive = 0
                self.total_changed = 0
                for x, column in enumerate(self.board[self.board_idx]):
                    for y, cell in enumerate(column):
                        self.board[(self.board_idx+1)%2][x][y] = self.cell_evaluate(x, y)
                self.board_idx = (self.board_idx+1)%2
                self.draw()
                if self.total_alive == 0 or self.total_changed==0:
                    self.boring = True
                generation+=1
                if self.new_game_pin:
                    if self.new_game_pin.value()==0:
                        self.boring = True
                
 
