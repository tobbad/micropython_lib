LSM303C_WHO_AM_I_ADDR = const(0x0F)  # device identification register
LSM303C_ACT_THS_A = const(0x1E)
LSM303C_ACT_DUR_A = const(0x1F)
LSM303C_CTRL_REG1_A = const(0x20)  # Control register 1 acceleration
LSM303C_CTRL_REG2_A = const(0x21)  # Control register 2 acceleration
LSM303C_CTRL_REG3_A = const(0x22)  # Control register 3 acceleration
LSM303C_CTRL_REG4_A = const(0x23)  # Control register 4 acceleration
LSM303C_CTRL_REG5_A = const(0x24)  # Control register 5 acceleration
LSM303C_CTRL_REG6_A = const(0x25)  # Control register 6 acceleration
LSM303C_CTRL_REG7_A = const(0x26)  # Control register 6 acceleration
LSM303C_STATUS_REG_A = const(0x27)  # Status register acceleration
LSM303C_OUT_X_L_A = const(0x28)  # Output Register X acceleration
LSM303C_OUT_X_H_A = const(0x29)  # Output Register X acceleration
LSM303C_OUT_Y_L_A = const(0x2A)  # Output Register Y acceleration
LSM303C_OUT_Y_H_A = const(0x2B)  # Output Register Y acceleration
LSM303C_OUT_Z_L_A = const(0x2C)  # Output Register Z acceleration
LSM303C_OUT_Z_H_A = const(0x2D)  # Output Register Z acceleration
LSM303C_FIFO_CTRL = const(0x2E)  # Fifo control Register acceleration
LSM303C_FIFO_SRC = const(0x2F)  # Fifo src Register acceleration
# Interrupt 1 configuration Register acceleration
LSM303C_IG_CFG1_A = const(0x30)
LSM303C_IG_SRC1_A = const(0x31)  # Interrupt 1 source Register acceleration
LSM303C_IG_THS_X1_A = const(0x32)
LSM303C_IG_THS_Y1_A = const(0x33)
LSM303C_IG_THS_Z1_A = const(0x34)
LSM303C_IG_DUR1_A = const(0x32)
# Interrupt 1 DURATION register acceleration
LSM303C_INT1_DURATION_A = const(0x33)
# Interrupt 2 configuration Register acceleration
LSM303C_INT2_CFG_A = const(0x34)
LSM303C_INT2_SOURCE_A = const(0x35)  # Interrupt 2 source Register acceleration
LSM303C_INT2_THS_A = const(0x36)  # Interrupt 2 Threshold register acceleration
# Interrupt 2 DURATION register acceleration
LSM303C_INT2_DURATION_A = const(0x37)
LSM303C_CLICK_CFG_A = const(0x38)  # Click configuration Register acceleration
LSM303C_CLICK_SOURCE_A = const(0x39)  # Click 2 source Register acceleration
LSM303C_CLICK_THS_A = const(0x3A)  # Click 2 Threshold register acceleration
LSM303C_TIME_LIMIT_A = const(0x3B)  # Time Limit Register acceleration
LSM303C_TIME_LATENCY_A = const(0x3C)  # Time Latency Register acceleration
LSM303C_TIME_WINDOW_A = const(0x3D)  # Time window register acceleration
LSM303C_CTRL_REG1_M = const(0x20)  # Magnetic control register 1
LSM303C_CTRL_REG2_M = const(0x21)  # Magnetic control register 2
LSM303C_CTRL_REG3_M = const(0x22)  # Magnetic control register 3
LSM303C_CTRL_REG4_M = const(0x23)  # Magnetic control register 4
LSM303C_CTRL_REG5_M = const(0x24)  # Magnetic control register 5
LSM303C_STATUS_REG_M = const(0x27)  # Magnetic status register M
LSM303C_OUT_X_L_M = const(0x28)  # Output Register X magnetic field
LSM303C_OUT_X_H_M = const(0x29)  # Output Register X magnetic field
LSM303C_OUT_Y_L_M = const(0x2A)  # Output Register Y magnetic field
LSM303C_OUT_Y_H_M = const(0x2B)  # Output Register Y magnetic field
LSM303C_OUT_Z_L_M = const(0x2C)  # Output Register Z magnetic field
LSM303C_OUT_Z_H_M = const(0x2D)  # Output Register Z magnetic field
LSM303C_TEMP_OUT_L_M = const(0x2E)  # Temperature Register magnetic field
LSM303C_TEMP_OUT_H_M = const(0x2F)  # Temperature Register magnetic field
LSM303C_INT_CFG_M = const(0x30)  # Axis interrupt configuration
LSM303C_INT_SRC_M = const(0x31)  # Axis interrupt source
LSM303C_INT_THS_L_M = const(0x32)  # Interrupt threshold L
LSM303C_INT_THS_H_M = const(0x33)  # Interrupt threshold M
LMS303C_ACC_ID = const(0x41)
LMS303C_MAG_ID = const(0x3D)
LSM303C_ACC_ODR_BITPOSITION = const(0x70)  # Output Data Rate bit position
LSM303C_ACC_ODR_OFF = const(0x00)  # Output Data Rate powerdown
LSM303C_ACC_ODR_10_HZ = const(0x10)  # Output Data Rate = 10 Hz
LSM303C_ACC_ODR_50_HZ = const(0x20)  # Output Data Rate = 50 Hz
LSM303C_ACC_ODR_100_HZ = const(0x30)  # Output Data Rate = 100 Hz
LSM303C_ACC_ODR_200_HZ = const(0x40)  # Output Data Rate = 200 Hz
LSM303C_ACC_ODR_400_HZ = const(0x50)  # Output Data Rate = 400 Hz
LSM303C_ACC_ODR_800_HZ = const(0x60)  # Output Data Rate = 800 Hz
LSM303C_ACC_X_ENABLE = const(0x01)
LSM303C_ACC_Y_ENABLE = const(0x02)
LSM303C_ACC_Z_ENABLE = const(0x04)
LSM303C_ACC_AXES_ENABLE = const(0x07)
LSM303C_ACC_AXES_DISABLE = const(0x00)
LSM303C_ACC_HR_ENABLE = const(0x80)
LSM303C_ACC_HR_DISABLE = const(0x00)
LSM303C_ACC_I2C_MODE = const(0x02)
LSM303C_ACC_SPI_MODE = const(0x01)
LSM303C_ACC_FULLSCALE_2G = const(0x00)  # �2 g
LSM303C_ACC_FULLSCALE_4G = const(0x20)  # �4 g
LSM303C_ACC_FULLSCALE_8G = const(0x30)  # �8 g
LSM303C_ACC_BDU_CONTINUOUS = const(0x00)  # Continuos Update
# Single Update: output registers not updated until MSB and LSB reading
LSM303C_ACC_BDU_MSBLSB = const(0x08)
LSM303C_ACC_BLE_LSB = const(0x00)  # Little Endian: data LSB @ lower address
LSM303C_ACC_BLE_MSB = const(0x40)  # Big Endian: data MSB @ lower address
LSM303C_ACC_HPM_REF_SIGNAL = const(0x08)
LSM303C_ACC_HPM_NORMAL_MODE = const(0x00)
LSM303C_ACC_DFC1_ODRDIV50 = const(0x00)
LSM303C_ACC_DFC1_ODRDIV100 = const(0x20)
LSM303C_ACC_DFC1_ODRDIV9 = const(0x40)
LSM303C_ACC_DFC1_ODRDIV400 = const(0x60)
LSM303C_ACC_HPF_DISABLE = const(0x00)
LSM303C_ACC_HPF_ENABLE = const(0x08)
LSM303C_ACC_HPF_CLICK_DISABLE = const(0x00)
LSM303C_ACC_HPF_CLICK_ENABLE = const(0x04)
LSM303C_ACC_HPI2S_INT1_DISABLE = const(0x00)
LSM303C_ACC_HPI2S_INT1_ENABLE = const(0x01)
LSM303C_ACC_HPI2S_INT2_DISABLE = const(0x00)
LSM303C_ACC_HPI2S_INT2_ENABLE = const(0x02)
LSM303C_ACC_SOFT_RESET_DEFAULT = const(0x00 << 6)
LSM303C_ACC_SOFT_RESET_ENABLE = const(0x01 << 6)
LSM303C_IT1_CLICK = const(0x80)
LSM303C_IT1_AOI1 = const(0x40)
LSM303C_IT1_AOI2 = const(0x20)
LSM303C_IT1_DRY1 = const(0x10)
LSM303C_IT1_DRY2 = const(0x08)
LSM303C_IT1_WTM = const(0x04)
LSM303C_IT1_OVERRUN = const(0x02)
LSM303C_IT2_CLICK = const(0x80)
LSM303C_IT2_INT1 = const(0x40)
LSM303C_IT2_INT2 = const(0x20)
LSM303C_IT2_BOOT = const(0x10)
LSM303C_IT2_ACT = const(0x08)
LSM303C_IT2_HLACTIVE = const(0x02)
LSM303C_OR_COMBINATION = const(0x00)  # OR combination of enabled IRQs
LSM303C_AND_COMBINATION = const(0x80)  # AND combination of enabled IRQs
LSM303C_MOV_RECOGNITION = const(0x40)  # 6D movement recognition
LSM303C_POS_RECOGNITION = const(0xC0)  # 6D position recognition
LSM303C_Z_HIGH = const(0x20)  # Z High enabled IRQs
LSM303C_Z_LOW = const(0x10)  # Z low enabled IRQs
LSM303C_Y_HIGH = const(0x08)  # Y High enabled IRQs
LSM303C_Y_LOW = const(0x04)  # Y low enabled IRQs
LSM303C_X_HIGH = const(0x02)  # X High enabled IRQs
LSM303C_X_LOW = const(0x01)  # X low enabled IRQs
LSM303C_Z_DOUBLE_CLICK = const(0x20)  # Z double click IRQs
LSM303C_Z_SINGLE_CLICK = const(0x10)  # Z single click IRQs
LSM303C_Y_DOUBLE_CLICK = const(0x08)  # Y double click IRQs
LSM303C_Y_SINGLE_CLICK = const(0x04)  # Y single click IRQs
LSM303C_X_DOUBLE_CLICK = const(0x02)  # X double click IRQs
LSM303C_X_SINGLE_CLICK = const(0x01)  # X single click IRQs
LSM303C_INT1INTERRUPT_DISABLE = const(0x00)
LSM303C_INT1INTERRUPT_ENABLE = const(0x80)
LSM303C_INT1INTERRUPT_LOW_EDGE = const(0x20)
LSM303C_INT1INTERRUPT_HIGH_EDGE = const(0x00)
LSM303C_MAG_TEMPSENSOR_ENABLE = const(0x80)  # Temp sensor Enable
LSM303C_MAG_TEMPSENSOR_DISABLE = const(0x00)  # Temp sensor Disable
LSM303C_MAG_OM_XY_LOWPOWER = const(0x00 << 5)
LSM303C_MAG_OM_XY_MEDIUM = const(0x01 << 5)
LSM303C_MAG_OM_XY_HIGH = const(0x02 << 5)
LSM303C_MAG_OM_XY_ULTRAHIGH = const(0x03 << 5)
LSM303C_MAG_ODR_0_625_HZ = const(0x00 << 2)  # Output Data Rate = 0.625 Hz
LSM303C_MAG_ODR_1_25_HZ = const(0x01 << 2)  # Output Data Rate = 1.25 Hz
LSM303C_MAG_ODR_2_5_HZ = const(0x02 << 2)  # Output Data Rate = 2.5 Hz
LSM303C_MAG_ODR_5_0_HZ = const(0x03 << 2)  # Output Data Rate = 5.0 Hz
LSM303C_MAG_ODR_10_HZ = const(0x04 << 2)  # Output Data Rate = 10 Hz
LSM303C_MAG_ODR_20_HZ = const(0x05 << 2)  # Output Data Rate = 20 Hz
LSM303C_MAG_ODR_40_HZ = const(0x06 << 2)  # Output Data Rate = 40 Hz
LSM303C_MAG_ODR_80_HZ = const(0x07 << 2)  # Output Data Rate = 80 Hz
LSM303C_MAG_FS_DEFAULT = const(0x00 << 5)
LSM303C_MAG_FS_16_GA = const(0x03 << 5)  # Full scale = 16 Gauss
LSM303C_MAG_REBOOT_DEFAULT = const(0x00 << 3)
LSM303C_MAG_REBOOT_ENABLE = const(0x01 << 3)
LSM303C_MAG_SOFT_RESET_DEFAULT = const(0x00 << 2)
LSM303C_MAG_SOFT_RESET_ENABLE = const(0x01 << 2)
LSM303C_MAG_I2C_MODE = const(0x80)
LSM303C_MAG_SPI_MODE = const(0x04)
LSM303C_MAG_CONFIG_NORMAL_MODE = const(0x00)
LSM303C_MAG_CONFIG_LOWPOWER_MODE = const(0x20)
LSM303C_MAG_SELECTION_MODE = const(0x03)
LSM303C_MAG_CONTINUOUS_MODE = const(0x00)
LSM303C_MAG_SINGLE_MODE = const(0x01)
LSM303C_MAG_POWERDOWN1_MODE = const(0x02)
LSM303C_MAG_POWERDOWN2_MODE = const(0x03)
LSM303C_MAG_OM_Z_LOWPOWER = const(0x00 << 2)
LSM303C_MAG_OM_Z_MEDIUM = const(0x01 << 2)
LSM303C_MAG_OM_Z_HIGH = const(0x02 << 2)
LSM303C_MAG_OM_Z_ULTRAHIGH = const(0x03 << 2)
LSM303C_MAG_BLE_LSB = const(0x00)
LSM303C_MAG_BLE_MSB = const(0x02)
LSM303C_MAG_BDU_CONTINUOUS = const(0x00)
LSM303C_MAG_BDU_MSBLSB = const(0x40)

