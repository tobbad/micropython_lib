#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Module to bundle several port pins to a 8 or 16 bit port
    Created on 8.4.2017
    @author: Tobias Badertscher

"""

class Port:
    
    READ = 0
    WRITE = 1

    def __init__(self, pins):
        cnt = len(pins)
        if (cnt != 8) and (cnt != 16):
            raise Exception("Only 8/16 pin port supported\nGot %d" % cnt)
        self._pins = pins
        self._mode = self.WRITE
        self.mode(self.READ)

    def mode(self, mode = READ):
        if mode != self._mode:
            pmode = self._pins[0].IN if mode is Port.READ else self._pins[0].OUT_PP
            for p in self._pins:
                p.init(pmode)
            self._mode = mode

    def read(self):
        res = 0
        for idx, p in enumerate(self._pins):
            res += 1<<idx if p.value() else 0
        return res

    def write(self, value):
        msk = 1
        for idx, p in enumerate(self._pins):
            val = 1 if value & msk else 0
            p.value(val) 
            msk <<= 1

    


if __name__ == '__main__':
    pass

