# -*- coding: utf-8 -*-
#
# Unit test for LoraWan MAC
#
import unittest
import sys
from itertools import permutations

sys.path.append('../../mock')

from micropython_lib.mock.led_matrix import Matrix
from micropython_lib.applications.conway import Game


class CreateGame(unittest.TestCase):
    
    SIZE = (4, 6, 3)
    
    def setUp(self):
        self.matrix = Matrix(self.SIZE[0], self.SIZE[1], self.SIZE[2])
        self.matrix.fill((13,2,56))
        self.game = Game(self.matrix)
        

    def test_Create(self):
        self.assertIsNotNone(self.game)
        
    def test_sizes(self):
        board_cnt = 2
        self.assertEqual(len(self.game.board), board_cnt)
        for i in range(board_cnt):
            self.assertEqual(len(self.game.board[i]), self.SIZE[0])
            for column in self.game.board[i]:
                self.assertEqual(len(column), self.SIZE[1])
    
    def test_blank_board(self):
        for b in self.game.board:
            for col in b:
                for cell in col:
                    self.assertEqual(cell, 0)
                    
    def test_blank_screen(self):
        for x in range(self.SIZE[0]):
            for y in range(self.SIZE[1]):
                rgb = self.matrix.pixel((x,y))
                res = all( i==j for i,j in zip(rgb,(0,0,0)))
                self.assertTrue(res)


class Rules(unittest.TestCase):

    SIZE = (11, 11, 3)
    NEI_POS =  ((-1,-1), (0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1), (1,1))
    
    def setUp(self):
        self.matrix = Matrix(self.SIZE[0], self.SIZE[1], self.SIZE[2])
        self.game = Game(self.matrix)
        self.c_pos = self.SIZE[0]>>1, self.SIZE[1]>>1
    
    def test_rule(self):
        for my_state in self.game.states:
            max_cnt = 20
            for i in range(max_cnt):
                res = self.game.rule(my_state, i, max_cnt-i)
                if my_state in ( self.game.CELL_DEAD, self.game.CELL_DYING):
                    exp_res = self.game.CELL_NEWBORN if i==3 else self.game.CELL_DEAD
                    self.assertEqual(res, exp_res)
                else:
                    exp_res = self.game.CELL_DYING
                    if 2<=i<=3:
                        exp_res = self.game.CELL_NEWBORN
                        
    def test_one_item(self):
        for c_type in (self.game.CELL_ALIVE, self.game.CELL_NEWBORN):
            self.game.board[self.game.board_idx][self.c_pos[0]][self.c_pos[1]] = c_type
            res = self.game.cell_evaluate(self.c_pos[0], self.c_pos[1])
            self.assertEqual(res, self.game.CELL_DYING)
    
    def test_one_item(self):
        for c_type in (self.game.CELL_ALIVE, self.game.CELL_NEWBORN):
            self.game.board[self.game.board_idx][self.c_pos[0]][self.c_pos[1]] = c_type
            res = self.game.cell_evaluate(self.c_pos[0], self.c_pos[1])
            self.assertEqual(res, self.game.CELL_DYING)
    
    @unittest.skip("Only run when needed")
    def test_all_neighours(self):
        for c_type in (self.game.CELL_ALIVE, self.game.CELL_NEWBORN):
            for n_cnt in range(1,9):
                for n_type in (self.game.CELL_ALIVE, self.game.CELL_NEWBORN):
                    for n_pos in permutations(self.NEI_POS, n_cnt):
                        # Set up board
                        self.game.clear_board()
                        self.game.board[self.game.board_idx][self.c_pos[0]][self.c_pos[1]] = c_type
                        for nei in n_pos:
                            pos = tuple( i+j for i, j in zip(self.c_pos, nei))
                            self.game.board[self.game.board_idx][pos[0]][pos[1]] = n_type
                        res = self.game.cell_evaluate(self.c_pos[0], self.c_pos[1])
                        exp_res =self.game.CELL_DYING
                        if n_cnt in (2,3):
                            exp_res =self.game.CELL_ALIVE
                        self.assertEqual(res, exp_res)
    
    def test_new_born(self):
        for c_type in ( self.game.CELL_DEAD, self.game.CELL_DYING):
            for n_pos in permutations(self.NEI_POS, 3):
                for n_type in (self.game.CELL_ALIVE, self.game.CELL_NEWBORN):
                    # Set up board
                    self.game.clear_board()
                    self.game.board[self.game.board_idx][self.c_pos[0]][self.c_pos[1]] = c_type
                    for nei in n_pos:
                        pos = tuple( i+j for i, j in zip(self.c_pos, nei))
                        self.game.board[self.game.board_idx][pos[0]][pos[1]] = n_type
                    res = self.game.cell_evaluate(self.c_pos[0], self.c_pos[1])
                    exp_res =self.game.CELL_NEWBORN
                    self.assertEqual(res, exp_res)

    @unittest.skip("Only run when needed")
    def test_no_change(self):
        for c_type in ( self.game.CELL_DEAD, self.game.CELL_DYING):
            for n_cnt in (1,2,4,5,6,7,8):
                for n_pos in permutations(self.NEI_POS, n_cnt):
                    for n_type in (self.game.CELL_ALIVE, self.game.CELL_NEWBORN):
                        # Set up board
                        self.game.clear_board()
                        self.game.board[self.game.board_idx][self.c_pos[0]][self.c_pos[1]] = c_type
                        for nei in n_pos:
                            pos = tuple( i+j for i, j in zip(self.c_pos, nei))
                            self.game.board[self.game.board_idx][pos[0]][pos[1]] = n_type
                        res = self.game.cell_evaluate(self.c_pos[0], self.c_pos[1])
                        exp_res = self.game.CELL_DEAD
                        self.assertEqual(res, exp_res)

if __name__ == '__main__':
    unittest.main()
