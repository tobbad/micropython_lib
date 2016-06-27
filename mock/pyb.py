#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

class Pin:
    
    IN, OUT_PP, OUT_OD, AF_PP, AF_OD, ANALOG = list(range(6))

    PULL_NONE, PULL_UP, PULL_DOWN = list(range(3))

    DEBUG = True

    def __init__(self, name, mapped_key, active=True):
        self._pin = name
        self._key = mapped_key
        self._active = 1 if active else 0
        self._inactive = 0 if active else 1
        if self.DEBUG:
            print("Key %s created" % name)
        
        
    def value(self):
        pressed  =0
        print(pressed)
        for k in pressed:
            if k == self._key:
                return self._active
            else:
                return self._inactive
                



def rng():
    return random.randint(0, 2<<30)

def delay(t=0):
    pass


if __name__ == '__main__':
    up=Pin('PB7', pygame.K_UP, False)
    while True:
        print("Key up is %s" % "off" if up.value() else "on")
            
