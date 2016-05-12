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
from i2cspi import COM_SPI
from multibyte import multibyte
from l3gd20_const import *


class L3GD20(COM_SPI, multibyte):
    #
    # Debug
    #
    DEFAULT_CONF = [
        (L3GD20_CTRL_REG1_ADDR, L3GD20_CTRL_REG1_VAL),
        (L3GD20_CTRL_REG2_ADDR, L3GD20_CTRL_REG2_VAL),
        (L3GD20_CTRL_REG3_ADDR, L3GD20_CTRL_REG3_VAL),
        (L3GD20_CTRL_REG4_ADDR, L3GD20_CTRL_REG4_VAL),
        (L3GD20_CTRL_REG5_ADDR, L3GD20_CTRL_REG5_VAL)]

    WHO_IAM_ANSWER = L3GD20_I_AM_L3GD20
    WHO_IAM_REG = L3GD20_WHO_AM_I_ADDR

    def __init__(self, communication, dev_selector):
        """
        Create a L3GD20 device.
        """
        super().__init__(communication, dev_selector,
                         self.ADDR_MODE_8,
                         self.TRANSFER_MSB_FIRST)
        self.init()

    def _update_dps_fs(self, new_fullscale):
        conv = {
            L3GD20_FULLSCALE_250: L3GD20_SENSITIVITY_250DPS,
            L3GD20_FULLSCALE_500: L3GD20_SENSITIVITY_500DPS,
            L3GD20_FULLSCALE_2000: L3GD20_SENSITIVITY_2000DPS,
            L3GD20_FULLSCALE_SELECTION: L3GD20_SENSITIVITY_2000DPS}
        entry = new_fullscale & L3GD20_FULLSCALE_SELECTION
        self._sensitivity = conv[entry]

    def write_binary(self, reg_addr, data):
        """
        Write byte to a certain address.
        SIDE EFFECT: If data is written to
        L3GD20_CTRL_REG4_ADDR the conversion factor is recalculated
        based on the register value.
        """
        super().write_binary(reg_addr, data)
        if reg_addr == L3GD20_CTRL_REG4_ADDR:
            self._update_dps_fs(data[0])

    def x(self):
        """
        Get angular velocity around x axis in degree per second.
        """
        return self.read_s16(L3GD20_OUT_X_L_ADDR) * self._sensitivity

    def y(self):
        """
        Get angular velocity around y axis.in degree per second.
        """
        return self.read_s16(L3GD20_OUT_Y_L_ADDR) * self._sensitivity

    def z(self):
        """
        Get angular velocity around z axis in degree per second.
        """
        return self.read_s16(L3GD20_OUT_Z_L_ADDR) * self._sensitivity

    def xyz(self):
        """
        Get tuple of all angular velocities in degree per second.
        """
        return (self.x(), self.y(), self.z())

    def temperature(self):
        """
        Get temperatur of device as integer degree celsius.
        """
        return self.read_s8(L3GD20_OUT_TEMP_ADDR)
