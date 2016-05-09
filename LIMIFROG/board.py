#
#
#
import pyb
from seps525 import SEPS525

sys_config={
    'lis3mdl':{'i2c_bus':2, 'i2c_addr':0x1C},
    'lps25h':{'i2c_bus':2, 'i2c_addr':0x5C},
    'lsm6ds3':{'i2c_bus':2, 'i2c_addr': 0x6A},
    'vl6180x':{'i2c_bus':2, 'i2c_addr': 0x29},
    'cs43l22':{'i2c_bus':1, 'i2c_addr': 0x4A, 'resetPin':'D4'},
    'oled':{'spi_bus':1, 'spi_cs': 'C5', 'rs':'C4', 'reset':'B1'},
    'buck':{'enable':'B6'},
    'ldo':{'enable':'C2'},
    'high_current':{'enable':'D2'},
    'vddh':{'enable':'C0'},
}


class board():

    def __init__(self):
        self.__buck = pyb.Pin('B6', pyb.Pin.OUT_PP)
        self.__buck.high()
        self.__ldo = pyb.Pin('C2', pyb.Pin.OUT_PP)
        self.__ldo.low()
        self.__high_current = pyb.Pin('D2', pyb.Pin.OUT_PP)
        self.__high_current.high()
        self.__vddh =  pyb.Pin('C0', pyb.Pin.OUT_PP)
        self.__vddh.low()
        self.__lcd_state = False

    def __set_get(self, pin, newState):
        if newState == None:
            return pin.value()
        elif newState == True:
            pin.high()
        else:
            pin.low()

    def __repr__(self):
        res = ("Limifrog board:",)
        res = res + ("vddh: %s" % ("ON" if self.vddh() else "OFF"),)
        res = res + ("buck: %s" % ("ON" if self.buck() else "OFF"),)
        res = res + ("ldo : %s" % ("ON" if self.ldo() else "OFF"),)
        res = res + ("lcd : %s" % ("ON" if self.lcd() else "OFF"),)
        res = res + ("high_current: %s" % ("ON" if self.high_current() else "OFF"),)
        return "\n".join(res)

    def vddh(self, newState = None):
        return self.__set_get(self.__vddh, newState)

    def high_current(self, newState = None):
        return self.__set_get(self.__high_current, newState)

    def buck(self, newState = None):
        return self.__set_get(self.__buck, newState)

    def ldo(self, newState = None):
        return self.__set_get(self.__ldo, newState)

    def lcd(self, newState=None):
        if newState != None:
            self.__lcd_state = True if newState==True else False
            self.high_current(self.__lcd_state)
            self.vddh(self.__lcd_state)
        return self.__lcd_state

class LimiFrogDisplay(SEPS525):

    XSIZE = const(160)
    YSIZE = const(128)

    def __init__(self, board, spi, cs, rs, reset):
        self.__board = board
        self.__reset = reset
        self.__reset.value(0)
        rs.value(1)
        cs.value(1)
        self.__reset.value(1)
        pyb.delay(10)
        self.__reset.value(0)
        pyb.delay(2)
        self.__reset.value(1)
        pyb.delay(2)
        super(LimiFrogDisplay, self).__init__(spi, cs, rs)

    def on(self):
        self.__board.lcd(1)
        pyb.delay(100)
        self.__com.write_reg(0x06, 0x01)

    def off(self):
        self.__com.write_reg(0x06, 0x00)
        self.__board.lcd(0)
        pyb.delay(100)

def display(board):
    spi = pyb.SPI(sys_config['oled']['spi_bus'], pyb.SPI.MASTER, baudrate=80000000, polarity=1, phase=0)
    reset = pyb.Pin(sys_config['oled']['reset'], pyb.Pin.OUT)
    rs = pyb.Pin(sys_config['oled']['rs'], pyb.Pin.OUT)
    cs = pyb.Pin(sys_config['oled']['spi_cs'], pyb.Pin.OUT)
    disp = LimiFrogDisplay(board, spi, cs=cs, rs=rs, reset=reset)
    return disp
    
