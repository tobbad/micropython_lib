#
#
#
import pyb

config = {
    'stlink_uart':{'uart':2},
    'mfx':{'i2c_bus': 2, 'i2c_addr': 0x84>>1, 'wakeUp_pin': 'A4', 'irq_pin':'C13'},
    'l3gd20': {'spi_bus': 2, 'spi_cs':'PD7' },
    'lsm303c_acc': {'spi_bus': 2, 'spi_cs':'PE0' },
    'lsm303c_rot': {'spi_bus': 2, 'spi_cs':'PC0' },
    'cs43l22': {'i2c_bus': 1, 'i2c_addr': 0x94>>1, 'resetPin': 'E3'},
    'switch':{'pins':['PA0','PA1','PA5','PA2', 'PA3'], 
              'name':['center','left','down','right','up'],
              'conf':[(pyb.Pin.IN, pyb.Pin.PULL_UP),(pyb.Pin.IN, pyb.Pin.PULL_UP),
                      (pyb.Pin.IN, pyb.Pin.PULL_UP),(pyb.Pin.IN, pyb.Pin.PULL_UP),
                      (pyb.Pin.IN, pyb.Pin.PULL_UP)]},
    'led':{'pins':['B2','E8'], 'name':['red','green'] },
}
