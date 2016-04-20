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

from pyb import Pin
from pyb import I2C
import pyb 

READ_CMD = const(0x01) 
MULTIPLEBYTE_CMD = const(0x80)
WHO_AM_I_ADDR = const(0x0f)
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

class STAccel:
    
    __I2CADDR = 0x38
    debug = False
    
    def __init__(self):
        # Choos i2c address 
        self.i2cAddr = pyb.Pin('PA6', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
        self.i2cAddr.low()
        #self.conf = pyb.Pin('PE3', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
        #self.conf.high()
        
        self.i2c = pyb.I2C(1, pyb.I2C.MASTER)
        print(self.i2c.scan())
        self.who_am_i = self.read_id()

        if self.who_am_i == LIS302DL_WHO_AM_I_VAL:
            self.write_bytes(LIS302DL_CTRL_REG1_ADDR, bytearray([LIS302DL_CONF]))
            self.sensitivity = 18
        elif self.who_am_i == LIS3DSH_WHO_AM_I_VAL:
            self.write_bytes(LIS3DSH_CTRL_REG4_ADDR, bytearray([LIS3DSH_CTRL_REG4_CONF]))
            self.write_bytes(LIS3DSH_CTRL_REG5_ADDR, bytearray([LIS3DSH_CTRL_REG5_CONF]))
            self.sensitivity = 0.06 * 256
        else:
            raise Exception('LIS302DL or LIS3DSH accelerometer not present')

    def __buf2Str(self, buf):
        return " ".join(["0x%02x" % i for i in buf])

    def convert_raw_to_g(self, x):
        if x & 0x80:
            x = x - 256
        return x * self.sensitivity / 1000

    def read_bytes(self, reg_addr, nbytes):
        i2c_addr = self.__I2CADDR | READ_CMD
        if nbytes > 1:
            reg_addr |=  MULTIPLEBYTE_CMD
        self.i2c.send(reg_addr, addr = self.__I2CADDR)
        buf = self.i2c.recv(nbytes, addr = i2c_addr)
        if self.debug:
            print("Read I2C(0x%02x) Reg 0x%02x: %s" % (i2c_addr, reg_addr, self.__buf2Str(buf)))
        return buf

    def write_bytes(self, reg_addr, buf):
        if len(buf) > 1:
            reg_addr |= MULTIPLEBYTE_CMD
        self.i2c.send(reg_addr, addr = self.__I2CADDR)
        for b in buf:
            self.i2c.send(b, addr = self.__I2CADDR)
        if self.debug:
            print("Wrote I2C(0x%02x) Reg 0x%02x: %s" % (self.__I2CADDR, reg_addr, self.__buf2Str(buf)))

    def read_id(self):
        return self.read_bytes(WHO_AM_I_ADDR, 1)[0]

    def x(self):
        return self.convert_raw_to_g(self.read_bytes(OUT_X_ADDR, 1)[0])

    def y(self):
        return self.convert_raw_to_g(self.read_bytes(OUT_Y_ADDR, 1)[0])

    def z(self):
        return self.convert_raw_to_g(self.read_bytes(OUT_Z_ADDR, 1)[0])

    def xyz(self):
        return (self.x(), self.y(), self.z())
