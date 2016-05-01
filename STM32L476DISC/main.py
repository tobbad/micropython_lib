
import pyb
import L3GD20
from lsm303ctr import LSM303CTR

rp = pyb.Pin('PE3', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
rp.high()
i2c = pyb.I2C(1, pyb.I2C.MASTER, baudrate=100000)

spi = pyb.SPI(2, pyb.SPI.MASTER, baudrate=600000, polarity = 1, phase = 1)
cs_gyro = pyb.Pin('PD7', pyb.Pin.OUT_PP)
gyro = L3GD20.L3GD20(spi, cs_gyro)
print(gyro.omega_xyz())
print(gyro.temperature())
gyro.write_u8(L3GD20.L3GD20_CTRL_REG4_ADDR, L3GD20.L3GD20_CTRL_REG4_VAL_ALT)
print(gyro.omega_xyz())

spi = pyb.SPI(2, pyb.SPI.MASTER, baudrate=600000, polarity = 1, phase = 1, direction=pyb.SPI.DIRECTION_1LINE)
cs_accel = pyb.Pin('PE0', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
cs_mag = pyb.Pin('PC0', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
mems = LSM303CTR(spi, cs_mag, cs_accel)
