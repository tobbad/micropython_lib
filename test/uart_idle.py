#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Test the UART reaction on a TX transfer to test
    the proper working of UART_TX_IDLE_IRQ
    Created on 2.6.2018
    @author: Tobias Badertscher

"""

import micropython

class UART_IDLE:
    
    USE_HARD = False
    READY="Ready\r\n"
    
    def __init__(self, uart):
        self._uart = uart
        self._uart.write("Hi there\n\r")
        self._buffer = bytearray(64)
        self._answer_irq = b"Irq \r\n"
        self._answer = b"Normal \r\n"
        self._normal_context_ref = self.normal_context
        
    def set_up_cb(self):
        flags = self._uart.IRQ_RX_IDLE
        if UART_IDLE.USE_HARD:
            self._uart.irq(self.irq_idle_callback, flags, UART_IDLE.USE_HARD)
        else:
            self._uart.irq(self.normal_context, flags, UART_IDLE.USE_HARD)
        
    def irq_idle_callback(self, other):
        self._uart.write(self._answer_irq)
        micropython.schedule(self._normal_context_ref, 0)
    
    def normal_context(self, value):
        cnt=self._uart.readinto(self._buffer)
        self._uart.write(self._answer)
        data = "".join([chr(i) if 32<=i<128 else "."  for i in self._buffer[:cnt] ])
        print("Get UART data in normal context: %s" % data)
        self._uart.write("Received: \"%s\"\r\n" % data)
    
