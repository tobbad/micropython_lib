 
from led36 import led36
from sensa import OPT3001
import pyb
import time 
import machine

pon = pyb.Pin("EN_3V3")
pon.on()
time.sleep_ms(20)

tile = led36()
sense = OPT3001(machine.I2C('X'))
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
