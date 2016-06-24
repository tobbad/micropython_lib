#
#
#
import pyb

sys_config = {
    'lis302dl': {'spi_bus': 1, 'spi_cs': 'PE3'},
    'cs43l22': {'i2c_bus': 1, 'i2c_addr': 0x4A, 'resetPin': 'PD4'},
    'lora':{'spi_bus':1, 'resetPin':'PD4'},
    'switch':{'pins':['PB7','PE3','PC11','PD6'], 'conf':[(pyb.Pin.IN, pyb.Pin.PULL_UP),(pyb.Pin.IN, pyb.Pin.PULL_UP),(pyb.Pin.IN, pyb.Pin.PULL_UP),(pyb.Pin.IN, pyb.Pin.PULL_UP)]},
    'led':{'pins':['PC13','PC15'] },
    'sdcard':{'spi_bus':3, 'spi_cs':'PB8'},
    'ads7843':{'spi_bus':3, 'spi_cs':'PB8', 'busy':'PD7'}, # Touch panel controller
    'SSD1289':{'data':['PD0', 'PD1', 'PD2', 'PD3', 'PE4', 'PE5', 'PE6', 'PE7', 'PE8', 'PE9', 'PE10', 'PE11', 'PE12', 'PE13', 'PE14', 'PE15', 'PE16'],
               'wr':'PC2',
               'rd':'PC1',
               'rs':'PC0',
               'cs':'PD10',
               'reset':'PC5',
               'led-a':'PA15'},
    'led_matrix':{'red':['PD0','PD3'], 'green':['PD1','PE4'], 'blue':['PD2','PE5'], 
                  'color':['PD0','PD3', 'PD1','PE4', 'PD2','PE5'],
                  'a':'PE6', 'b':'PE8','c':'PE7','d':'PE9',
                  'line_sel':['PE6', 'PE8','PE7', 'PE9'],
                  'clk':'PE11', 
                  'latch':'PE10',
                  'oe':'PE12'},
    'pmod':{'gps':{'uart':3, 'reset':'PC4','onepps':'PA3','fix':'PC14'} }
}
