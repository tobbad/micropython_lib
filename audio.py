

import math
import pyb
import math


def volume(val=127):
    i2c = pyb.I2C(1, pyb.I2C.MASTER)
    i2c.mem_write(val, 46, 0)


def playSine(freq=440):
    # create a buffer containing a sine-wave
    buf = bytearray(100)
    for i in range(len(buf)):
        buf[i] = 128 + int(127 * math.sin(2 * math.pi * i / len(buf)))

    # output the sine-wave at freq Hz
    print(pyb.DAC)
    dac = pyb.DAC(1)
    print(type(dac))
    dac.write_timed(buf, freq * len(buf), mode=pyb.DAC.CIRCULAR)


def play():
    volume(127)
    playSine()

buf = bytearray(100)
for i in range(len(buf)):
    buf[i] = 128 + int(127 * math.sin(2 * math.pi * i / len(buf)))

freq = 440
dac = pyb.DAC(1)
dac.write_timed(buf, freq * len(buf), mode=pyb.DAC.CIRCULAR)
