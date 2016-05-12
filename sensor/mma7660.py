"""
Driver for STMicroelectronics L3GD20 gyro for MicroPython.

This driver assumes a SPI device and a chip select (CS) pin given
to the constructor.

The following example assumes that the CS is connected to the "PC1" pin
and spi bus 5 is used.

>>> from pyb import Pin
>>> cs = Pin('PC1', Pin.OUT_PP, Pin.PULL_NONE)
>>> cs.high()
>>> from pyb import SPI
>>> spi_bus_nr = 5
>>> spi = SPI(spi_bus_nr, SPI.MASTER, baudrate=328125,
              polarity=1, phase=1, bits=8)

>>> from stm_l3gd20 import L3GD20
>>> dev = L3GD20(cs, spi)

Reading angular velocity:

>>> wx = d.omega_x()
>>> print(wx)
875.0

See:
    STM32Cube_FW_F4_V1.3.0/Drivers/BSP/Components/l3gd20/l3gd20.h
    STM32Cube_FW_F4_V1.3.0/Drivers/BSP/Components/l3gd20/l3gd20.c
"""
from i2cspi import COM_I2C
from multibyte import multibyte

MMA7660_X_ADDR = const(0x01)  # Output Register X
MMA7660_Y_ADDR = const(0x02)  # Output Register Y
MMA7660_Z_ADDR = const(0x03)  # Output Register Z


class MMA7660(COM_SPI, multibyte):
    #
    # Debug
    #
    DEFAULT_CONF = [
        (0x07, 0x01),]

    WHO_IAM_ANSWER = 0
    WHO_IAM_REG = 0
    WHO_IAM_ANSWER_MASK = 0x00

    def __init__(self, communication, dev_selector):
        """
        Create a MMA7660 device.
        """
        super().__init__(communication, dev_selector,
                         self.ADDR_MODE_8,
                         self.TRANSFER_MSB_FIRST)
        self.init()

    def _reg2val(self, reg):
        val =self.read_u8(reg)
        val = val-64 if val >=32 else val
        return val


    def x(self):
        """
        Get angular velocity around x axis in degree per second.
        """
        return self._reg2val(MMA7660_X_ADDR)

    def y(self):
        """
        Get angular velocity around y axis.in degree per second.
        """
        return self._reg2val(MMA7660_Y_ADDR)

    def z(self):
        """
        Get angular velocity around z axis in degree per second.
        """
        return self._reg2val(MMA7660_Z_ADDR)

    def xyz(self):
        """
        Get tuple of all angular velocities in degree per second.
        """
        return (self.x(), self.y(), self.z())
