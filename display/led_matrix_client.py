#!/usr/bin/env python

import struct
import serial
class Matrix(object):

    HELLO, WIDTH, HEIGHT, DEPTH, PIXEL, FILL, CLEAR, TEXT = range(48, 48+8)
    CMDS = (HELLO, WIDTH, HEIGHT, DEPTH, PIXEL, FILL, CLEAR, TEXT)
    ANSW_OK, ANSW_ERROR  = b'\0', b'\1'
    ANSW = (ANSW_OK, ANSW_ERROR)
    LINE_SEP = '\x0d\x0a'
    
    DEBUG = False
        
    def __init__(self, com_dev_fname):
        self._com = serial.Serial(com_dev_fname, timeout = 0.1)
        self.clear_serial()
        self._width = self.width()
        self._height = self.height()
        self._depth = self.depth()

    def clear_serial(self):
        data = 1
        while data:
            data=self._com.read()
    
    def _l2str(self, data):
        hex_str = " ".join(["0x%02x" % (ord(i) ) for i in data])
        text_str = "".join(["%s" % (i if i.isalnum() else '.') for i in data])
        return hex_str +"\n" + text_str
    
    def read(self):
        res=[]
        data = self._com.read(10000)
        while data:
            if self.DEBUG:
                print("Received %s" % self._l2str(data))
            data = data.split(self.LINE_SEP)
            for i,l in enumerate(data):
                if len(l)>2:
                    res.append(l)
            data = self._com.read(10000)
        return res
    
    def write(self, data):
        data += self.LINE_SEP
        data = bytearray(data)
        if self.DEBUG:
            bStr = " ".join(["0x%02x" % i for i in data])
            print("Send bytes: %s" % bStr)
        self._com.write(data)
        lines = self.read()
        answ = None
        for l in lines:
            if self.DEBUG:
                print(l)
            if l[0] not in self.ANSW:
                print("Unknown answer \"%s\"" % self._l2str(l))
                continue
            answ = l[1:]
            if self.DEBUG:
                print("Answer %s of lenght %d" % (self._l2str(answ), len(answ)))
            break
        return answ

    def hello(self):
        data = struct.pack("B", self.HELLO)
        answ = self.write(data)
        cnt = struct.unpack("B", answ[0])[0]
        fmt = "%ds" % cnt
        text = struct.unpack(fmt, answ[1:])[0]
        return text

    def width(self):
        data = struct.pack("B", self.WIDTH)
        answ = self.write(data)
        val = struct.unpack("H", answ)[0]
        return val

    def height(self):
        data = struct.pack("B", self.HEIGHT)
        answ = self.write(data)
        val = struct.unpack("H", answ)[0]
        return val

    def depth(self):
        data = struct.pack("B", self.DEPTH)
        answ = self.write(data)
        val = struct.unpack("H", answ)[0]
        return val
    
    def get_color(self, color):
        return struct.pack('BBB', color[0], color[1], color[2])
    
    def get_coord(self, coord):
        return struct.pack("HH", coord[0], coord[1])
    
    def get_string(self, text):
        fmt = "B%ds" % len(text)
        return struct.pack(fmt, len(text), text)
    
    def pixel(self, coord, color = None):
        data =  struct.pack("B", self.PIXEL )
        data += self.get_coord(coord)
        if color:
            data += self.get_color(color)
            self.write(data)
        else:
            res = self.write(data)
            return struct.unpack("BBB", res)
    
    def fill(self, color):
        data = struct.pack("B", self.FILL)
        data += self.get_color(color)
        self.write(data)

    def clear(self):
        data = struct.pack("B", self.CLEAR)
        self.write(data)
        
    def text(self, text, coord, color):
        data =  struct.pack("B", self.TEXT)
        data += self.get_string(text)
        data += self.get_coord(coord)
        data += self.get_color(color)
        self.write(data)
    
if __name__ == '__main__':
    # from led_matrix_client import Matrix
    m=Matrix('/dev/ttyACM0')
    m.hello()
    m.width()
    m.height()
    m.depth()
    m.pixel((0,0))
    m.pixel((0,0), (1,0,0))
    m.pixel((0,0), (0,1,0))
    m.pixel((0,0), (0,0,1))
    m.fill((0,0,15))
    m.clear()
    m.text("This", (0,0), (0,1,0))
    m.text("Work", (0,8), (0,0,1))
    m.text("R", (4,16), (1,0,0))
    m.text("G", (12,16), (0,1,0))
    m.text("B", (20,16), (0,0,1))
    
