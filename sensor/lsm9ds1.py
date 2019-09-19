from i2cspi import COM_I2C
from multibyte import multibyte
from lsm9ds1_const import *


class ACCGYRO(COM_I2C, multibyte):

    WHO_IAM_ANSWER = 0x68
    WHO_IAM_REG = 0xF

    def __init__(self, communication, dev_selector):
        super().__init__(communication, dev_selector,
                         self.ADDR_MODE_8,
                         self.TRANSFER_MSB_FIRST)
        # enable autoincrement
        tmp = self.read_u8(LSM9DS1_CTRL8)
        tmp |= LSM9DS1_CTRL8_BDU
        tmp |= LSM9DS1_CTRL8_IF_ADD_INC
        self.write_u8(LSM9DS1_CTRL8, tmp)

    def set_multi_byte(self, addr):
        ''' Multi byte read is configured in register CTRL8'''
        return addr

    def temperature(self):
        t = self.read_s16(LSM9DS1_TEMP_OUT_L)
        return  t/16.0 + 25.0 


class ACCEL(ACCGYRO):
    #
    # Modified finished
    # ToDo check Measurement
    # 
    
    def ctrl(self, g_odr='10HZ', g_full_scale_g='2G', g_axis_en="XYZ"):
        g_odr = g_odr.upper()
        g_full_scale_g = g_full_scale_g.upper()
        g_axis_en = g_axis_en.upper()

        tmp = self.read_u8(LSM9DS1_CTRL6_XL)
        tmp &= ~LSM9DS1_CTRL6_XL_ODR['MASK']
        tmp |= LSM9DS1_CTRL6_XL_ODR[g_odr]
        tmp &= ~LSM9DS1_CTRL6_XL_FS['MASK']
        tmp |= LSM9DS1_CTRL6_XL_FS[g_full_scale_g]
        self.write_u8(LSM9DS1_CTRL6_XL, tmp)

        tmp = self.read_u8(LSM9DS1_CTRL5_XL)
        tmp &= ~LSM9DS1_CTRL5_XL_AXIS_EN['MASK']
        tmp |= LSM9DS1_CTRL5_XL_AXIS_EN['X'] if 'X' in g_axis_en else 0
        tmp |= LSM9DS1_CTRL5_XL_AXIS_EN['Y'] if 'Y' in g_axis_en else 0
        tmp |= LSM9DS1_CTRL5_XL_AXIS_EN['Z'] if 'Z' in g_axis_en else 0
        self.write_u8(LSM9DS1_CTRL5_XL, tmp)

    def xyz(self):
        '''
        Returns the acceleration in 10^(-3) g.
        1 g = 9.81 m/s^2
        '''
        # Get raw data
        x = self.read_s16(LSM9DS1_OUT_X_L_XL)
        y = self.read_s16(LSM9DS1_OUT_Y_L_XL)
        z = self.read_s16(LSM9DS1_OUT_Z_L_XL)
        # Get sensitivity
        sens = (self.read_u8(LSM9DS1_CTRL6_XL) & LSM9DS1_CTRL6_XL_FS['MASK'])>> LSM9DS1_CTRL6_XL_FS['SHIFT']
        sens = LSM9DS1_CTRL6_XL_FS['MAP'][sens]/(2**16)
        return (x*sens, y*sens, z*sens)


