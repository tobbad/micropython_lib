"""
Driver for STMicroelectronics LSM303CTR Accel/Mag sensor for MicroPython.

This driver assumes a SPI device and two chip select pins given
to the constructor. 

The following example assumes that the CS is connected to the "PE0" pin
and spi bus 1 is used.

>>> from pyb import Pin
>>> cs_mag = Pin('PC1', Pin.OUT_PP, Pin.PULL_NONE)
>>> cs_mag.high()
>>> cs_accel = Pin('PC1', Pin.OUT_PP, Pin.PULL_NONE)
>>> cs_accel.high()
>>> from pyb import SPI
>>> spi_bus_nr = 5
>>> spi = SPI(spi_bus_nr, SPI.MASTER, baudrate=328125,
              polarity=1, phase=1, bits=8, direction=pyb.SPI.DIRECTION_1LINE)

>>> from lsm30ctr import LSM303CTR
>>> dev = LSM303CTR(spi, cs_mg, cs_acce)

Reading angular velocity:

>>> wx = d.omega_x()
>>> print(wx)
875.0

See:
    STM32Cube_FW_L4_V1.4.0/Drivers/BSP/Components/lsm303c/
"""
import pyb
from i2cspi import COM_SPI
from multibyte import multibyte

LSM303C_CTRL_REG1_A = const(0x20)   # Control register 1 acceleration 
LSM303C_CTRL_REG2_A = const(0x21)   # Control register 2 acceleration 
LSM303C_CTRL_REG3_A = const(0x22)   # Control register 3 acceleration 
LSM303C_CTRL_REG4_A = const(0x23)   # Control register 4 acceleration 
LSM303C_CTRL_REG5_A = const(0x24)   # Control register 5 acceleration 
LSM303C_CTRL_REG6_A = const(0x25)   # Control register 6 acceleration 
LSM303C_CTRL_REG7_A = const(0x26)   # Control register 6 acceleration    
LSM303C_WHO_AM_I_ADDR = const(0x0F)   # device identification register 
LMS303C_MAG_ID = const(0x3D)

class LSM303C_MAG(COM_SPI, multibyte):

    WHO_IAM_ANSWER = LMS303C_MAG_ID
    WHO_IAM_REG = LSM303C_WHO_AM_I_ADDR
    
    def __init__(self, communication, dev_selector):
        super(LSM303C_MAG, self).__init__(communication, dev_selector, self.ADDR_MODE_8, self.TRANSFER_MSB_FIRST)
        


class LSM303C():

    def __init__(self, communication, dev_selector_mag, dev_selector_accel):
        self.dev_mag = LSM303C_MAG(communication, dev_selector_mag)
        #self.dev_accel = COM_SPI(communication, dev_selector_mag, COM_SPI.ADDR_MODE_8, COM_SPI.TRANSFER_MSB_FIRST)
        self.dev_mag.DEBUG = True
        # Enabled SPI read communication 
        print(LSM303C_CTRL_REG4_A)
        self.dev_mag.write_u8(LSM303C_CTRL_REG4_A, 0x05)
        self.dev_mag.exists()
        
        
