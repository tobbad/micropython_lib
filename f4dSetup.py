import pyb

def setupPins():
    i2cAddr = pyb.Pin('PA6', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
    i2cAddr.low()
    conf = pyb.Pin('PE3', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
    conf.high()
    audioReset = pyb.Pin(pyb.Pin.board.PD4, pyb.Pin.OUT_PP)
    audioReset.low()
    pyb.delay(100)
    audioReset.high()

 
