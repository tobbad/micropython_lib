# -*- coding: utf-8 -*-
"""
Driver for STMicroelectronics HTS221 Capacitive digital sensor
       for relative humidity and temperature for MicroPython.

This driver assumes a I2C device given to the constructor.

"""
from i2cspi import COM_I2C
from multibyte import multibyte


class HTS221(COM_I2C, multibyte):

    WHO_IAM_ANSWER = 0xBC

    WHO_IAM_REG = 0x0F
    AV_CONF_REG = 0x10
    CTRL_REG1 = 0x20
    PD_BIT = 0x07
    BDU_BIT = 0x02
    ODR_BIT = 0x00
    PD_MASK = 0x80
    BDU_MASK = 0x04
    ODR_MASK = 0x03
    CTRL_REG2 = 0x21
    CTRL_REG3 = 0x22
    STATUS_REG = 0x27
    HR_OUT_L_REG = 0x28
    T0_OUT_L = 0x2A
    # Calibration registers
    H0_RH_X2_REG = 0x30
    H1_RH_X2_REG = 0x31
    T0_DEGC_X8_REG = 0x32
    T1_DEGC_X8_REG = 0x33
    T0_T1_DEGC_H2_REG = 0x35
    H0_T0_OUT_L_REG = 0x36
    H0_T0_OUT_H_REG = 0x37
    H1_T0_OUT_L_REG = 0x3A
    H1_T0_OUT_H_REG = 0x3B
    T0_OUT_L_REG = 0x3C
    T0_OUT_H_REG = 0x3D
    T1_OUT_L_REG = 0x3E
    T1_OUT_H_REG = 0x3F

    def __init__(self, communication, dev_selector):
        super().__init__(communication, dev_selector,
                         self.ADDR_MODE_8,
                         self.TRANSFER_MSB_FIRST)
        self._set_up()
        self._load_calibration()

    def _set_up(self):
        tmp = self.read_u8(self.CTRL_REG1);

        # Enable BDU
        tmp &= ~self.BDU_MASK
        tmp |= (1 << self.BDU_BIT)

        # Set default ODR
        tmp &= ~self.ODR_MASK
        tmp |= 0x01 # Set ODR to 1Hz

        # Activate the device
        tmp |= self.PD_MASK

        # Apply settings to CTRL_REG1
        self.write_u8(self.CTRL_REG1, tmp)

    def _load_calibration(self):
        self._h0_rh = self.read_u8(self.H0_RH_X2_REG) >> 1
        self._h1_rh = self.read_u8(self.H1_RH_X2_REG) >> 1
        self._h0_t0_out = self.read_s16(self.H0_T0_OUT_L_REG)
        self._h1_t0_out = self.read_s16(self.H1_T0_OUT_L_REG)
        T_MSB = self.read_u8(self.T0_T1_DEGC_H2_REG)
        self._T0_degC = (self.read_u8(self.T0_DEGC_X8_REG) | ((T_MSB & 0x03) << 8))/8.0
        self._T1_degC = (self.read_u8(self.T1_DEGC_X8_REG) | ((T_MSB & 0x0C) << 6))/8.0
        self._T0_out = self.read_s16(self.T0_OUT_L_REG)
        self._T1_out = self.read_s16(self.T1_OUT_L_REG)

    def print_calib(self):
        print("h0_rh = %d" % (self._h0_rh))
        print("h1_rh = %d" % (self._h1_rh))
        print("h0_t0_out = %d" % (self._h0_t0_out))
        print("h1_t0_out = %d" % (self._h1_t0_out))
        print("T0_degC = %f" % (self._T0_degC))
        print("T1_degC = %f" % (self._T1_degC))
        print("T0_out = %d" % (self._T0_out))
        print("T1_out = %d" % (self._T1_out))

    def average_conf(self, shift, mask, value):
        value &= mask
        value <<= shift
        mask_s = mask << shift
        c_val = self.read(HTS221.AV_CONF_REG) & (~mask_s)
        c_val |= value
        self.write(HTS221.AV_CONF_REG, value)

    def average_t_conf(self, value):
        self.average_conf(0x07, 3, value)

    def average_h_conf(self, value):
        self.average_conf(0x07, 0, value)

    def temperature(self):
        T_out = self.read_s16(self.T0_OUT_L)
        T = float(T_out - self._T0_out) * float(self._T1_degC - self._T0_degC) / float(self._T1_out - self._T0_out)  +  self._T0_degC
        return T

    def humidity(self):
        h_t_out = self.read_u16(self.HR_OUT_L_REG)
        hum = float(h_t_out - self._h0_t0_out) * float(self._h1_rh - self._h0_rh) / float(self._h1_t0_out - self._h0_t0_out)  +  self._h0_rh
        hum *= 10.0
        hum = hum if hum > 0 else 0.0
        hum = hum if hum < 1000 else 1000.0
        return hum/10.0
