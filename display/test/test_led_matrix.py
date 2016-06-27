# -*- coding: utf-8 -*-
#
# Unit test for LoraWan MAC
#
import unittest
import sys

from micropython_lib.mock.led_matrix import Matrix


class CreateMatrixMock(unittest.TestCase):
    
    SIZE = (4, 6, 3)
    
    DEBUG = False
    
    def setUp(self):
        self.matrix = Matrix(self.SIZE[0], self.SIZE[1], self.SIZE[2])

    def test_size(self):
        self.assertEqual(self.SIZE[0], self.matrix.width())
        self.assertEqual(self.SIZE[1], self.matrix.height())
        self.assertEqual(self.SIZE[2], self.matrix.depth())

    def test_blank_after_create(self):
        data = self.matrix.board()
        for x in range(self.SIZE[0]):
            for y in range(self.SIZE[1]):
                res = all( i==j for i,j in zip(data[x][y],(0,0,0)))
                self.assertTrue(res)

    def test_fill(self):
        fill_color = (1,4,8)
        self.matrix.fill(fill_color)
        data = self.matrix.board()
        for x in range(self.SIZE[0]):
            for y in range(self.SIZE[1]):
                if self.DEBUG:
                    print("Pixel[%d, %d] = (%d, %d, %d)" %(x, y, data[x][y][0], data[x][y][1], data[x][y][2]))
                    print([i==j for i,j in zip(data[x][y],fill_color)])
                res = all( i==j for i,j in zip(data[x][y],fill_color))
                self.assertTrue(res)

    def test_clear(self):
        fill_color = (1,4,8)
        exp_color = (0,0,0)
        self.matrix.fill(fill_color)      
        self.matrix.clear()
        data = self.matrix.board()
        for x in range(self.SIZE[0]):
            for y in range(self.SIZE[1]):
                if self.DEBUG:
                    print("Pixel[%d, %d] = (%d, %d, %d)" %(x, y, data[x][y][0], data[x][y][1], data[x][y][2]))
                    print([i==j for i,j in zip(data[x][y],fill_color)])
                res = all( i==j for i,j in zip(data[x][y], exp_color))
                self.assertTrue(res)

    def test_pixel(self):
        for x in range(self.SIZE[0]):
            for y in range(self.SIZE[1]):
                exp_color = (x,y, x*y%256)
                self.matrix.pixel((x,y),exp_color)
                cell = self.matrix.board()[x][y]
                res = all( i==j for i,j in zip(cell,exp_color))
                self.assertTrue(res)
         



if __name__ == '__main__':
    unittest.main()
