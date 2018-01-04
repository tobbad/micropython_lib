#
#
#
import pyb
import struct


class COM():

    debug = False

    def __init__(self, spi, cs, rs):
        self.__spi = spi
        self.__cs = cs
        self.__rs = rs

    def __data_start(self):
        self.__cs.value(0)
        self.__rs.value(0)
        self.__spi.send(0x22)
        self.__rs.value(1)
        # Switch to 16 bit transfer ?

    def __data_end(self):
        # Switch back to 8 bit transfer ?
        self.__cs.value(1)

    def write_reg(self, addr, value):
        self.__cs.value(0)
        self.__rs.value(0)
        self.__spi.send(addr)
        self.__rs.value(1)
        self.__cs.value(1)
        self.__cs.value(0)
        self.__spi.send(value)
        self.__cs.value(1)

    def send_cmd(self, cmd):
        self.__rs.value(0)
        self.__cs.value(0)
        self.__spi.send(cmd)
        self.__cs.value(1)
        self.__rs.value(1)

    def send_data(self, data):
        self.__data_start()
        self.__spi.send(data)
        self.__data_end()


class SEPS525():

    # Copy modify paste from LBF_OLED_Init default configuration which is
    # taken from DD-160128FC-1A.pdf
    CONF = ((0x06, 0x00), (0x02, 0x01), (0x80, 0x00),
            (0x03, 0x30),
            # Driving current R G B - default R = 82uA / G = 56uA / B = 58uA
            (0x10, 0x52), (0x11, 0x38), (0x12, 0x3A),
            # Precharge time RGB
            (0x08, 0x01), (0x09, 0x01), (0x0A, 0x01),
            # Precharge current R G B
            (0x0B, 0x0A), (0x0C, 0x0A), (0x0D, 0x0A),
            #    * Display mode set :
            #     *  - RGB
            #     *  - Column = 0->159
            #     *  - Column data display = Normal display
            #     *
            (0x13, 0x00),
            # External interface mode=MPU
            (0x14, 0x31),     # 0x01 ?
            #   * Memory write mode :
            #     *  - 8 bits dual transfer
            #     *  - 65K support
            #     *  - Horizontal address counter is increased
            #     *  - Vertical address counter is increased
            #     *  - The data is continuously written horizontally
            #     *
            (0x16, 0x66),
            # Duty = 128
            (0x28, 0x7F),
            # Display start on line 0
            (0x29, 0x00),
            # DDRAM read address start point 0x2E~0x2F
            (0x2E, 0x00),     # X
            (0x2F, 0x00),     # Y
            # Display screen saver size 0x33~0x36
            (0x33, 0x00),     # Screen saver columns start
            (0x34, 0x9F),     # Screen saver columns end
            (0x35, 0x00),     # Screen saver row start
            (0x36, 0x7F))     # Screen saver row end

    def __init__(self, spi, cs, rs):
        self.__buffer = bytearray(self.XSIZE*self.YSIZE*2)
        self.__com = COM(spi, cs, rs)
        self.__com.write_reg(0x04, 0x01)
        pyb.delay(10)
        self.__com.write_reg(0x04, 0x00)
        pyb.delay(10)
        for adr, val in self.CONF:
            self.__com.write_reg(adr, val)
        self.__color = 0x0000

    def set_region(self, xmin, xmax, ymin, ymax):
        xmin = min(xmin, self.XSIZE-1)
        xmin = max(xmin, 0)
        xmax = min(xmax, self.XSIZE-1)
        xmax = max(xmax, 0)
        ymin = min(ymin, self.YSIZE-1)
        ymin = max(ymin, 0)
        ymax = min(ymax, self.YSIZE-1)
        ymax = max(ymax, 0)
        if (ymin > ymax):
            ymin, ymax = ymax, ymin
        if (xmin > xmax):
            xmin, xmax = xmax, xmin
        self.__com.write_reg(0x17, xmin)   # X start
        self.__com.write_reg(0x18, xmax)   # X end
        self.__com.write_reg(0x19, ymin)   # Y start
        self.__com.write_reg(0x1A, ymax)   # Y end
        self.__com.write_reg(0x20, xmin)   # memory accesspointer x
        self.__com.write_reg(0x21, ymin)   # memory accesspointer y
        return (xmax-xmin+1)*(ymax-ymin+1)*2  # a pixel color is 16 bit

    @micropython.viper
    def __mem_fill(self, color: int, byte_cnt: int):
        bPtr = ptr16(self.__buffer)
        for i in range(byte_cnt >> 1):
            bPtr[i] = color

    @micropython.viper
    def __circle(self, x0: int, y0: int, r: int):
        # adapted from https://github.com/elfnor/\
        # micropython-blog-examples/blob/master/oled/lcd_gfx.py
        color = int(self.__color)
        drawSize = r*r
        screenSize = int(self.XSIZE*self.YSIZE)
        size = drawSize if drawSize < screenSize else screenSize
        self.__mem_fill(color, size)
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r
        while x < y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f += ddF_y
            x += 1
            ddF_x += 2
            f += ddF_x
            self.box(x0-x, y0-y, x0+x, y0-y, color)
            self.box(x0-x, y0+y+1, x0+x, y0+y+1, color)
            self.box(x0+y, y0-x, x0+y, y0+x+1, color)
            self.box(x0-y, y0-x, x0-y, y0+x+1, color)
        self.box(x0-x, y0-y, x0+x, y0+y+1, color)

    def box(self, xmin, ymin, xmax, ymax, color):
        size = self.set_region(xmin, xmax, ymin, ymax)
        self.__mem_fill(color, size)
        data = memoryview(self.__buffer)
        self.__com.send_data(data[0:size])

    def pixel(self, x, y, color):
        if not (0 <= x < self.XSIZE):
            return
        if not (0 <= y < self.YSIZE):
            return
        self.box(x, y, x+1, y+1, color)

    def line(self, x0, y0, x1, y1, color):
        # copy from https://github.com/elfnor/ \
        # micropython-blog-examples/blob/master/oled/lcd_gfx.py
        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dx = x1-x0
        dy = abs(y1-y0)
        err = dx/2
        ystep = -1
        if y0 < y1:
            ystep = 1
        for xx in range(x0, x1):
            if steep:
                self.pixel(y0, xx, color)
            else:
                self.pixel(xx, y0, color)
            err -= dy
            if err < 0:
                y0 += ystep
                err += dx

    def circle(self, x0, y0, r, color):
        self.__color = color
        self.__circle(x0, y0, r)

    def clear(self):
        self.box(0, 0, self.XSIZE, self.YSIZE, 0)
