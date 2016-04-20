# -*- coding: utf-8 -*-
REF_P_XL = const(0x08)
REF_P_L = const(0x09)
REF_P_H = const(0x0A)

RES_CONF = const(0x10)

CTRL_REG1_ADDR = const(0x20)
CTRL_REG2_ADDR = const(0x21)
CTRL_REG3_ADDR = const(0x22)
CTRL_REG4_ADDR = const(0x23) # 25H

STATUS_REG = const(0x27)

PRESS_OUT_XL = const(0x28)
PRESS_OUT_L = const(0x29)
PRESS_OUT_H = const(0x2A)

TEMP_OUT_L = const(0x2B)
TEMP_OUT_H = const(0x2C)

FIFO_CTRL = const(0x2E) # 25H
FIFO_STATUS = const(0x2F) # 25H

AMP_CTRL = const(0x30) # 331AP

RPDS_L = const(0x39) # 25H
RPDS_H = const(0x3A) # 25H

DELTA_PRESS_XL = const(0x3C) # 331AP
DELTA_PRESS_L = const(0x3D) # 331AP
DELTA_PRESS_H = const(0x3E) # 331AP


# dummy addresses for registers in different locations on different devices;
# the library translates these based on device type
# value with sign flipped is used as index into translated_regs array

INTERRUPT_CFG = const(-1)
INT_SOURCE = const(-2)
THS_P_L = const(-3)
THS_P_H = const(-4)
# update dummy_reg_count if registers are added here!


# device-specific register addresses

LPS331AP_INTERRUPT_CFG = const(0x23)
LPS331AP_INT_SOURCE = const(0x24)
LPS331AP_THS_P_L = const(0x25)
LPS331AP_THS_P_H = const(0x26)

LPS25H_INTERRUPT_CFG = const(0x24)
LPS25H_INT_SOURCE = const(0x25)
LPS25H_THS_P_L = const(0x30)
LPS25H_THS_P_H = const(0x31)

