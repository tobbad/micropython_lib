# XL = Linear Accleration
# G = Gyro/Angular rate
#

#
# Angular rate control register
#
LSM9DS1_CTRL1_G = const(0x10)
LSM9DS1_CTRL1_G_ODR = {}
LSM9DS1_CTRL1_G_ODR['PD'] =   (0x00)  # Output Data Rate: Power-down
LSM9DS1_CTRL1_G_ODR['14HZ9'] = (0x20)  
LSM9DS1_CTRL1_G_ODR['59HZ5'] = (0x40)  
LSM9DS1_CTRL1_G_ODR['119HZ'] = (0x60) 
LSM9DS1_CTRL1_G_ODR['238HZ'] = (0x80) 
LSM9DS1_CTRL1_G_ODR['476HZ'] = (0xA0) 
LSM9DS1_CTRL1_G_ODR['952HZ'] = (0xC0) 
LSM9DS1_CTRL1_G_ODR['MASK'] = (0xE0)
LSM9DS1_CTRL1_G_ODR['SHIFT'] = (5)

LSM9DS1_CTRL1_G_FS = {}
LSM9DS1_CTRL1_G_FS['245'] = (0x00)  # Full scale: 245 dps*/
LSM9DS1_CTRL1_G_FS['500'] = (0x08)  # Full scale: 500 dps */
LSM9DS1_CTRL1_G_FS['2000'] = (0x18)  # Full scale: 2000 dps */
LSM9DS1_CTRL1_G_FS['MASK'] = (0x18)
LSM9DS1_CTRL1_G_FS['MAP'] = (245.0, 500.0, -1, 2000.0)
LSM9DS1_CTRL1_G_FS['SHIFT'] = (3)

LSM9DS1_CTRL2_G = const(0x11)

LSM9DS1_CTRL3_G = const(0x12)
LSM9DS1_ORIENT_CFG_G = const(0x13)
LSM9DS1_INT_GEN_SRC_G = const(0x14)
#
# Temperatuer measurement (16 bits)
#
LSM9DS1_TEMP_OUT_L = const(0x15)
#
# Status Register
#
LSM9DS1_STATUS_REG1 = const(0x17)
#
# Angular rate out register
# (each 16 bits)
#
LSM9DS1_OUT_X_G_L = const(0x18)
LSM9DS1_OUT_Y_G_L = const(0x1A)
LSM9DS1_OUT_Z_G_L = const(0x1C)
#
# Control register
#
LSM9DS1_CTRL4 = const(0x1E)
LSM9DS1_CTRL4_G_AXIS_EN = {}
LSM9DS1_CTRL4_G_AXIS_EN['X'] = (0x08)
LSM9DS1_CTRL4_G_AXIS_EN['Y'] = (0x10)
LSM9DS1_CTRL4_G_AXIS_EN['Z'] = (0x20)
LSM9DS1_CTRL4_G_AXIS_EN['MASK'] = (0x38)

