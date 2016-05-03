LSM6DS3_XG_CTRL3_C = const(0x12)
LSM6DS3_XG_CTRL4_C = const(0x13)
LSM6DS3_XG_CTRL5_C = const(0x14)
LSM6DS3_XG_CTRL10_C = const(0x19)
LSM6DS3_XG_CTRL2_G = const(0x11)
LSM6DS3_XG_CTRL6_G = const(0x15)
LSM6DS3_XG_CTRL7_G = const(0x16)
LSM6DS3_XG_CTRL1_XL = const(0x10)
LSM6DS3_XG_CTRL8_XL = const(0x17)
LSM6DS3_XG_CTRL9_XL = const(0x18)

LSM6DS3_TEMP_OUT_L = const(0x20)

LSM6DS3_XG_IF_INC = const(0x04)
LSM6DS3_XG_IF_INC_MASK = const(0x04)

LSM6DS3_XG_FIFO_CTRL5=const(0x0A)
LSM6DS3_XG_FIFO_MODE={}
LSM6DS3_XG_FIFO_MODE['BYPASS'] = (0x00) # BYPASS Mode. FIFO turned off
LSM6DS3_XG_FIFO_MODE['FIFO'] = (0x01) # FIFO Mode. Stop collecting data when FIFO is full
LSM6DS3_XG_FIFO_MODE['CONTINUOUS_THEN_FIFO'] = (0x03) # CONTINUOUS mode until trigger is deasserted, then FIFO mode
LSM6DS3_XG_FIFO_MODE['BYPASS_THEN_CONTINUOUS'] = (0x04) # BYPASS mode until trigger is deasserted, then CONTINUOUS mode
LSM6DS3_XG_FIFO_MODE['CONTINUOUS_OVERWRITE'] = (0x05) # CONTINUOUS mode. If the FIFO is full the new sample overwrite the older one
LSM6DS3_XG_FIFO_MODE['MASK'] = (0x07)

LSM6DS3_XG_FIFO_ODR = {}
LSM6DS3_XG_FIFO_ODR['NA'] = (0x00) # FIFO ODR NA
LSM6DS3_XG_FIFO_ODR['10HZ'] = (0x08) # FIFO ODR 10Hz
LSM6DS3_XG_FIFO_ODR['25HZ'] = (0x10) # FIFO ODR 25Hz
LSM6DS3_XG_FIFO_ODR['50HZ'] = (0x18) # FIFO ODR 50Hz
LSM6DS3_XG_FIFO_ODR['100HZ'] = (0x20) # FIFO ODR 100Hz
LSM6DS3_XG_FIFO_ODR['200HZ'] = (0x28) # FIFO ODR 200Hz
LSM6DS3_XG_FIFO_ODR['400HZ'] = (0x30) # FIFO ODR 400Hz
LSM6DS3_XG_FIFO_ODR['800HZ'] = (0x38) # FIFO ODR 800Hz
LSM6DS3_XG_FIFO_ODR['1600HZ'] = (0x40) # FIFO ODR 1600Hz
LSM6DS3_XG_FIFO_ODR['3300HZ'] = (0x48) # FIFO ODR 3300Hz
LSM6DS3_XG_FIFO_ODR['6600HZ'] = (0x50) # FIFO ODR 6600Hz
LSM6DS3_XG_FIFO_ODR['MASK'] = (0x78)

LSM6DS3_XG_OUT_X_L_G = const(0x22)
LSM6DS3_XG_OUT_Y_L_G = const(0x24)
LSM6DS3_XG_OUT_Z_L_G = const(0x26)
LSM6DS3_G_ODR = {}
LSM6DS3_G_ODR['PD'] = (0x00) # Output Data Rate: Power-down
LSM6DS3_G_ODR['13HZ'] = (0x10) # Output Data Rate: 13 Hz
LSM6DS3_G_ODR['26HZ'] = (0x20) # Output Data Rate: 26 Hz
LSM6DS3_G_ODR['52HZ'] = (0x30) # Output Data Rate: 52 Hz
LSM6DS3_G_ODR['104HZ'] = (0x40) # Output Data Rate: 104 Hz
LSM6DS3_G_ODR['208HZ'] = (0x50) # Output Data Rate: 208 Hz
LSM6DS3_G_ODR['416HZ'] = (0x60) # Output Data Rate: 416 Hz
LSM6DS3_G_ODR['833HZ'] = (0x70) # Output Data Rate: 833 Hz
LSM6DS3_G_ODR['1K66HZ'] = (0x80) # Output Data Rate: 1.66 kHz
LSM6DS3_G_ODR['MASK'] = (0xF0)