# Magnetometer Sensitivity for XY Axes
LSM303C_M_SENSITIVITY_XY_1_3Ga = const(1100)  # 1.3 Ga full scale [LSB/Ga]
LSM303C_M_SENSITIVITY_XY_1_9Ga = const(855)  # 1.9 Ga full scale [LSB/Ga]
LSM303C_M_SENSITIVITY_XY_2_5Ga = const(670)  # 2.5 Ga full scale [LSB/Ga]
LSM303C_M_SENSITIVITY_XY_4Ga = const(450)    # 4 Ga full scale [LSB/Ga]
LSM303C_M_SENSITIVITY_XY_4_7Ga = const(400)  # 4.7 Ga full scale [LSB/Ga]
LSM303C_M_SENSITIVITY_XY_5_6Ga = const(330)  # 5.6 Ga full scale [LSB/Ga]
LSM303C_M_SENSITIVITY_XY_8_1Ga = const(230)  # 8.1 Ga full scale [LSB/Ga]
# Magnetometer Sensitivity forZ Axis
LSM303C_M_SENSITIVITY_Z_1_3Ga = const(980)   # 1.3 Ga full scale [LSB/Ga]
LSM303C_M_SENSITIVITY_Z_1_9Ga = const(760)   # 1.9 Ga full scale [LSB/Ga]
LSM303C_M_SENSITIVITY_Z_2_5Ga = const(600)   # 2.5 Ga full scale [LSB/Ga]
LSM303C_M_SENSITIVITY_Z_4Ga = const(400)     # 4 Ga full scale [LSB/Ga]
LSM303C_M_SENSITIVITY_Z_4_7Ga = const(355)   # 4.7 Ga full scale [LSB/Ga]
LSM303C_M_SENSITIVITY_Z_5_6Ga = const(295)   # 5.6 Ga full scale [LSB/Ga]
LSM303C_M_SENSITIVITY_Z_8_1Ga = const(205)   # 8.1 Ga full scale [LSB/Ga]

