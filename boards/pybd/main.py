 
from led36 import led36
from sensa import OPT3001
import pyb
import time 
import machine

pon = pyb.Pin("EN_3V3")
pon.on()
time.sleep_ms(20)

tile = led36()
pyb.Pin('PULL_SCL', pyb.Pin.OUT, value=1) # enable 5.6kOhm X9/SCL pull-up
pyb.Pin('PULL_SDA', pyb.Pin.OUT, value=1) # enable 5.6kOhm X10/SDA pull-up
i2cx=machine.I2C('X')
i2cy=machine.I2C('Y')
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
