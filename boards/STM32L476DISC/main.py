
import pyb
from l3gd20 import L3GD20
from lsm303c import LSM303C
from mfx import MFX
from board import config, IDD_DEFAULT

rp = pyb.Pin('PE3', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
rp.high()
i2c = pyb.I2C(1, pyb.I2C.MASTER, baudrate=100000)

spi = pyb.SPI(2, pyb.SPI.MASTER, baudrate=600000, polarity=1, phase=1)
cs_gyro = pyb.Pin('PD7', pyb.Pin.OUT_PP)
gyro = L3GD20(spi, cs_gyro)
# gyro.DEBUG = False
print("Gyro = (%7.2f %7.2f, %7.2f)" % gyro.xyz())
print("Temperature = %.1f C" % gyro.temperature())

if 1 == 0:
    cs_accel = pyb.Pin('PE0', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
    cs_mag = pyb.Pin('PC0', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
    mems = LSM303C(spi, cs_mag, cs_accel)
    mems.bidi_mode()
    mems.exists()
    print("Accel = (%6.4f, %6.4f, %6.4f)" % mems.accel.xyz())
    print("Mag   = (%6.4f, %6.4f, %6.4f)" % (mems.mag.xyz()))

i2c_mfx = pyb.I2C(config['mfx']['i2c_bus'], pyb.I2C.MASTER, baudrate=100000)
wake_up_mfx = pyb.Pin(config['mfx']['wakeUp_pin'], pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
irq_mfx = pyb.Pin(config['mfx']['irq_pin'], pyb.Pin.IN, pyb.Pin.PULL_DOWN)
conf = IDD_DEFAULT()
mfx = MFX(i2c_mfx, config['mfx']['i2c_addr'], wake_up_mfx, conf, irq_mfx)