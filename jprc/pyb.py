#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    pyb stub for code on the python board side.
    Created on 10.12.2017
    @author: Tobias Badertscher

"""
import serial
import os

uart_dev = os.sep.join(("", "dev", "ttyACM2"))
baud = 115200


def main():
    com = serial.Serial(uart_dev, baudrate=baud, timeout=80.0/baud)
    while True:
        data=bytes("Hello world!", "ascii")
        com.write(data)
        ans = com.read(100)
        if ans is not None and len(ans)>0:
            print(ans)


if __name__ == '__main__':
    main()

