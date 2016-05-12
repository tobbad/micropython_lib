#
#
#
import pyb

sys_config = {
    'sx127x': {'spi_bus': 1, 'spi_cs': 'X5'},
    'mma7660': {'i2c_bus': 1, 'i2c_addr': 0x4c, "avdd":"B5"},
}
