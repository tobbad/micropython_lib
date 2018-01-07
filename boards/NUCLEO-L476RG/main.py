
import pyb
from board import config

led = pyb.LED(1)
btn = pyb.Pin(config['switch']['pin'], mode = config['switch']['mode'], pull = config['switch']['pull'])

