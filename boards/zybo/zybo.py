#!/usr/bin/python3

from micropython_lib.host.zynq_uart_spi import ZYNQ_UART_SPI as SPI
import serial
import inspect
import time

dev_name = '/dev/ttyUSB1'


class COMM:

    DEBUG = False
    CRLF = '\r\n'

    def __init__(self, com_dev_fname, debug = True):
        self.DEBUG = debug
        self._com = serial.Serial(com_dev_fname, baudrate = 115200, timeout = 0.1)
        self._com.flushInput()

    def read(self, cnt=10000):
        data =  self._com.read(cnt)
        data = data.decode('latin-1').split(self.CRLF)
        if self.DEBUG:
            for idx, i in enumerate(data):
                print("data[%2d]: %s" % (idx,i))
        return data

    def write(self, data=""):
        data += self.CRLF
        if self.DEBUG:
            print("Send data: %s" % data[0:-len(self.CRLF)])
        self._com.write(bytes(data, 'latin-1'))
        return

class ZYBO:

    class GPIO_PIN:
        OUT = 0
        IN = 1
        MARKER = 'PIN'
        PIN_AT86RF215_RESET = (830, OUT)

    class REGISTER:
        BASE_ADDR = (0x43C00000, 0x43C10000)

        class FIFO_RX:
            ADDR = 0x00

        class FIFO_TX:
            ADDR = 0x04

        class STATUS:
            ADDR = 0x08
            FIFO_FULL = ( 0x1, 0)

        class CONTROL:
            ADDR = 0x0C
            FIFO_LIMIT = (0x1FF,0)
            FIFO_RESET = (0x1, 16)
            DESER_CLK_RESET = (0x1, 17)
            DESER_IO_RESET = (0x1, 18)
            BITSLIP = (0x1, 31)

    LOGIN = False
    DEBUG = False
    IN_PIN = [ ]
    OUT_PIN_INI_VALUE = [(830, 0),]

    def __init__(self, dev_name, debug = False):
        self.com = COMM(dev_name, debug)
        self.DEBUG = debug
        self.com.write()
        res = self.com.read()
        if self.DEBUG:
            print("Initial read:"+str(res))
        if 'login' in res[-1]:
            if self.login():
                self.LOGIN = True
                self.set_up_GPIO()
        elif 'root' in res[-1]:
            self.LOGIN = True
        self.set_up_GPIO()
        self.reset_at86rf215(False)
        self.spi = SPI(self.com, 0, 0, debug = self.DEBUG)


    def login(self):
        success = False
        self.com.write('root')
        res1 = self.com.read()
        while 'assword'  not in res1[-1]:
            self.com.write('root')
            res1 = self.com.read()
        self.com.write('root')
        res2 = self.com.read()
        if "root" in res2[-1]:
            success = True
        return success

    def set_up_GPIO(self):
        marker = self.GPIO_PIN.MARKER
        for name, item in inspect.getmembers(self.GPIO_PIN):
            if name[0:len(marker)] == marker:
                pin_nr, direction = item
                self.com.write("echo %d > /sys/class/gpio/export" % (pin_nr))
                self.com.read()
                if direction == self.GPIO_PIN.OUT:
                    self.com.write("echo out > /sys/class/gpio/gpio%d/direction" % (pin_nr))
                else:
                    self.com.write("echo in > /sys/class/gpio/gpio830/direction" % (pin_nr))
                self.com.read()

    def pin_value(self, pin_nr, value):
        self.com.write("echo %d > /sys/class/gpio/gpio%d/value" % (value, pin_nr))
        self.com.read()

    def reset_at86rf215(self, mode=False):
        pin_nr = self.GPIO_PIN.PIN_AT86RF215_RESET[0]
        self.pin_value(pin_nr, 0 if mode else 1)

    def memory(self, addr, value=None):
        tpl = "devmem 0x%08x 32 %s"
        cmd = tpl % (addr, "0x%08x" % value if value is not None else "")
        self.com.write(cmd)
        res = self.com.read()
        if value == None:
            value = int(res[1], 16)
        return value

    def bit(self, addr, mask, value):
        val = self.memory(addr) & ~mask
        val |= mask if value>0 else 0
        self.memory(addr, val)

    def reset_deser(self, inst, value = 1):
        addr = self.REGISTER.BASE_ADDR[inst]
        addr+=self.REGISTER.CONTROL.ADDR
        mask = self.REGISTER.CONTROL.DESER_IO_RESET[0] << self.REGISTER.CONTROL.DESER_IO_RESET[1]
        self.bit(addr, mask, value)

    def reset_fifo(self, inst, value = 1):
        addr = self.REGISTER.BASE_ADDR[inst]
        addr+=self.REGISTER.CONTROL.ADDR
        mask = self.REGISTER.CONTROL.FIFO_RESET[0] << self.REGISTER.CONTROL.FIFO_RESET[1]
        self.bit(addr, mask, value)

    def bitslip(self, inst):
        addr = self.REGISTER.BASE_ADDR[inst]
        addr+=self.REGISTER.CONTROL.ADDR
        mask = self.REGISTER.CONTROL.BITSLIP[0] << self.REGISTER.CONTROL.BITSLIP[1]
        self.bit(addr, mask, 1)
        self.bit(addr, mask, 0)

    def fifo(self, inst, value = None):
        addr = self.REGISTER.BASE_ADDR[inst]
        addr+= self.REGISTER.FIFO_RX.ADDR if value is None else self.REGISTER.FIFO_TX.ADDR
        return self.memory(addr, value)

    def sync_rxd(self, inst):
        success = True
        self.reset_deser(inst,1)
        self.reset_deser(inst,0)
        mask = 0xC001C001
        exp_val = 0x80004000
        val = self.fifo(inst) & mask
        cnt = 32
        while val != exp_val:
            self.bitslip(inst)
            self.reset_fifo(inst,1)
            self.reset_fifo(inst,0)
            for i in range(5):
                val = self.fifo(inst)
                if i>0:
                    print("{0:2d} {1:032b} 0x{2:08X}".format(32-cnt,val, val&mask))
            cnt-=1
            if cnt == 0:
                success = False
                break
            val &= mask
        return success
