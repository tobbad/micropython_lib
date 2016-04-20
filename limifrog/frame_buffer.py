#
#
#
class Frame_Buffer():

    FB_SIZE = (16,)

    def __init__(self, xsize, ysize, pixel_size):
        if not pixel_size in self.FB_SIZE:
            raise Exception("Pixelsize %d not supported" % (pixel_size))
        self.__buffer = bytearray(xsize*ysize*pixel_size)
        self.__color = 0x0000
        self.__x_size = xsize
        self.__y_size = ysize
        self.__pixel_size = pixel_size
        if self.__pixel_size == 16:
            self.__fill = self.__fill_16
        self.__x_mirror = False
        self.__y_mirror = False

    @micropython.viper
    def __fill_16(self, color: int, byte_cnt: int):
        bPtr = ptr16(self.__buffer)
        for i in range(byte_cnt>>1):
            bPtr[i] = color

    def trim_region(self, xmin, ymin, xmax, ymax):
        xmin = min(xmin, self.XSIZE-1)
        xmin = max(xmin, 0)
        xmax = min(xmax, self.XSIZE-1)
        xmax = max(xmax, 0)
        ymin = min(ymin, self.YSIZE-1)
        ymin = max(ymin, 0)
        ymax = min(ymax, self.YSIZE-1)
        ymax = max(ymax, 0)
        if (ymin>ymax):
            ymin, ymax = ymax, ymin
        if (xmin>xmax):
            xmin, xmax = xmax, xmin
        return xmin, ymin, xmax, ymax

    def box(self, xmin, ymin, xmax, ymax, color):
        size = self.set_region(xmin, xmax, ymin, ymax)
        self.__mem_fill(color, size)

