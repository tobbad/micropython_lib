# main.py -- put your code here!

import pyb

led = pyb.LED(1)
#uart = pyb.UART(2, 9600)
rtc = pyb.RTC()
rtc.init()

i2c_mfx = pyb.I2C(config['mfx']['i2c_bus'], pyb.I2C.MASTER, baudrate=100000)
wake_up_mfx = pyb.Pin(config['mfx']['wakeUp_pin'], pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
irq_mfx = pyb.Pin(config['mfx']['irq_pin'], pyb.Pin.IN, pyb.Pin.PULL_DOWN)
conf = IDD_DEFAULT()
mfx = MFX(i2c_mfx, config['mfx']['i2c_addr'], wake_up_mfx, conf, irq_mfx)

idx=0
while True:
    led.toggle()
    data = None #uart.read(10)
    Y,M,D,wd,h,m,s,ms = rtc.datetime()
    dstr="Time: %d.%d.%d %02d:%02d:%02d\n\r" % (D,M,Y,h,m,s)
    #uart.write(dstr)
    print(dstr[0:-2])
    pyb.delay(500)
    if data is not None:
        print("%4d %s" % (idx, str(data)))
        idx+=1
    
