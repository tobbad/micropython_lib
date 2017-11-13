# main.py -- put your code here!

import pyb

led = pyb.LED(1)
uart = pyb.UART(2, 9600)
rtc = pyb.RTC()

idx=0
while True:
    led.toggle()
    data = uart.read(10)
    Y,M,D,wd,h,m,s,ms = rtc.datetime()
    dstr="Time: %d.%d.%d %02d:%02d:%02d\n\r" % (D,M,Y,h,m,s)
    uart.write(dstr)
    print(dstr[0:-2])
    if data is not None:
        print("%4d %s" % (idx, str(data)))
        idx+=1
    
