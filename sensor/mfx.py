# -*- coding: utf-8 -*-
'''
Driver for the MFX extension modules mounted on the STM32L476G-DISCO
and maybe useable on other boards (STM32L496GDISCO?)
'''
from i2cspi import COM_I2C
from multibyte import multibyte
import time
from board import IDD_DEFAULT
from mfx_const import *

class MFX(COM_I2C, multibyte):
    ''' Multifunction expansion module is a STM32L152 based expansion to 
        the functionality of the kit.'''
    
    def __init__(self, communication, dev_selector, 
                 wakeup_pin, config, irq_pin=None):
        super().__init__(communication, dev_selector,
                         self.ADDR_MODE_8,
                         self.TRANSFER_MSB_FIRST, False)
        self._wakeup = wakeup_pin
        self._config = config
        self._irq = irq_pin
        self.DEBUG = True
        self.wakeUp()
               
    def __str__(self):
        res =  ("ID         : 0x%02X" % (self.id()),)
        res += ("FW Version : %d" %(self.fw_version()),)
        return "\n".join(res)
        
    def _enable(self, reg, flag):
        tmp = self.read(reg)
        tmp |= flag
        self.write(reg, tmp)
        
    def wakeUp(self):
        self._wakeup.value(1)
        time.sleep_ms(1)
        self._wakeup.value(1)
        time.sleep_ms(5)
        
    def id(self):
        return self.read(REG_ADR_ID)
    
    def fw_version(self):
        return self.read_u16_r(REG_ADR_FW_VERSION_MSB)
   
    def enable_idd(self):
        self._enable(REG_ADR_IDD_CTRL, IDD_CTRL_REQ)
        
    def config_idd(self):
        self._enable(REG_ADR_SYS_CTRL, SYS_CTRL_IDD_EN)
        # Control register setting: number of shunts 
        value =  ((self._config.ShuntNbUsed << 1) & IDD_CTRL_SHUNT_NB)
        value |= (self._config.VrefMeasurement & IDD_CTRL_VREF_DIS)
        value |= (self._config.Calibration & IDD_CTRL_CAL_DIS)
        self.write(REG_ADR_IDD_CTRL, value)

        # Idd pre delay configuration: unit and value
        value = (self._config.PreDelayUnit & IDD_PREDELAY_UNIT) | \
                (self._config.PreDelayValue & IDD_PREDELAY_VALUE)
        self.write(REG_ADR_IDD_PRE_DELAY, value)

        # Shunt 0 register value: MSB then LSB 
        value = self._conf.Shunt0Value >> 8
        self.write(REG_ADR_IDD_SHUNT0_MSB, value)
        value = self._conf.Shunt0Value
        self.write(REG_ADR_IDD_SHUNT0_LSB, value)

        # Shunt 1 register value: MSB then LSB 
        value = self._conf.Shunt1Value >> 8
        self.write(REG_ADR_IDD_SHUNT1_MSB, value)
        value = self._conf.Shunt1Value
        self.write(REG_ADR_IDD_SHUNT1_LSB, value)

        # Shunt 2 register value: MSB then LSB 
        value = self._conf.Shunt2Value >> 8
        self.write(REG_ADR_IDD_SHUNT2_MSB, value)
        value = self._conf.Shunt2Value
        self.write(REG_ADR_IDD_SHUNT2_LSB, value)

        # Shunt 3 register value: MSB then LSB 
        value = self._conf.Shunt3Value >> 8
        self.write(REG_ADR_IDD_SHUNT3_MSB, value)
        value = self._conf.Shunt3Value
        self.write(REG_ADR_IDD_SHUNT3_LSB, value)

        # Shunt 4 register value: MSB then LSB 
        value = self._conf.Shunt4Value >> 8
        self.write(REG_ADR_IDD_SHUNT4_MSB, value)
        value = self._conf.Shunt4Value
        self.write(REG_ADR_IDD_SHUNT4_LSB, value)

        # Shunt 0 stabilization delay 
        value = self._config.Shunt0StabDelay
        self.write(REG_ADR_IDD_SH0_STABILIZATION, value)

        # Shunt 1 stabilization delay 
        value = self._config.Shunt1StabDelay
        self.write(REG_ADR_IDD_SH1_STABILIZATION, value)

        # Shunt 2 stabilization delay 
        value = self._config.Shunt2StabDelay
        self.write(REG_ADR_IDD_SH2_STABILIZATION, value)

        # Shunt 3 stabilization delay 
        value = self._config.Shunt3StabDelay
        self.write(REG_ADR_IDD_SH3_STABILIZATION, value)

        # Shunt 4 stabilization delay 
        value = self._config.Shunt4StabDelay
        self.write(REG_ADR_IDD_SH4_STABILIZATION, value)

        # Idd ampli gain value: MSB then LSB 
        value = self._conf.AmpliGain >> 8
        self.write(REG_ADR_IDD_GAIN_MSB, value)
        value = self._conf.AmpliGain
        self.write(REG_ADR_IDD_GAIN_LSB, value)

        # Idd VDD min value: MSB then LSB 
        value = self._conf.VddMin >> 8
        self.write(REG_ADR_IDD_VDD_MIN_MSB, value)
        value = self._conf.VddMin
        self.write(REG_ADR_IDD_VDD_MIN_LSB, value)

        # Idd number of measurements 
        value = self._config.MeasureNb
        self.write(REG_ADR_IDD_NBR_OF_MEAS, value)

        # Idd delta delay configuration: unit and value 
        value = (self._config.DeltaDelayUnit & IDD_DELTADELAY_UNIT) |\
                (self._config.DeltaDelayValue & IDD_DELTADELAY_VALUE)
        self.write(REG_ADR_IDD_MEAS_DELTA_DELAY, value)

        # Idd number of shut on board 
        value = self._config.ShuntNbOnBoard
        self.write(REG_ADR_IDD_SHUNTS_ON_BOARD, value)
        
    def gpio(self, pin_nr, value=None):
        pass
    
    
