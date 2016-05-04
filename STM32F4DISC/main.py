#
# Main file for STM32F4DISCOVERY
#
import pyb
from staccel import STAccel
acc = STAccel()

def setupPins():
    i2cAddr = pyb.Pin('PA6', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
    i2cAddr.low()
    conf = pyb.Pin('PE3', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
    conf.high()
    audioReset = pyb.Pin(pyb.Pin.board.PD4, pyb.Pin.OUT_PP)
    audioReset.low()
    pyb.delay(100)
    audioReset.high()

def run():
    while True:
        print("%5.2g %5.2f %5.2f" % (acc.x(), acc.y(), acc.z()))
        pyb.delay(100)


from  CS43L22 import CS43L22
snd = CS43L22()
