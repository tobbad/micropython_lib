#
#
#
import pyb

sys_config={
    'lis302dl':{'spi_bus':1, 'spi_cs': 'PE3'},
    'cs43l22':{'i2c_bus':1, 'i2c_addr': 0x4A, 'resetPin':'PD4'},
}
