from i2cspi import COM_I2C
from multibyte import multibyte
from lsm6ds3_const import *


class ACCGYRO(COM_I2C, multibyte):

    WHO_IAM_ANSWER = 0x69
    WHO_IAM_REG = 0xF

    def __init__(self, communication, dev_selector):
        super().__init__(communication, dev_selector,
                         self.ADDR_MODE_8,
                         self.TRANSFER_MSB_FIRST)
        # enable autoincrement
        tmp = self.read_u8(LSM6DS3_XG_CTRL3_C)
        tmp |= LSM6DS3_XG_IF_INC
        self.write_u8(LSM6DS3_XG_CTRL3_C, tmp)
        # Disable FIFO
        self.write(LSM6DS3_XG_FIFO_CTRL5,
                   LSM6DS3_XG_FIFO_MODE['BYPASS'] | LSM6DS3_XG_FIFO_ODR['NA'])

    def set_multi_byte(self, addr):
        ''' Multi byte read is configured in register CTRL3'''
        return addr

    def temperature(self):
        t = self.read_s16(LSM6DS3_TEMP_OUT_L)
        return 25.0 + t / 16.0


class ACCEL(ACCGYRO):

    def ctrl(self, g_odr='13HZ', g_full_scale_g='2G', g_axis_en="XYZ"):
        g_odr = g_odr.upper()
        g_full_scale_g = g_full_scale_g.upper()
        g_axis_en = g_axis_en.upper()

        tmp = self.read_u8(LSM6DS3_XG_CTRL1_XL)
        tmp &= ~LSM6DS3_XL_ODR['MASK']
        tmp |= LSM6DS3_XL_ODR[g_odr]
        tmp &= ~LSM6DS3_XL_FS['MASK']
        tmp |= LSM6DS3_XL_FS[g_full_scale_g]
        self.write_u8(LSM6DS3_XG_CTRL1_XL, tmp)

        tmp = self.read_u8(LSM6DS3_XG_CTRL9_XL)
        tmp &= ~LSM6DS3_XL_AXIS_EN['MASK']
        tmp |= LSM6DS3_XL_AXIS_EN['X'] if 'X' in g_axis_en else 0
        tmp |= LSM6DS3_XL_AXIS_EN['Y'] if 'Y' in g_axis_en else 0
        tmp |= LSM6DS3_XL_AXIS_EN['Z'] if 'Z' in g_axis_en else 0
        self.write_u8(LSM6DS3_XG_CTRL9_XL, tmp)

    def xyz(self):
        '''
        Returns the acceleration in 10^(-3) g.
        1 g = 9.81 m/s^2
        '''
        # Get raw data
        x = self.read_s16(LSM6DS3_XG_OUT_X_L_XL)
        y = self.read_s16(LSM6DS3_XG_OUT_Y_L_XL)
        z = self.read_s16(LSM6DS3_XG_OUT_Z_L_XL)
        # Get sensitivity
        sens = (self.read_u8(LSM6DS3_XG_CTRL1_XL) & LSM6DS3_XL_FS['MASK'])
        sens = (1 << (sens >> LSM6DS3_XL_FS['SHIFT'])) * 0.061
        return (x*sens, y*sens, z*sens)


class GYRO(ACCGYRO):

    def ctrl(self, gy_odr='13HZ', gy_full_scale_dps='2000',
             gy_axis_en='XYZ'):
        gy_odr = gy_odr.upper()
        gy_full_scale_dps = gy_full_scale_dps.upper()
        gy_axis_en = gy_axis_en.upper()
        # Gyro setup
        tmp = self.read_u8(LSM6DS3_XG_CTRL2_G)
        tmp &= ~LSM6DS3_G_ODR['MASK']
        tmp |= LSM6DS3_G_ODR[gy_odr]
        tmp &= ~LSM6DS3_G_FS['MASK']
        tmp |= LSM6DS3_G_FS[gy_full_scale_dps]
        self.write_u8(LSM6DS3_XG_CTRL2_G, tmp)
        # Axis selection
        tmp = self.read_u8(LSM6DS3_XG_CTRL10_C)
        tmp &= ~LSM6DS3_G_AXIS_EN['MASK']
        tmp |= LSM6DS3_G_AXIS_EN['X'] if 'X' in gy_axis_en else 0
        tmp |= LSM6DS3_G_AXIS_EN['Y'] if 'Y' in gy_axis_en else 0
        tmp |= LSM6DS3_G_AXIS_EN['Z'] if 'Z' in gy_axis_en else 0
        self.write_u8(LSM6DS3_XG_CTRL10_C, tmp)

    def xyz(self):
        # Get raw data
        x = self.read_s16(LSM6DS3_XG_OUT_X_L_G)
        y = self.read_s16(LSM6DS3_XG_OUT_Y_L_G)
        z = self.read_s16(LSM6DS3_XG_OUT_Z_L_G)
        # Get sensitivity
        sens = (self.read_u8(LSM6DS3_XG_CTRL2_G) & LSM6DS3_G_FS['MASK'])
        if sens == LSM6DS3_G_FS['125']:
            sens = 4.375
        elif sens == LSM6DS3_G_FS['245']:
            sens = 8.75
        elif sens == LSM6DS3_G_FS['500']:
            sens = 17.50
        elif sens == LSM6DS3_G_FS['1000']:
            sens = 35.0
        elif sens == LSM6DS3_G_FS['2000']:
            sens = 70.0
        else:
            raise Exception("Unknown gyro sensitivity 0x%02x" % (sens))
        return (x*sens, y*sens, z*sens)


class LSM6DS3():

    def __init__(self, communication, dev_selector):
        # Setup defaults on gyro and accel
        self.accel = ACCEL(communication, dev_selector)
        self.accel.ctrl()
        self.gyro = GYRO(communication, dev_selector)
        self.gyro.ctrl()

    def temperature(self):
        return self.accel.temperature()