class GYRO(ACCGYRO):
    #
    # Modified finished
    # ToDo check Measurement
    # 
 
    def ctrl(self, gy_odr='14HZ9', gy_full_scale_dps='245',
             gy_axis_en='XYZ'):
        gy_odr = gy_odr.upper()
        gy_full_scale_dps = gy_full_scale_dps.upper()
        gy_axis_en = gy_axis_en.upper()
        # Gyro setup
        tmp = self.read_u8(LSM9DS1_CTRL1_G)
        tmp &= ~LSM9DS1_CTRL1_G_ODR['MASK']
        tmp |= LSM9DS1_CTRL1_G_ODR[gy_odr]
        tmp &= ~LSM9DS1_CTRL1_G_FS['MASK']
        tmp |= LSM9DS1_CTRL1_G_FS[gy_full_scale_dps]
        self.write_u8(LSM9DS1_CTRL1_G, tmp)
        # Axis selection
        tmp = self.read_u8(LSM9DS1_CTRL4)
        tmp &= ~LSM9DS1_CTRL4_G_AXIS_EN['MASK']
        tmp |= LSM9DS1_CTRL4_G_AXIS_EN['X'] if 'X' in gy_axis_en else 0
        tmp |= LSM9DS1_CTRL4_G_AXIS_EN['Y'] if 'Y' in gy_axis_en else 0
        tmp |= LSM9DS1_CTRL4_G_AXIS_EN['Z'] if 'Z' in gy_axis_en else 0
        self.write_u8(LSM9DS1_CTRL4, tmp)

    def xyz(self):
        # Get raw data
        x = self.read_s16(LSM9DS1_OUT_X_G_L)
        y = self.read_s16(LSM9DS1_OUT_Y_G_L)
        z = self.read_s16(LSM9DS1_OUT_Z_G_L)
        # Get sensitivity
        sens = (self.read_u8(LSM9DS1_CTRL1_G) & LSM9DS1_CTRL1_G_FS['MASK'])>>LSM9DS1_CTRL1_G_FS['SHIFT']
        sens = LSM9DS1_CTRL1_G_FS['MAP'][sens]/2**16
        return (x*sens, y*sens, z*sens)

class MAG(COM_I2C, multibyte):

    WHO_IAM_ANSWER = 0x3D
    WHO_IAM_REG = 0xF

    def __init__(self, communication, dev_selector):
        super().__init__(communication, dev_selector,
                         self.ADDR_MODE_8,
                         self.TRANSFER_MSB_FIRST)
        # enable 
        tmp = self.read_u8(LSM9DS1_CTRL_REG3_M)
        tmp &= ~LSM9DS1_CTRL_REG3_M_CONV_MODE['MASK']
        tmp |= LSM9DS1_CTRL_REG3_M_CONV_MODE['CONTINUOUS']
        self.write_u8(LSM9DS1_CTRL_REG3_M, tmp)
        # Block read mode
        tmp = self.read_u8(LSM9DS1_CTRL_REG5_M)
        tmp |= LSM9DS1_CTRL_REG5_M_BDU
        self.write_u8(LSM9DS1_CTRL_REG5_M, tmp)

    def set_multi_byte(self, addr):
        ''' Multi byte read is configured in register CTRL3'''
        return addr

    def ctrl(self, m_odr='5HZ', m_full_scale_g='4G',
             m_axis_en='XYZ'):
        m_odr = m_odr.upper()
        m_full_scale_g = m_full_scale_g.upper()
        m_axis_en = m_axis_en.upper()
        # Output data rate
        tmp = self.read_u8(LSM9DS1_CTRL_REG1_M)
        tmp &= ~LSM9DS1_CTRL_REG1_M_ODR['MASK']
        tmp |= LSM9DS1_CTRL_REG1_M_ODR[m_odr]
        self.write_u8(LSM9DS1_CTRL_REG1_M, tmp)

    def xyz(self):
        # Get raw data
        x = self.read_s16(LSM9DS1_OUT_X_L_M)
        y = self.read_s16(LSM9DS1_OUT_Y_L_M)
        z = self.read_s16(LSM9DS1_OUT_Z_L_M)
        # Get sensitivity
        sens = (self.read_u8(LSM9DS1_CTRL_REG2_M) & LSM9DS1_CTRL_REG2_M_FS['MASK'])
        sens >>= LSM9DS1_CTRL_REG2_M_FS['SHIFT']
        sens = LSM9DS1_CTRL_REG2_M_FS['MAP'][sens]/2**15
        return (x*sens, y*sens, z*sens)


class LSM9DS1():

    def __init__(self, communication, dev_acc_sel, dev_gyr_sel, dev_mag_sel):
        # Setup defaults on gyro and accel
        self.accel = ACCEL(communication, dev_acc_sel)
        self.accel.ctrl()
        self.gyro = GYRO(communication, dev_gyr_sel)
        self.gyro.ctrl()
        self.mag = MAG(communication, dev_mag_sel)
        self.mag.ctrl()

    def temperature(self):
        return self.accel.temperature()