#
# Linear Acceleration control register
#
LSM9DS1_CTRL5_XL = const(0x1F)
LSM9DS1_CTRL5_XL_AXIS_EN = {}
LSM9DS1_CTRL5_XL_AXIS_EN['X'] = (0x08)
LSM9DS1_CTRL5_XL_AXIS_EN['Y'] = (0x10)
LSM9DS1_CTRL5_XL_AXIS_EN['Z'] = (0x20)
LSM9DS1_CTRL5_XL_AXIS_EN['MASK'] = (0x38)
LSM9DS1_CTRL6_XL = const(0x20)
LSM9DS1_CTRL6_XL_ODR = {}
LSM9DS1_CTRL6_XL_ODR['PD']    = (0x00)  # Output Data Rate: Power-down*/
LSM9DS1_CTRL6_XL_ODR['10HZ']  = (0x20)  # Output Data Rate*/
LSM9DS1_CTRL6_XL_ODR['50HZ']  = (0x40)  # Output Data Rate */
LSM9DS1_CTRL6_XL_ODR['119HZ'] = (0x60)  # Output Data Rate */
LSM9DS1_CTRL6_XL_ODR['238HZ'] = (0x80)  # Output Data Rate */
LSM9DS1_CTRL6_XL_ODR['476HZ'] = (0xA0)  # Output Data Rate */
LSM9DS1_CTRL6_XL_ODR['952HZ'] = (0xE0)  # Output Data Rate */
LSM9DS1_CTRL6_XL_ODR['MASK']  = (0xE0)
LSM9DS1_CTRL6_XL_FS = {}
LSM9DS1_CTRL6_XL_FS['2G'] = (0x00)  # Full scale: +- 2g */
LSM9DS1_CTRL6_XL_FS['4G'] = (0x10)  # Full scale: +- 4g */
LSM9DS1_CTRL6_XL_FS['8G'] = (0x18)  # Full scale: +- 8g */
LSM9DS1_CTRL6_XL_FS['16G'] = (0x08) # Full scale: +- 16g */
LSM9DS1_CTRL6_XL_FS['MASK'] = (0x18)
LSM9DS1_CTRL6_XL_FS['SHIFT'] = (0x3)
LSM9DS1_CTRL6_XL_FS['MAP'] = (2.0, 16.0, 4.0, 8.0)
LSM9DS1_CTRL7_XL = const(0x21)
#
# Control register
#
LSM9DS1_CTRL8 = const(0x22)
LSM9DS1_CTRL8_BDU = const(0x40)
LSM9DS1_CTRL8_IF_ADD_INC = const(0x04)
LSM9DS1_CTRL9 = const(0x23)
LSM9DS1_CTRL10 = const(0x24)
#
# Linear Acceleration interrupt generation
#
LSM9DS1_INT_GEN_SRC_XL = const(0x26)
#
# Status Register
#
LSM9DS1_STATUS_REG2 = const(0x27)
#
# Linear Acceleration out register
# (each 16 bits)
#
LSM9DS1_OUT_X_L_XL = const(0x28)
LSM9DS1_OUT_Y_L_XL = const(0x2A)
LSM9DS1_OUT_Z_L_XL = const(0x2C)
#
# FIFO Control
#
LSM9DS1_FIFO_CTRL = const(0x2E)
LSM9DS1_FIFO_SRC = const(0x2F)
LSM9DS1_FIFO_MODE = {}
LSM9DS1_FIFO_MODE['SHIFT'] = (0x05)
LSM9DS1_FIFO_MODE['BYPASS'] = (0x00<<LSM9DS1_FIFO_MODE['SHIFT'])  # BYPASS Mode. FIFO turned off
# FIFO Mode. Stop collecting data when FIFO is full
LSM9DS1_FIFO_MODE['FIFO'] = (0x01<<LSM9DS1_FIFO_MODE['SHIFT'])
# CONTINUOUS mode until trigger is deasserted, then FIFO mode
LSM9DS1_FIFO_MODE['CONTINUOUS_THEN_FIFO'] = (0x03<<LSM9DS1_FIFO_MODE['SHIFT'])
# BYPASS mode until trigger is deasserted, then CONTINUOUS mode
LSM9DS1_FIFO_MODE['BYPASS_THEN_CONTINUOUS'] = (0x04<<LSM9DS1_FIFO_MODE['SHIFT'])
# CONTINUOUS mode. If the FIFO is full the new sample overwrite the older one
LSM9DS1_FIFO_MODE['CONTINUOUS_OVERWRITE'] = (0x05<<LSM9DS1_FIFO_MODE['SHIFT'])
LSM9DS1_FIFO_MODE['MASK'] = (0x07<<LSM9DS1_FIFO_MODE['SHIFT'])
#
# Angular rate interrupt generation
#
LSM9DS1_INT_GEN_CFG_G = const(0x30)
#
# Angular rate interrupt generation thresholds
#
LSM9DS1_INT_GEN_THS_X_G = const(0x31)
LSM9DS1_INT_GEN_THS_Y_G = const(0x33)
LSM9DS1_INT_GEN_THS_Z_G = const(0x35)
LSM9DS1_INT_GEN_DUR = const(0x37)
#
# Magneto sensor
#
LSM9DS1_OFFSET_X_REG_L_M = const(0x06)
LSM9DS1_OFFSET_Y_REG_L_M = const(0x08)
LSM9DS1_OFFSET_Z_REG_L_M = const(0x0A)
LSM9DS1_CTRL_REG1_M = const(0x20)
LSM9DS1_CTRL_REG1_M_ODR = {}
LSM9DS1_CTRL_REG1_M_ODR['HZ625'] = (0x00)  # Output Data Rate: Power-down*/
LSM9DS1_CTRL_REG1_M_ODR['1HZ25'] = (0x04)  # Output Data Rate*/
LSM9DS1_CTRL_REG1_M_ODR['2HZ5']  = (0x08)  # Output Data Rate */
LSM9DS1_CTRL_REG1_M_ODR['5HZ']  = (0x0C)  # Output Data Rate */
LSM9DS1_CTRL_REG1_M_ODR['10HZ'] = (0x10)  # Output Data Rate */
LSM9DS1_CTRL_REG1_M_ODR['20HZ'] = (0x14)  # Output Data Rate */
LSM9DS1_CTRL_REG1_M_ODR['40HZ'] = (0x18)  # Output Data Rate */
LSM9DS1_CTRL_REG1_M_ODR['80HZ'] = (0x1C)  # Output Data Rate */
LSM9DS1_CTRL_REG1_M_ODR['MASK']  = (0x1C)

