#
#
#
import pyb

class limifrog():

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
        res = ("vddh: %s" % ("ON" if self.vddh() else "OFF"),)
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