LSM6DS3_G_FS = {}
LSM6DS3_G_FS['125'] = (0x02) # Full scale: 125 dps*/
LSM6DS3_G_FS['245'] = (0x00) # Full scale: 245 dps*/
LSM6DS3_G_FS['500'] = (0x04) # Full scale: 500 dps */
LSM6DS3_G_FS['1000'] = (0x08) # Full scale: 1000 dps */
LSM6DS3_G_FS['2000'] = (0x0C) # Full scale: 2000 dps */
LSM6DS3_G_FS['MASK'] = (0x0E)
LSM6DS3_G_FS['SHIFT'] = 1

LSM6DS3_G_AXIS_EN = {}
LSM6DS3_G_AXIS_EN['X'] = (0x08)
LSM6DS3_G_AXIS_EN['Y'] = (0x10)
LSM6DS3_G_AXIS_EN['Z'] = (0x20)
LSM6DS3_G_AXIS_EN['MASK'] = (0x38)

LSM6DS3_XG_OUT_X_L_XL = const(0x28)
LSM6DS3_XG_OUT_Y_L_XL = const(0x2A)
LSM6DS3_XG_OUT_Z_L_XL = const(0x2C)
LSM6DS3_XL_ODR = {}
LSM6DS3_XL_ODR['PD'] = (0x00) # Output Data Rate: Power-down*/
LSM6DS3_XL_ODR['13HZ'] = (0x10) # Output Data Rate: 13 Hz*/
LSM6DS3_XL_ODR['26HZ'] = (0x20) # Output Data Rate: 26 Hz*/
LSM6DS3_XL_ODR['52HZ'] = (0x30) # Output Data Rate: 52 Hz */
LSM6DS3_XL_ODR['104HZ'] = (0x40) # Output Data Rate: 104 Hz */
LSM6DS3_XL_ODR['208HZ'] = (0x50) # Output Data Rate: 208 Hz */
LSM6DS3_XL_ODR['416HZ'] = (0x60) # Output Data Rate: 416 Hz */
LSM6DS3_XL_ODR['833HZ'] = (0x70) # Output Data Rate: 833 Hz */
LSM6DS3_XL_ODR['1K66HZ'] = (0x80) # Output Data Rate: 1.66 kHz */
LSM6DS3_XL_ODR['3K33HZ'] = (0x90) # Output Data Rate: 3.33 kHz */
LSM6DS3_XL_ODR['6K66HZ'] = (0xA0) # Output Data Rate: 6.66 kHz */
LSM6DS3_XL_ODR['MASK'] = (0xF0)

LSM6DS3_XL_FS = {}
LSM6DS3_XL_FS['2G'] = (0x00) # Full scale: +- 2g */
LSM6DS3_XL_FS['4G'] = (0x08) # Full scale: +- 4g */
LSM6DS3_XL_FS['8G'] = (0x0C) # Full scale: +- 8g */
LSM6DS3_XL_FS['16G'] = (0x04) # Full scale: +- 16g */
LSM6DS3_XL_FS['MASK'] = (0x0C)
LSM6DS3_XL_FS['SHIFT'] = 3

LSM6DS3_XL_AXIS_EN = {}
LSM6DS3_XL_AXIS_EN['X'] = (0x08)
LSM6DS3_XL_AXIS_EN['Y'] = (0x10)
LSM6DS3_XL_AXIS_EN['Z'] = (0x20)
LSM6DS3_XL_AXIS_EN['MASK'] = (0x38)
