#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Python code runnign on the host to test the communication stack.
    Created on 12.7.2016
    @author: Tobias Badertscher
"""
import serial
from micropython_lib.common.datalink import Datalink
import time

timeout =0.0018

class dl_com(serial.Serial):

    TIMEOUT = timeout

    def any(self):
        wait_cnt = self.in_waiting
        if wait_cnt == 0:
            time.sleep(self.TIMEOUT)
        return self.in_waiting>0

def get_datalink(dev_name):
    dev = dl_com(dev_name, timeout = timeout)
    dl = Datalink(dev)
    return dl


def test_echo(dev_name):
    dl = get_datalink(dev_name)
    for data_send in range(256):
        status = dl.write([data_send, ])
        if status is False:
            print("NACK on data %d" % (data_send))
            time.sleep(1)
        elif status is None:
            print("No receiver for data %d" % (data_send))
            time.sleep(1)
        data_recv = dl.read()
        if data_recv != data_send:
            if data_recv is None:
                print("Send 0x%02x, Nothing recevied" % (data_send,))
            else:
                rcv_str=", ".join(["0x%02x" % i for i in data_recv])
                print("Send 0x%02x, Recevied %s" % (data_send,  rcv_str))

def receiver(dev_name):
    dl = get_datalink(dev_name)
    while True:
        data = dl.read()
        if data is not None:
            data_str = ", ".join(["0x%02x" % i for i in data])
            print("Received %s" % data_str)

def sender(dev_name):
    dl = get_datalink(dev_name)
    value = 0
    while True:
        status = dl.write([value, ])
        value = (value + 1) % 256
        if status == None:
            time.sleep(1)
        elif status == True:
            print("ACK write of %d" % value)
        elif status == False:
            print("ACK write of %d" % value)
        else:
            raise ValueError("Unknown Status")


if __name__ == '__main__':
    test_echo('/dev/ttyACM0')
    #receiver('/dev/ttyACM0')
    #sender('/dev/ttyACM0')


