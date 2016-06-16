

from pyb import Pin, delay


class LED_MATRIX:
    
    DEBUG = True
    
    def __init__(self, columns, rows, red, green, blue, a, b, c, d, clk, latch, oe):
        self.__col = columns
        self.__row = rows
        self.__red = tuple(Pin(i, Pin.OUT_PP) for i in red)
        self.__green = tuple(Pin(i, Pin.OUT_PP) for i in green)
        self.__blue = tuple(Pin(i, Pin.OUT_PP) for i in blue)
        self.__a = Pin(a, Pin.OUT_PP)
        self.__b = Pin(b, Pin.OUT_PP)
        self.__c = Pin(c, Pin.OUT_PP)
        self.__d = None
        self.__cycle_max = 8
        if d is not None:
            self.__d = Pin(d, Pin.OUT_PP)
            self.__cycle_max = 16
        self.__clk = Pin(clk, Pin.OUT_PP)
        self.__latch = Pin(latch, Pin.OUT_PP)
        self.__oe = Pin(oe, Pin.OUT_PP)
        self.__buffer = bytearray(self.__col*self.__row*2)
        self.__grpsel = 0 # cycles 
        if self.DEBUG:
            print(self)
        
        
    def pixel(self, x, y, col = None):
        if 0 <= x <= self.__col and 0 <= y <= self.__row:
            addr = x*y*2
            if col is None:
                r = self.__buffer[addr+1] & 0x0F
                g = (self.__buffer[addr]>>4) & 0x0F
                b = self.__buffer[addr] & 0x0F
                return r, g, b
            else:
                # col[0] is red
                # col[1] is green
                # col[2] is blue
                self.__buffer[addr] =  ((col[1] & 0x0F)<<4) | col[2] & 0x0F
                self.__buffer[addr+1] =  col[0] & 0x0F
        else:
            raise Exception("Pixel (%d, %d) not on canevas" % (x, y))
        
        
    def select_row(self, rowsel):
        if rowsel & 0x01:
            self.__a.high()
        else:
            self.__a.low()
        if rowsel & 0x02:
            self.__b.high()
        else:
            self.__b.low()
        if rowsel & 0x04:
            self.__c.high()
        else:
            self.__c.low()
        if self.__d is not None:
            if rowsel & 0x08:
                self.__d.high()
            else:
                self.__d.low()

    def set_rgb_pin(self, val, pin):
        if (val & 0x01):
            pin.high()
        else:
            pin.low()
        return val>>1

    def set_data(self, grp):
        val0 = grp<<28
        val1 = grp<<24
        if grp !=42:
            r0, r1, g0, g1, b0, b1 = val0, val1, val0,  val1, val0, val1
        else:
            r0, r1, g0, g1, b0, b1 = 0 ,0 ,0, 0 ,0 ,0
        for i in range(32):
            r0 = self.set_rgb_pin(r0, self.__red[0])
            r1 = self.set_rgb_pin(r1, self.__red[1])
            g0 = self.set_rgb_pin(g0, self.__green[0])
            g1 = self.set_rgb_pin(g1, self.__green[1])
            b0 = self.set_rgb_pin(b0, self.__blue[0])
            b1 = self.set_rgb_pin(b1, self.__blue[1])
            self.__clk.high()
            self.__clk.low()

    def update(self):
        self.__oe.high() # disable led driver output
        self.__latch.high() # latch data of last call to output
        # Select group
        self.select_row(self.__grpsel)
        # Set output enable for last data
        self.__oe.low()
        self.__latch.low()
        # Select next group
        self.__grpsel = (self.__grpsel + 1) % self.__cycle_max
        # Set data for next group
        self.set_data(self.__grpsel)
        
    def __str__(self):
        res = []
        res.append("Set up led matrix with:")
        res.append("red  : %s %s" % (self.__red[0], self.__red[1]))
        res.append("green: %s %s" % (self.__green[0], self.__green[1]))
        res.append("blue : %s %s" % (self.__blue[0], self.__blue[1]))
        res.append("clk  : %s" % self.__clk)
        res.append("latch: %s" % self.__latch)
        res.append("oe   : %s" % self.__oe)
        res.append("a, b, c, d = %s %s %s %s" % (self.__a, self.__b, self.__c, self.__d))
        res.append("grp sel: %d " % self.__grpsel)
        return "\n".join(res)
        
