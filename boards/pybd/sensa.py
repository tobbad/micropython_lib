



class led:
     def __init__(self, i2c, addr=64):
         self._r = Signal('X2', Pin.OUT, value=0, invert=True)
         self._g = Signal('X3', Pin.OUT, value=0, invert=True)
         self._b = Signal('X4', Pin.OUT, value=0, invert=True)
         
     def set(self, r, g, b):
         self._r.on() if r else self._r.off()
         self._g.on() if g else self._g.off()
         self._b.on() if b else self._b.off()
 
class HDC2080:
    def __init__(self, i2c, addr=64):
        self.i2c = i2c
        self.addr = addr

    def is_ready(self):
        return self.i2c.readfrom_mem(self.addr, 0x0f, 1)[0] & 1 == 0

    def measure(self):
        self.i2c.writeto_mem(self.addr, 0x0f, b'\x01')

    def temperature(self):
        data = self.i2c.readfrom_mem(self.addr, 0x00, 2)
        data = data[0] | data[1] << 8
        return data / 0x10000 * 165 - 40

    def humidity(self):
        data = self.i2c.readfrom_mem(self.addr, 0x02, 2)
        data = data[0] | data[1] << 8
        return data / 0x10000 * 100

class OPT3001:
    def __init__(self, i2c, addr=69):
        self.i2c = i2c
        self.addr = addr

    def is_ready(self):
        return bool(self.i2c.readfrom_mem(self.addr, 0x01, 2)[1] & 0x80)

    def measure(self):
        self.i2c.writeto_mem(self.addr, 0x01, b'\xca\x10')

    def lux(self):
        data = self.i2c.readfrom_mem(self.addr, 0, 2)
        return 0.01 * 2 ** (data[0] >> 4) * ((data[0] & 0x0f) << 8 | data[1])