LSM9DS1_CTRL_REG2_M = const(0x21)
LSM9DS1_CTRL_REG2_M_FS = {}
LSM9DS1_CTRL_REG2_M_FS['4G'] = (0x00)  # Full scale: +- 2g */
LSM9DS1_CTRL_REG2_M_FS['8G'] = (0x20)  # Full scale: +- 4g */
LSM9DS1_CTRL_REG2_M_FS['12G'] = (0x40)  # Full scale: +- 8g */
LSM9DS1_CTRL_REG2_M_FS['16G'] = (0x60) # Full scale: +- 16g */
LSM9DS1_CTRL_REG2_M_FS['MASK'] = (0x60)
LSM9DS1_CTRL_REG2_M_FS['SHIFT'] = (5)
LSM9DS1_CTRL_REG2_M_FS['MAP'] = (4.0, 8.0, 12.0, 16.0)
LSM9DS1_CTRL_REG3_M = const(0x22)
LSM9DS1_CTRL_REG3_M_CONV_MODE = {}
LSM9DS1_CTRL_REG3_M_CONV_MODE['CONTINUOUS'] = (0x00)  
LSM9DS1_CTRL_REG3_M_CONV_MODE['SINGLE'] = (0x01)  
LSM9DS1_CTRL_REG3_M_CONV_MODE['PD'] = (0x02)  
LSM9DS1_CTRL_REG3_M_CONV_MODE['PD1'] = (0x03)  
LSM9DS1_CTRL_REG3_M_CONV_MODE['MASK'] = (0x03)  

LSM9DS1_CTRL_REG4_M = const(0x23)
LSM9DS1_CTRL_REG5_M = const(0x24)
LSM9DS1_CTRL_REG5_M_BDU = const(0x40)
LSM9DS1_CTRL_REG5_M_IF_ADD_INC = const(0x04)
LSM9DS1_STATUS_REG_M = const(0x27)
LSM9DS1_OUT_X_L_M = const(0x28)
LSM9DS1_OUT_Y_L_M = const(0x2A)
LSM9DS1_OUT_Z_L_M = const(0x2C)
LSM9DS1_INT_CFG_M = const(0x30)
LSM9DS1_INT_SRC_M = const(0x31)
LSM9DS1_INT_THS_L_M = const(0x32)