LSM303C_CONTINUOUS_CONVERSION = const(0x00)  # Continuous-Conversion Mode
LSM303C_SINGLE_CONVERSION = const(0x01)  # Single-Conversion Mode
LSM303C_SLEEP = const(0x02)  # Sleep Mode

LSM303C_CTRL_REG2_M_RESET = LSM303C_MAG_REBOOT_ENABLE | \
                            LSM303C_MAG_SOFT_RESET_ENABLE
LSM303C_CTRL_REG2_M_CONF = LSM303C_MAG_FS_16_GA | LSM303C_MAG_REBOOT_DEFAULT |\
                           LSM303C_MAG_SOFT_RESET_DEFAULT
LSM303C_CTRL_REG3_M_CONF = LSM303C_MAG_SPI_MODE |\
                           LSM303C_MAG_CONFIG_NORMAL_MODE |\
                           LSM303C_MAG_CONTINUOUS_MODE
LSM303C_CTRL_REG1_M_CONF = LSM303C_MAG_TEMPSENSOR_DISABLE |\
                           LSM303C_MAG_OM_XY_ULTRAHIGH | LSM303C_MAG_ODR_40_HZ
LSM303C_CTRL_REG4_M_CONF = LSM303C_MAG_OM_Z_ULTRAHIGH | LSM303C_MAG_BLE_LSB
LSM303C_CTRL_REG5_M_CONF = LSM303C_MAG_BDU_CONTINUOUS
