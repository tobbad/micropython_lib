# -*- coding: utf-8 -*-
#
# Unit test for LoraWan MAC
#
import unittest
import os
import sys
import numpy as np

sys.path.append('../../mock')

from micropython_lib.mock.led_matrix import Matrix
from micropython_lib.applications.tetris import Tetris, Stone, Board

class Board_mock:
    
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._board = np.zeros((self._width, self._height), dtype='uint8')
        
    def pixel(self, coord, color=None):
        if color:
            if isinstance(color, (tuple,list)):
                raise ValueError("No tuple on board allowed")
            self._board[coord[0]][coord[1]] = color
        else:
            return self._board[coord[0]][coord[1]]

    def __str__(self):
        res = [os.linesep]
        res.append("   |"+"|".join(( " %2d" % i for i in range(self._width))))
        res.append("-"+("-"*(4*self._width+3)))
        for y in range(self._height):
            l="%2d |" % y
            for x in range(self._width):
                val = self._board[x][y]
                l += ("   |" if val == 0 else " %1d |" % val)
            res.append(l)
            res.append("-"+("-"*(4*self._width+3)))
        return os.linesep.join(res)


class ShapeTest(unittest.TestCase):
    
    SIZE = (16, 10)
    POS = (4, 0)
    SHAPE_NR = 6
    
    def setUp(self):
        self.stone = Stone(self.SIZE[0], self.SIZE[1], self.POS[0], self.POS[1], self.SHAPE_NR)
        self.board = Board_mock(self.SIZE[0], self.SIZE[1])

    def test_Create(self):
        self.assertIsNotNone(self.stone)
        
    def test_location(self):
        self.assertEqual(self.stone.coord[0], self.POS[0])
        self.assertEqual(self.stone.coord[1], self.POS[1])
        
    def test_move(self):
        for y in range(self.SIZE[1]):
            collide = self.stone.move((0,1), self.board)
            if y < self.SIZE[1]-1:
                self.assertFalse(collide) 
                self.assertEqual(self.stone.coord[1], y+1)
            else:
                self.assertTrue(collide) 
                self.assertEqual(self.stone.coord[1], y)
            
    def test_move_along_left(self):
        collide = self.stone.move((-4,0), self.board)
        self.assertFalse(collide) 
        for y in range(self.SIZE[1]):
            collide = self.stone.move((-1,1), self.board)
            if y < self.SIZE[1]-1:
                self.assertFalse(collide) 
                self.assertEqual(self.stone.coord[1], y+1)
            else:
                self.assertTrue(collide) 
                self.assertEqual(self.stone.coord[1], y)

    def test_move_along_right(self):
        collide = self.stone.move((8,0), self.board)
        self.assertFalse(collide) 
        for y in range(self.SIZE[1]):
            collide = self.stone.move((1,1), self.board)
            if y < self.SIZE[1]-1:
                self.assertFalse(collide) 
                self.assertEqual(self.stone.coord[1], y+1)
            else:
                self.assertTrue(collide) 
                self.assertEqual(self.stone.coord[1], y)

    def test_rotate_collide(self):
        collide = self.stone.move((0,6), self.board)
        collide = self.stone.rotate(self.board)
        self.assertFalse(collide) 
        collide = self.stone.move((0,1), self.board)
        self.assertTrue(collide) 
        self.stone.draw(self.board, self.SHAPE_NR)

    def test_collide_with_other_stone(self):
        stone = Stone(self.SIZE[0], self.SIZE[1], self.POS[0], self.POS[1], self.SHAPE_NR)
        stone.move((0, 9), self.board)
        stone.draw(self.board, self.SHAPE_NR)
        for y in range(self.SIZE[1]):
            collide = self.stone.move((0,1), self.board)
            if y < self.SIZE[1]-2:
                self.assertFalse(collide) 
                self.assertEqual(self.stone.coord[1], y+1)
            else:
                self.assertTrue(collide) 
                self.assertEqual(self.stone.coord[1], 8)
        #self.stone.draw(self.board, self.SHAPE_NR)
        #print(self.board)
    
class BoardTest(unittest.TestCase):

    SIZE = (5, 11)
    
    def setUp(self):
        self.board = Board(self.SIZE[0], self.SIZE[1])
     
    def fill_line(self, y, val):
        for x in range(self.SIZE[0]):
            self.board.pixel((x,y), val)
    
    def fill_mark_line(self, y, val):
        for x in range(self.SIZE[0]):
            self.board.pixel((x,y), val if x%2 else 0)
    
    def check_for_value(self, y, exp_val):
        res = True
        for x in range(self.SIZE[0]):
            val = self.board.pixel((x,y))
            if val != exp_val:
                break
        else:
            return True
        return False
    

    def fill_mark_line(self, y, val):
        for x in range(self.SIZE[0]):
            self.board.pixel((x,y), val if x%2 else 0)

    def check_for_marker(self, y, fill_val):
        res = True
        for x in range(self.SIZE[0]):
            exp_val = fill_val if x%2 else 0
            val = self.board.pixel((x,y))
            if val != exp_val:
                print("Pixel[%d, %d] = %d != %d" % (x,y, val, exp_val) )
                break
        else:
            return True
        return False
     
    def test_line_fill_check(self):
        y=0
        self.fill_line(y,1)
        self.assertFalse(self.check_for_value(y, 0))
      
    def test_marker_check(self):
        y=0
        self.fill_mark_line(y,1)
        self.assertTrue(self.check_for_marker(y,1))
      
    def test_remove_nothing(self):
        rem_line = self.board.remove_full_line()
        self.assertFalse(rem_line)

    def test_remove_top_line(self):
        y=0
        self.fill_line(y,1)
        rem_line = self.board.remove_full_line()
        self.assertTrue(rem_line)
        res = self.check_for_value(y, 0)
        self.assertTrue(res)
        
    def test_remove_bottom_line(self):
        y=self.SIZE[1]-1
        self.fill_line(y, 1)
        rem_line = self.board.remove_full_line()
        self.assertTrue(rem_line)
        #self.board.to_term()
        res = self.check_for_value(y, 0)
        self.assertTrue(res)
      
    def test_copy_line(self):
        y=self.SIZE[1]-1
        self.fill_line(y,1)
        rem_line = self.board.copy_line(y,0)
        #self.board.to_term()
        res = self.check_for_value(0, 1)
        self.assertTrue(res)
        res = self.check_for_value(y, 1)
        self.assertTrue(res)
        
    def test_move_marker_lines_above(self):
        y=5
        marker = 4
        self.fill_line(y, 1)
        self.fill_mark_line(y-1, marker)
        rem_line = self.board.remove_full_line()
        #self.board.to_term()
        res = self.check_for_marker(y, marker)
        self.assertTrue(res)
        
    def test_no_move_marker_lines_below(self):
        y=5
        marker = 4
        self.fill_line(y, 1)
        self.fill_mark_line(y+1, marker)
        rem_line = self.board.remove_full_line()
        #self.board.to_term()
        res = self.check_for_marker(y+1, marker)
        self.assertTrue(res)
        
    def test_delete_multiple(self):
        for y in range(self.board.height):
            if y%2:
                self.fill_line(y, 1)
            else:
                self.fill_mark_line(y, y/2)
        # Test
        rem_line = self.board.remove_full_line()
        #
        # Evaluate
        #
        for y in range(self.board.height):
            exp_mark = 0 if y<6 else y-5
            res = self.check_for_marker(y, exp_mark)
            self.assertTrue(res)


if __name__ == '__main__':
    unittest.main()
