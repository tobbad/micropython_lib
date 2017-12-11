#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    pyb stub for code on the python board side.
    Created on 10.12.2017
    @author: Tobias Badertscher

"""
import serial
from micropython_lib.common.datalink import Datalink
import os
import time

uart_dev = os.sep.join(("", "dev", "ttyACM1"))
baud = 115200
timeout =0.0018


class dl_com(serial.Serial):

    TIMEOUT = timeout

    def any(self):
        wait_cnt = self.in_waiting
        if wait_cnt == 0:
            time.sleep(self.TIMEOUT)
        return self.in_waiting>0

def main():
    ser = dl_com(uart_dev, baudrate=baud, timeout=80.0/baud)
    com = Datalink(ser, debug=False)
    while True:
        data=bytes("Hello world!", "ascii")
        ans=com.write(data)
        if ans:
            ans = com.read()
            print("received answer")
            if ans is not None and len(ans)>0:
                print(ans)


if __name__ == '__main__':
    main()

