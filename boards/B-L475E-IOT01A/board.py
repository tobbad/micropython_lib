#
#
#
import pyb
sys_config = {
    'hts221':   {'i2c_bus': 2, 'i2c_addr': 0xBE>>1, 'irqPin':'PD15'},
    'lis3mdl':  {'i2c_bus': 2, 'i2c_addr': 0x3C>>1, 'irqPin':'PC8'},
    'lps22hb':  {'i2c_bus': 2, 'i2c_addr': 0xBA>>1, 'irqPin':'PD10'},
    'lsm6dsl':  {'i2c_bus': 2, 'i2c_addr': 0xD4>>1, 'irqPin':'PD11'},
    'vl53lox':  {'i2c_bus': 2, 'i2c_addr': 0x52>>1, 'irqPin':'','xshut':'PC6', 'gpio':'PC7'},
    'm24sr64-y':{'i2c_bus': 2, 'i2c_addr': 0xAC>>1, 'gpo':'PE4', 'disable':'PE2'},
    'ism43362-m3g-l44':{'spi_bus': 3, 'spi_cs': 'PE0', 'resetPin':'PE8', 'boot0':'PB12','wakeup':'PB13','irqPin':'PE1'},
    'spbtle-rf':{'spi_bus': 3, 'spi_cs': 'PD13', 'resetPin':'PA8', 'irqPin':'PE6'},
    'spsgrf':{'spi_bus': 3, 'spi_cs': 'PB5', 'irqPin':'PE5', 'sdn':'PB15'},
    'microphone':{'data':'PE7', 'clk':'PE9'},
    'button':{'pins':['PC13',], 'conf':[(pyb.Pin.IN, pyb.Pin.PULL_UP),]},
    'led1':{'pin':'PA5'},
    'led2':{'pin':'PB14'},
    'led_wifi_btle':{'pin':'PC9'}
}

