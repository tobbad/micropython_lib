'''
Driver for Samtech SX1276/77/78/79 which is
the same chip as HopeRF RF-96
'''
from i2cspi import COM_SPI


class SX127X(COM_SPI):

    WHO_IAM_REG = 0x42
    WHO_IAM_ANSWER = 0x12

    def __init__(self, communication, dev_selector):
        super().__init__(communication, dev_selector,
                         addr_size=self.ADDR_MODE_8,
                         msb_first=self.TRANSFER_MSB_FIRST)

