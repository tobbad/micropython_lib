 
from led36 import led36
from sensa import OPT3001
import pyb
import time 
import machine
from lps22hx import LPS22HH
from lsm9ds1 import LSM9DS1

config = {
    'lps22hh': {'i2c_bus': 2, 'i2c_addr': 0x5C},
    'lsm9ds1_accgyr': {'i2c_bus': 2, 'i2c_addr': 0x6A},
    'lsm9ds1_mag': {'i2c_bus': 2, 'i2c_addr': 0x1C},
    'extPower': {'enable': "EN_3V3"},
}

sel = 0

pon = pyb.Pin(config['extPower']['enable'])
pon.on()
time.sleep_ms(20)

tile = led36()
pyb.Pin('PULL_SCL', pyb.Pin.OUT, value=1) # enable 5.6kOhm X9/SCL pull-up
pyb.Pin('PULL_SDA', pyb.Pin.OUT, value=1) # enable 5.6kOhm X10/SDA pull-up
i2cx=machine.I2C('X')
i2cy = pyb.I2C(config['lps22hh']['i2c_bus'], pyb.I2C.MASTER, baudrate=100000)
lps22 = LPS22HH(i2cy, config['lps22hh']['i2c_addr'])
lsm9d1 = LSM9DS1(i2cy, config['lsm9ds1_accgyr']['i2c_addr'], config['lsm9ds1_accgyr']['i2c_addr'], config['lsm9ds1_mag']['i2c_addr'])
tile.brightness(100)
tile.fill_rgb(255,255,255)

if 0 == sel:
    while True:
        p=lps22.value()
        h=lps22.height()
        T1=lps22.temperature()
        acc = " acc = (" +(", ".join(["%+6.3f"%i for i in lsm9d1.accel.xyz()])) + ") g" 
        gyr = " gyr = (" +(", ".join(["%+6.3f"%i for i in lsm9d1.gyro.xyz()])) + ") dps" 
        mag = " mag = (" +(", ".join(["%+6.3f"%i for i in lsm9d1.mag.xyz()])) + ") G" 
        print("p = %5.3e %s, h = %.1f m, T1 = %.1f C, %s, %s, %s" %  (p, lps22.unit(), h, T1, acc, mag, gyr))
else:
    sense = OPT3001(i2cx)
    tile.brightness(100)
    tile.fill_rgb(255,255,255)
    while True:
        sense.measure()
        while not sense.is_ready():
            machine.idle()
        tile.brightness(int(sense.lux()/10))
        print(sense.lux())
#tile.text('Micropython is sooo cool..', col_cycle=True)
#tile.show()

#led36.random_dots(led36.LED_ADDR)
