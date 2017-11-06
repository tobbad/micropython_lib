# main.py -- put your code here!

import pyb

led = pyb.LED(1)
uart = pyb.UART(1, 28800)

idx=0
while True:
    led.toggle()
    data = uart.read(10)
    if data is not None:
        print("%4d %s" % (idx, str(data)))
    idx+=1
    
