rp = pyb.Pin('PE3', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
rp.high()
i2c = pyb.I2C(1, pyb.I2C.MASTER, baudrate=100000)

i2c.scan()
i2c.mem_read(1, 74, 0x01)
