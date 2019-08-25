 
from led36 import led36
import pyb
import time 

pon = pyb.Pin("EN_3V3")
pon.on()
time.sleep_ms(20)

tile = led36()
tile.brightness()
tile.text('Micropython is sooo cool..', col_cycle=True)
tile.show()

#led36.random_dots(led36.LED_ADDR)
