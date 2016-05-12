from i2cspi import COM_I2C
from multibyte import multibyte
import pyb

BEEPTONE_ADDR = const(0x1e)


class CS43L22(COM_I2C, multibyte):

    WHO_IAM_REG = 0x01
    WHOAMI_ANS = 0xE0
    WHOAMI_ANS_MASK = 0xF8
    __reg = [0x01, 0x02, 0x04, 0x05, 0x06, 0x08, 0x09,
             0x0a, 0x0c, 0x0d, 0x0e, 0x0f, 0x15, 0x1A, 0x1B,
             0x1C, 0x1d, 0x1E, 0x1F, 0x20, 0x21, 0x23, 0x25,
             0x26, 0x27, 0x28, 0x29, 0x2e, 0x2f, 0x30, 0x31,
             0x34]

    def __init__(self, communication, dev_selector, resetPin):
        # Release reset from the device
        self.reset = resetPin
        self.reset.low()
        pyb.delay(10)
        self.reset.high()
        pyb.delay(10)
        super().__init__(communication, dev_selector,
                         addr_size=self.ADDR_MODE_8,
                         msb_first=self.TRANSFER_MSB_FIRST)

    def init(self):
        print([hex(i) for i in self.com.scan()])

        self.write_u8(0x00, 0x99)
        self.write_u8(0x47, 0x80)
        self.write_u8(0x32, 0x80)
        self.write_u8(0x32, 0x00)
        self.write_u8(0x00, 0x00)
        self.write_u8(0x02, 0x9e)
        pyb.delay(100)

        # Volume
        self.write_u8(0x20, 0x18)
        self.write_u8(0x21, 0x18)
        self.write_u8(0x1a, 0x18)
        self.write_u8(0x1b, 0x18)

        self.write_u8(0x1c, 0x0f)
        self.write_u8(0x1d, 0x06)
        self.write_u8(BEEPTONE_ADDR, 0xc0)

    def __str__(self):
        res = []
        for r in self.__reg:
            val = self.read_u8(r)
            res.append("Reg[0x%02X]= 0x%02X" % (r, val))
        return "\n".join(res)

    def set(self, reg, value):
        if reg in self.__reg:
            self.write_u8(reg, value)
        else:
            print("Not supported register 0x%02X" % (reg))

    def get(self, reg):
        if reg in self.__reg:
            return self.read_u8(reg)
        else:
            print("Not supported register 0x%02X" % (reg))
            return None

    def __u82db(self, value):
        if value <= 12:
            value = value/0.5
        else:
            (256-value)*0.5
            value = max(-102, value)
        return value

    def volume(self, value=None):
        if value is None:
            for reg, ch in ((0x20, 'A'), (0x21, 'B')):
                value = self.read_u8(reg)
                print("Volume %s: %.1f dB" % (ch, self.__u82db(value)))

    def beep(self, freq, time):
        pass
