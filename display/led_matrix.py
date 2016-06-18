

from pyb import Pin, delay


class LED_MATRIX:
    
    DEBUG = True
    PORT2GPIO = [stm.GPIOA, stm.GPIOB, stm.GPIOC, stm.GPIOD, stm.GPIOE ]
    
    def __init__(self, width, height, red, green, blue, a, b, c, d, clk, latch, oe):
        self.__width = width
        self.__height = height
        self.__BYTES_PER_WEIGHT= 3*width*height>>3
        self.__BITPERCOLOR = 4
        self.__red = tuple(Pin(i, Pin.OUT_PP) for i in red)
        self.__green = tuple(Pin(i, Pin.OUT_PP) for i in green)
        self.__blue = tuple(Pin(i, Pin.OUT_PP) for i in blue)
        self.__color = list(Pin(i, Pin.OUT_PP) for i in red)
        self.__color.extend(list(Pin(i, Pin.OUT_PP) for i in green))
        self.__color.extend(list(Pin(i, Pin.OUT_PP) for i in blue))
        print(self.__color)
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
        self.__buffer = bytearray(self.__width*self.__height*2)
        self.__next_linenr = 0 
        self.__next_ln2weight = 1
        self.__set_hi = []
        self.__set_lo = []
        if self.DEBUG:
            print(self)
        
        
    def pixel(self, x, y, col = None):
        if (0 <= x < self.__width) and (0 <= y < self.__height):
            lower = y < 16
            if col is None:
                r, g, b = 0, 0, 0
                for ln2w in range(self.__BITPERCOLOR):
                    addr = ln2w*self.__BYTES_PER_WEIGHT+(y&0x0F)*(self.__width>>1)+x
                    if (addr & 0x03) != 0x03:
                        val = self.__buffer[addr]
                        print("Eval %s value at %d = 0x%02x weight %d" % ( "lower" if lower else "upper", addr, val, ln2w ))
                        if lower:
                            r += ((val   ) & 0x01)*(1<<ln2w)
                            g += ((val>>2) & 0x01)*(1<<ln2w)
                            b += ((val>>4) & 0x01)*(1<<ln2w)
                        else:     
                            r += ((val>>1) & 0x01)*(1<<ln2w)
                            g += ((val>>3) & 0x01)*(1<<ln2w)
                            b += ((val>>5) & 0x01)*(1<<ln2w)
                    else:
                        if lower:
                            r += ((self.__buffer[addr  ]>>6) & 0x01)*(1<<ln2w)
                            g += ((self.__buffer[addr+1]>>6) & 0x01)*(1<<ln2w)
                            b += ((self.__buffer[addr+2]>>6) & 0x01)*(1<<ln2w)
                        else:
                            r += ((self.__buffer[addr  ]>>7) & 0x01)*(1<<ln2w)
                            g += ((self.__buffer[addr+1]>>7) & 0x01)*(1<<ln2w)
                            b += ((self.__buffer[addr+2]>>7) & 0x01)*(1<<ln2w)
                return r, g, b
            else:
                # col[0] is red
                # col[1] is green
                # col[2] is blue
                for ln2w in range(self.__BITPERCOLOR):
                    addr = ln2w*self.__BYTES_PER_WEIGHT+(y & 0x0F)*(self.__width>>1)+x
                    if (addr & 0x03) != 0x03:
                        val = self.__buffer[addr]
                        if lower:
                            val &= 0xEA
                            val |= 0x01 if col[0] & (1<<ln2w) else 0x00
                            val |= 0x04 if col[1] & (1<<ln2w) else 0x00
                            val |= 0x10 if col[2] & (1<<ln2w) else 0x00
                        else:
                            val &= 0xD5
                            val |= 0x02 if col[0] & (1<<ln2w) else 0x00
                            val |= 0x08 if col[1] & (1<<ln2w) else 0x00
                            val |= 0x20 if col[2] & (1<<ln2w) else 0x00
                        print("Set regular buffer@ %d to 0x%02x" % (addr, val))
                        self.__buffer[addr] = val
                    else:
                        mask = 0x80 if lower else 0x40
                        for i in range(3):
                            self.__buffer[addr+i] &= ~mask
                        self.__buffer[addr]   |= mask if col[0] & (1<<ln2w) else 0x00
                        self.__buffer[addr+1] |= mask if col[1] & (1<<ln2w) else 0x00
                        self.__buffer[addr+2] |= mask if col[1] & (1<<ln2w) else 0x00
                        print("Set iregular buffer@ %d, %d %d to 0x%02x 0x%02x 0x%02x" % (addr, addr+1, addr+2, self.__buffer[addr], self.__buffer[addr+1], self.__buffer[addr+2]))
        else:
            raise Exception("Pixel (%d, %d) is not on canevas" % (x, y))
        
        
    def select_line(self, line_number):
        if line_number & 0x01:
            self.__a.high()
        else:
            self.__a.low()
        if line_number & 0x02:
            self.__b.high()
        else:
            self.__b.low()
        if line_number & 0x04:
            self.__c.high()
        else:
            self.__c.low()
        if self.__d is not None:
            if line_number & 0x08:
                self.__d.high()
            else:
                self.__d.low()

    def set_rgb_pin(self, val, pin):
        if (val & 0x01):
            pin.high()
        else:
            pin.low()
        return val>>1

    def set_data(self, ln2w, line_nr):
        val0 = line_nr<<28
        val1 = line_nr<<24
        if line_nr !=42:
            r0, r1, g0, g1, b0, b1 = val0, val1, val0,  val1, val0, val1
        else:
            r0, r1, g0, g1, b0, b1 = 0 ,0 ,0, 0 ,0 ,0
        for i in range(self.__width):
            r0 = self.set_rgb_pin(r0, self.__red[0])
            r1 = self.set_rgb_pin(r1, self.__red[1])
            g0 = self.set_rgb_pin(g0, self.__green[0])
            g1 = self.set_rgb_pin(g1, self.__green[1])
            b0 = self.set_rgb_pin(b0, self.__blue[0])
            b1 = self.set_rgb_pin(b1, self.__blue[1])
            self.__clk.high()
            self.__clk.low()

    #@micropython.viper
    def set_data_f(self, ln2w, line_nr):
        offset = ln2w*self.__BYTES_PER_WEIGHT+(line_nr & 0x0F)*(self.__width>>1)
        val_11=0
        idx = 0
        for x in range(self.__width):
            s_idx = x & 0x03
            ser_val = 0
            if s_idx == 3:
                ser_val = val_11
                val_11 =0
            else:
                ser_val = self.__buffer[offset+idx]
                val_11 |= (ser_val>>(6-2*s_idx))
                idx+=1
            for pin_nr in range(len(self.__color)):
                pin = self.__color[pin_nr]
                mask = 1<<pin_nr
                if ser_val & mask:
                    #self.__set_hi[pin.port] = 1 << pin.pin
                    pin.high()
                else:
                    #self.__set_lo[pin.port] = 1 << pin.pin
                    pin.low()
            self.__clk.high()
            self.__clk.low()

    def update(self):
        #print("Show line %d, weight %d" % (self.__next_linenr, self.__next_ln2weight))
        self.__oe.high() # disable led driver output
        self.__latch.high() # latch data of last call to output
        # Select group
        self.select_line(self.__next_linenr)
        # Set output enable for last data
        self.__oe.low()
        self.__latch.low()
        # Select next group
        self.__next_linenr = (self.__next_linenr + 1)
        if self.__next_linenr == self.__cycle_max:
            self.__next_linenr = 0
            self.__next_ln2weight = (self.__next_ln2weight+1)%self.__BITPERCOLOR
        # Set data for next group
        self.set_data_f(self.__next_ln2weight, self.__next_linenr)

    def show(self, single=False):
        cnt = 0
        while True:
            self.update()
            cnt+=1
            if single and cnt>self.__height:
                break


    def test(self):
        col = (15,0,0)
        clear = (0,0,0)
        for x in range(self.__width):
            for y in range(self.__height):
                print(x,y)
                self.pixel(x,y, col)
                self.show(True)
                self.pixel(x,y, clear)
                

    def non_zero(self):
        res = []
        for x in range(self.__width):
            for y in range(self.__height):
                val = self.pixel(x,y)
                if any(val):
                    res.append("Pixel at (%d, %d) = (%d, %d, %d)" % (x,y,val[0],val[1], val[2]))
        return "\n".join(res)

        
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
        res.append("line sel: %d " % self.__next_linenr)
        return "\n".join(res)
        
