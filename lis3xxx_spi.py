"""
Driver for accelerometer on STM32F4 Discover board.

Sets accelerometer range at +-2g.
Returns list containing X,Y,Z axis acceleration values in 'g' units (9.8m/s^2).

See:
    STM32Cube_FW_F4_V1.1.0/Drivers/BSP/Components/lis302dl/lis302dl.h
    STM32Cube_FW_F4_V1.1.0/Drivers/BSP/Components/lis302dl/lis302dl.c
    STM32Cube_FW_F4_V1.1.0/Drivers/BSP/STM32F4-Discovery/stm32f4_discovery.c
    STM32Cube_FW_F4_V1.1.0/Drivers/BSP/STM32F4-Discovery/stm32f4_discovery.h
    STM32Cube_FW_F4_V1.1.0/Drivers/BSP/STM32F4-Discovery/stm32f4_discovery_accelerometer.c
    STM32Cube_FW_F4_V1.1.0/Drivers/BSP/STM32F4-Discovery/stm32f4_discovery_accelerometer.h
    STM32Cube_FW_F4_V1.1.0/Projects/STM32F4-Discovery/Demonstrations/Src/main.c
"""

from i2cspi import COM_SPI
from multibyte import multibyte

READWRITE_CMD = const(0x80)
MULTIPLEBYTE_CMD = const(0x40)
OUT_X_ADDR = const(0x29)
OUT_Y_ADDR = const(0x2b)
OUT_Z_ADDR = const(0x2d)
OUT_T_ADDR = const(0x0c)

LIS302DL_WHO_AM_I_VAL = const(0x3b)
LIS302DL_CTRL_REG1_ADDR = const(0x20)
# Configuration for 100Hz sampling rate, +-2g range
LIS302DL_CONF = const(0b01000111)

LIS3DSH_WHO_AM_I_VAL = const(0x3f)
LIS3DSH_CTRL_REG4_ADDR = const(0x20)
LIS3DSH_CTRL_REG5_ADDR = const(0x24)
# Configuration for 100Hz sampling rate, +-2g range
LIS3DSH_CTRL_REG4_CONF = const(0b01100111)
LIS3DSH_CTRL_REG5_CONF = const(0b00000000)


class LIS3XXX(COM_SPI, multibyte):

    def __init__(self, communication, dev_selector):
        super(LIS302DL, self).__init__(communication, dev_selector)
        self.init()

    def x(self):
        return self.read_s8(OUT_X_ADDR, 1)*self.sensitivity

    def y(self):
        return self.read_s8(OUT_Y_ADDR, 1)*self.sensitivity

    def z(self):
        return self.read_s8(OUT_Z_ADDR, 1)*self.sensitivity

    def xyz(self):
        return (self.x(), self.y(), self.z())


class LIS3DSH(LIS3XXX):

    WHO_IAM_REG = 0x0F
    WHO_IAM_ANSWER = LIS3DSH_WHO_AM_I_VAL

    DEFAULT_CONF = ((LIS3DSH_CTRL_REG4_ADDR, LIS3DSH_CTRL_REG4_CONF),
                    (LIS3DSH_CTRL_REG5_ADDR, LIS3DSH_CTRL_REG5_CONF))

    def __init__(self, communication, dev_selector):
        super(LIS3DSH, self).__init__(communication, dev_selector)
        self.sensitivity = 0.06 * 256/1000


class LIS302DL(LIS3XXX):

    WHO_IAM_REG = 0x0F
    WHO_IAM_ANSWER = LIS302DL_WHO_AM_I_VAL

    DEFAULT_CONF = ((LIS302DL_CTRL_REG1_ADDR, LIS302DL_CONF),)

    def __init__(self, communication, dev_selector):
        super(LIS302DL, self).__init__(communication, dev_selector)
        self.sensitivity = 18.0/1000
