#
# Board configuration fro STM32L496G-DISCO
#

sys_config = {
    'led': {'1': 'B13', '2':'io1:4'},
    'lcd': {'backlight': 'I0'},
    'touch': {'i2c_bus': 2, 'i2c_addr':0x70>>1, 'irq': 'g14', 'reset':'io1:1'},
    'joystick': {'up': 'I8', 'down': 'i10', 'left': 'i9', 'right':'f11', 'sel':'C3'},
    'idd': {'i2c_bus': 2, 'i2c_addr': 0x42, 'wakeup':'H6', 'irq':'C5' },
    'io1': {'i2c_bus': 2, 'i2c_addr': 0x42, 'wakeup':'H6', 'irq':'C5' },
    'cs42l51': {'i2c_bus': 2, 'i2c_addr':0x94>>1, 'reset':'C6' },
    'camera': {'i2c_bus': 2, 'i2c_addr':0x60>>1},
}
