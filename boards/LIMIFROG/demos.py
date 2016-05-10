# -*- coding: utf-8 -*-
import pyb

def clamp(x, vx, xmax, border, r):
    if x <= border+r:
        vx=0
        x = border+r+1
    if x >= xmax-border-r-1:
        vx=0
        x = xmax-border-r-2
    return x, vx


def gravity(disp, accel):
    border = 5
    color = 0x0FF0
    dt = 0.1
    r = 5
    x,y = (disp.XSIZE>>1), (disp.YSIZE>>1)
    xo,yo= x, y
    vx, vy = 0 , 0
    m = 1E-4
    disp.box(0, 0, disp.XSIZE-1, disp.YSIZE-1, 0xFFFF)
    disp.box(border, border, disp.XSIZE-border-1, disp.YSIZE-border-1, 0)
    while True:
        xn, yn = int(x+0.5), int(y+0.5)
        disp.box(xo-r, yo-r, xo+r, yo+r+1, 0)
        disp.circle(xn, yn, r, color)
        xo , yo = xn, yn
        ax, ay, az = accel.xyz()
        ay *= -1
        vx = vx + ax * dt
        vy = vy + ay * dt
        x = x + vx*dt
        y = y + vy*dt
        x, vx = clamp(x, vx, disp.XSIZE, border, r)
        y, vy = clamp(y, vy, disp.YSIZE-1, border, r)


def colors(disp):
    while True:
        color = randint(0, 2**16-1)
        disp.box(0, 0, 159, 127, color)
        #pyb.delay(200)
