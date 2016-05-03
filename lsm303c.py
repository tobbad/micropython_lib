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

>>> from lsm30c import LSM303CTR
>>> dev = LSM303C(spi, cs_mg, cs_acce)

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
from lsm303c_const import *

class LSM303C_MAG(COM_SPI, multibyte):

    WHO_IAM_ANSWER = LMS303C_MAG_ID
    WHO_IAM_REG = LSM303C_WHO_AM_I_ADDR

    DEFAULT_CONF = [(LSM303C_CTRL_REG2_M, LSM303C_MAG_REBOOT_ENABLE | LSM303C_MAG_SOFT_RESET_ENABLE  ),
                    (LSM303C_CTRL_REG2_M, LSM303C_MAG_FS_16_GA | LSM303C_MAG_REBOOT_DEFAULT | LSM303C_MAG_SOFT_RESET_DEFAULT  ),
                    (LSM303C_CTRL_REG3_M, LSM303C_MAG_SPI_MODE | LSM303C_MAG_CONFIG_NORMAL_MODE | LSM303C_MAG_CONTINUOUS_MODE ),
                    (LSM303C_CTRL_REG1_M, LSM303C_MAG_TEMPSENSOR_DISABLE | LSM303C_MAG_OM_XY_ULTRAHIGH | LSM303C_MAG_ODR_40_HZ),                    
                    (LSM303C_CTRL_REG4_M, LSM303C_MAG_OM_Z_ULTRAHIGH | LSM303C_MAG_BLE_LSB                                    ),
                    (LSM303C_CTRL_REG5_M, LSM303C_MAG_BDU_CONTINUOUS                                                          )]
    
    def __init__(self, communication, dev_selector):
        super(LSM303C_MAG, self).__init__(communication, dev_selector, self.ADDR_MODE_8, self.TRANSFER_MSB_FIRST)
        
    def set_multi_byte(self, addr):
        multi_byte_mask = 0x04
        val = self.read_u8(LSM303C_CTRL_REG4_M) 
        if val & multi_byte_mask == 0:
            val |= multi_byte_mask
            self.write_u8(LSM303C_CTRL_REG4_M, val)
        return addr

    def _update_dps_fs(self, new_value):
        fs_max = 2**15
        conv = {
            LSM303C_MAG_FS_16_GA: 16.0/fs_max}
        if new_value not in conv:
            return 
        self._sensitivity = conv[new_value & 0x60] 

    def write_binary(self, reg_addr, data):
        """
        Write byte to a certain address.
        SIDE EFFECT: If data is written to
        L3GD20_CTRL_REG4_ADDR the conversion factor is recalculated
        based on the register value.
        """
        super(LSM303C_MAG, self).write_binary(reg_addr, data)
        if reg_addr == LSM303C_CTRL_REG2_M:
            self._update_dps_fs(data[0])

    def x(self):
        val = self.read_s16(LSM303C_OUT_X_L_A)
        return val*self._sensitivity

    def y(self):
        val = self.read_s16(LSM303C_OUT_Y_L_A)
        return val*self._sensitivity

    def z(self):
        val = self.read_s16(LSM303C_OUT_Z_L_A)
        return val*self._sensitivity

    def xyz(self):
        return self.x(), self.y(), self.z()

class LSM303C_ACCEL(COM_SPI, multibyte):

    WHO_IAM_ANSWER = LMS303C_ACC_ID
    WHO_IAM_REG = LSM303C_WHO_AM_I_ADDR
    DEFAULT_CONF = [(LSM303C_CTRL_REG5_A, LSM303C_ACC_SOFT_RESET_ENABLE ),
                    (LSM303C_CTRL_REG4_A, LSM303C_ACC_FULLSCALE_2G | LSM303C_ACC_SPI_MODE ),
                    (LSM303C_CTRL_REG1_A, LSM303C_ACC_HR_DISABLE | LSM303C_ACC_ODR_50_HZ | LSM303C_ACC_AXES_ENABLE |LSM303C_ACC_BDU_CONTINUOUS),
                    ]
    
    def __init__(self, communication, dev_selector):
        super(LSM303C_ACCEL, self).__init__(communication, dev_selector, self.ADDR_MODE_8, self.TRANSFER_MSB_FIRST)
 
    def set_multi_byte(self, addr):
        multi_byte_mask = 0x04
        val = self.read_u8(LSM303C_CTRL_REG4_A)
        if val & multi_byte_mask == 0:
            val |= multi_byte_mask
            self.write_u8(LSM303C_CTRL_REG4_A, val)
        return addr
    
    def _update_dps_fs(self, new_value):
        fs_max = 2**15
        conv = {
            LSM303C_ACC_FULLSCALE_2G: 2.0/fs_max,
            LSM303C_ACC_FULLSCALE_4G: 4.0/fs_max,
            LSM303C_ACC_FULLSCALE_8G: 8.0/fs_max}
        self._sensitivity = conv[new_value & 0x30] 

    def write_binary(self, reg_addr, data):
        """
        Write byte to a certain address.
        SIDE EFFECT: If data is written to
        L3GD20_CTRL_REG4_ADDR the conversion factor is recalculated
        based on the register value.
        """
        super(LSM303C_ACCEL, self).write_binary(reg_addr, data)
        if reg_addr == LSM303C_CTRL_REG4_A:
            self._update_dps_fs(data[0])

    def x(self):
        val = self.read_s16(LSM303C_OUT_X_L_M)
        return val*self._sensitivity

    def y(self):
        val = self.read_s16(LSM303C_OUT_Y_L_M)
        return val*self._sensitivity

    def z(self):
        val = self.read_s16(LSM303C_OUT_Z_L_M)
        return val*self._sensitivity

    def xyz(self):
        return self.x(), self.y(), self.z()



class LSM303C():

    def __init__(self, communication, dev_selector_mag, dev_selector_accel):
        self.mag = LSM303C_MAG(communication, dev_selector_mag)
        #self.mag.DEBUG = True
        self.mag.bidi_mode = True
        self.mag.init()
        self.accel = LSM303C_ACCEL(communication, dev_selector_accel)
        #self.accel.DEBUG = True
        self.accel.bidi_mode = True
        self.accel.init()
        # Enabled SPI read communication 
        #print(LSM303C_CTRL_REG4_A)
        #self.dev_mag.write_u8(LSM303C_CTRL_REG4_A, 0x05)
        

    def set_bidi_mode(self, value=True):
        self.mag.bidi_mode = value
        self.accel.bidi_mode = value
        
    def init(self):
        self.mag.init()
        self.accel.init()
        
    def exists(self):
        self.mag.exists()
        self.accel.exists()
