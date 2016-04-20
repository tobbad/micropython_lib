
import pyb
import math

led = []
for i in range(1,5):
    led.append(pyb.LED(i))

dac = pyb.DAC(1)

def volume(val=127):
    i2c = pyb.I2C(1, pyb.I2C.MASTER)
    i2c.mem_write(val, 46, 0)

def gen_sinus(size = 100):
    buf = bytearray(size)
    for i in range(len(buf)):
        buf[i] = 128 + int(127 * math.sin(2 * math.pi * i / size))
    return buf
    
def play(buf, freq=440):
    dac.write_timed(buf, freq * len(buf), mode=pyb.DAC.CIRCULAR)


    
    
 
