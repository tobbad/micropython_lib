#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Class to measure current on the l476 discoverz
    Created on 2.6.2018
    @author: Tobias Badertscher

"""

class IDD_DEFAULT:
    
    def __init__(self, revision='c'):
        self._rev = revision
    
    @property
    def AmpliGain(self):
        if self._rev == 'c':
            return 4967
        else:
            return 4990
        
    IDD_SHUNT0_VALUE = 1000  # value in milliohm 
    IDD_SHUNT1_VALUE = 24    # value in ohm 
    IDD_SHUNT2_VALUE = 620   # value in ohm 
    IDD_SHUNT4_VALUE = 10000 # value in ohm 
    #
    # Shunt stabilization delay on discovery in milli ohms
    #
    IDD_SHUNT0_STABDELAY = 149 # value in millisec
    IDD_SHUNT1_STABDELAY = 149 # value in millisec
    IDD_SHUNT2_STABDELAY = 149 # value in millisec
    IDD_SHUNT4_STABDELAY = 255 # value in millisec
    #
    # IDD Vdd Min on discovery
    # 
    IDD_VDD_MIN = 2000 # value in millivolt 
    # 
    # IDD Shunt Number
    # 
    IDD_SHUNT_NB_1 = 0x01
    IDD_SHUNT_NB_2 = 0x02
    IDD_SHUNT_NB_3 = 0x03
    IDD_SHUNT_NB_4 = 0x04
    IDD_SHUNT_NB_5 = 0x05

    # 
    # Vref Measurement
    # 
    IDD_VREF_AUTO_MEASUREMENT_ENABLE  = 0x00
    IDD_VREF_AUTO_MEASUREMENT_DISABLE = 0x70

    # 
    # IDD Calibration
    # 
    IDD_AUTO_CALIBRATION_ENABLE = 0x00
    IDD_AUTO_CALIBRATION_DISABLE = 0x80
    # 
    # IDD PreDelay masks
    # 
    IDD_PREDELAY_UNIT  = 0x80
    IDD_PREDELAY_VALUE = 0x7F
    # 
    # IDD PreDelay unit
    # 
    IDD_PREDELAY_0_5_MS = 0x00
    IDD_PREDELAY_20_MS  = 0x80
    # 
    # IDD Delta Delay masks
    # 
    IDD_DELTADELAY_UNIT  = 0x80
    IDD_DELTADELAY_VALUE = 0x7F
    # 
    # IDD Delta Delay unit
    # 
    IDD_DELTADELAY_0_5_MS = 0x00
    IDD_DELTADELAY_20_MS  = 0x80
    # 
    # Here comes the config
    #        
    VddMin = IDD_VDD_MIN;
    Shunt0Value = IDD_SHUNT0_VALUE;
    Shunt1Value = IDD_SHUNT1_VALUE;
    Shunt2Value = IDD_SHUNT2_VALUE;
    Shunt3Value = 0;
    Shunt4Value = IDD_SHUNT4_VALUE;
    Shunt0StabDelay = IDD_SHUNT0_STABDELAY;
    Shunt1StabDelay = IDD_SHUNT1_STABDELAY;
    Shunt2StabDelay = IDD_SHUNT2_STABDELAY;
    Shunt3StabDelay = 0;
    Shunt4StabDelay = IDD_SHUNT4_STABDELAY;
    ShuntNbOnBoard = IDD_SHUNT_NB_4;
    ShuntNbUsed = IDD_SHUNT_NB_4;
    VrefMeasurement = IDD_VREF_AUTO_MEASUREMENT_ENABLE;
    Calibration = IDD_AUTO_CALIBRATION_ENABLE;
    PreDelayUnit = IDD_PREDELAY_20_MS;
    PreDelayValue = 0x7F;
    MeasureNb = 100;
    DeltaDelayUnit = IDD_DELTADELAY_0_5_MS;
    DeltaDelayValue = 10;
    