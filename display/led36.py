#
# MicroPython module to control the led36 tile of pybd
#
# Credit goes to MicroPython website and marfis:
# https://forum.micropython.org/viewtopic.php?t=6272
#
import time, machine

LED_BROADCAST = 1       # broadcast I2C address
LED_ADDR = 60           # default individual LED36 address


class led36:
    
    def __init__(self, addr=LED_ADDR):
        self._addr = addr
        self._i2c = machine.I2C('X')  # select X bus
        self._i2c.writeto(LED_ADDR, b'\x01') # initialise all LED36 tiles with broadcast address

    def _doTransfer(self, data, addr=None):
        if addr is None:
            self._i2c.writeto(self._addr, data)
        else:
            self._i2c.writeto(addr, data)

    def cyc(self, dt=250):
        """ Set all LEDs to black, red, green, yellow, blue, magenta, cayn and white for dt ms
            ramp up brightnes from 0 % to 100 %
        """
        while True:
            try:
                self.fill_rgb(100, 100, 100)
                break
            except:
                time.sleep_ms(100)
        for i in range(8):
            self.fill_rgb((i & 1) * 255, ((i >> 1) & 1) * 255, ((i >> 2) & 1) * 255)
            time.sleep_ms(dt)
        for i in range(100):
            self.brightness(i)
            time.sleep_ms(20)

    def brightness(self, b=100):
        """ Set brigntness """
        ba = bytearray(b'\x02\x16 ')
        ba[-1] = b & 0xff
        self._doTransfer(ba)

    def bloop(self, dt=100, maxv=100, inc=1):
        """ Cycle through brigntness ramp """
        b = 0
        while True:
            print(b)
            self.brightness(b)
            b += inc
            b %= maxv
            time.sleep_ms(dt)

    def pump(self, dt=10, maxv=100):
        """ Cycle through brightness modulation """
        import math
        sinar = []
        for i in range(90):
            sinar.append(int((math.sin(i * 4 / 180 * math.pi) + 1) * maxv / 2))
        i = 0
        while True:
            self.brightness(sinar[i])
            i += 1
            i %= len(sinar)
            time.sleep_ms(dt)

    def fill_rgb(self, r, g, b):
        """ Fill LED array using set pixel command """
        self._doTransfer(b'\x02X\x00\x00')
        buf = bytearray(b'\x02A   ')
        buf[2] = r
        buf[3] = g
        buf[4] = b
        for i in range(36):
            self._doTransfer(buf)

    def illu(self, r, g, b):
        """ Fill LED array using set illumination command """
        buf = bytearray(b'\x02i   ')
        buf[2] = r
        buf[3] = g
        buf[4] = b
        self._doTransfer(buf)

    def fill_frame(self, r, g, b):
        """ Fill LED array using fill frame command """
        self._doTransfer(b'\x02ml')
        buf = bytearray(b'   ')
        buf[0] = r
        buf[1] = g
        buf[2] = b
        for i in range(36):
            self._doTransfer(buf)

    def set_dot(self, x, y, r, g, b):
        """ Set single LED color at position """
        buf = bytearray(b'\x02X  ')
        buf[2] = x
        buf[3] = y
        self._doTransfer(buf)
        buf = bytearray(b'\x02A   ')
        buf[2] = r
        buf[3] = g
        buf[4] = b
        self._doTransfer(buf)

    def fill_raw(self, r, g, b):
        """ Fill LED array with raw values using fill frame command """
        self._doTransfer(b'\x02nl')
        buf = bytearray(b'   ')
        buf[0] = r
        buf[1] = g
        buf[2] = b
        for i in range(36):
            self._doTransfer(buf)

    def led_pins(self, v):
        """ Permute LED colors (use with care) """
        buf = bytearray(b'\x02\x1c\x00')
        buf[-1] = v & 3
        self._doTransfer(buf)

    def random_dots(self, dt=10):
        """ Set random colors at random positions """
        import pyb
        while True:
            rn = pyb.rng()
            r = rn & 0xff
            g = (rn >> 8) & 0xff
            b = (rn >> 16) & 0xff
            x = (rn >> 24) % 36
            y = x // 6
            x %= 6
            self.set_dot(x, y, r, g, b)
            time.sleep_ms(dt)
            
    def set_text_color(self, r,g,b,rb,gb,bb):
        ba = bytearray(b'\x02c      ')
        ba[-6] = b
        ba[-5] = g
        ba[-4] = r
        ba[-3] = bb
        ba[-2] = gb
        ba[-1] = rb    
        self._doTransfer(ba)

    def set_rot(self, angle):
        ba = bytearray(b'\x02\x14 ')
        ba[-1] = angle
        self._doTransfer(ba)

    def text(self, data, col_cycle=False):
        pre_cyc=b'\x02k '
        pre_else=b'\x02l '
        pre = pre_cyc if col_cycle else pre_else
        offset = len(pre) + 1
        ba=bytearray(offset + len(data))
        idx = 0
        ba[0:len(pre)] = pre
        ba[len(pre)] = len(data) & 0xff
        for idx, i in enumerate(data):
            ba[offset+idx] = ord(i)
        self._doTransfer(ba, addr=1)

    def show(self, delay=50):
        while True:
            self._doTransfer(b'\x01')
            time.sleep_ms(delay)
