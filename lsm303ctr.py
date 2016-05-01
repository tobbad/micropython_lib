"""
Driver for STMicroelectronics LSM303CTR yro for MicroPython.

This driver assumes a SPI device and a chip select (CS) pin given
to the constructor.

The following example assumes that the CS is connected to the "PE0" pin
and spi bus 5 is used.

>>> from pyb import Pin
>>> cs_mag = Pin('PC1', Pin.OUT_PP, Pin.PULL_NONE)
>>> cs_mag.high()
>>> cs_accel = Pin('PC1', Pin.OUT_PP, Pin.PULL_NONE)
>>> cs_accel.high()
>>> from pyb import SPI
>>> spi_bus_nr = 5
>>> spi = SPI(spi_bus_nr, SPI.MASTER, baudrate=328125,
              polarity=1, phase=1, bits=8)

>>> from lsm30ctrl3gd20 import LSM303CTR
>>> dev = LSM303CTR(spi, cs_mg, cs_acce, three_Wire = True)

Reading angular velocity:

>>> wx = d.omega_x()
>>> print(wx)
875.0

See:
    STM32Cube_FW_F4_V1.3.0/Drivers/BSP/Components/l3gd20/l3gd20.h
    STM32Cube_FW_F4_V1.3.0/Drivers/BSP/Components/l3gd20/l3gd20.c
"""
import pyb

class LSM303CTR():

    def __init__(self, spi, cs_mag, cs_accel):
        self.is3Wire = three_Wire
        self.cs_mag = cs_mag
        self.cs_accel = cs_accel
        self.spi = spi
        