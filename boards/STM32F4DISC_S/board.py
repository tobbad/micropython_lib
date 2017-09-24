#
#
#
import pyb

sys_config = {
    'stlink_uart':{'uart':1},
    'lis302dl': {'spi_bus': 1, 'spi_cs': 'PE3'},
    'cs43l22': {'i2c_bus': 1, 'i2c_addr': 0x4A, 'resetPin': 'PD4'},
    'lora':{'spi_bus':1, 'spi_cs':'PB11',  'resetPin':'PD4'},
    'switch':{'pins':['PB7','PE3','PC11','PD6'], 'conf':[(pyb.Pin.IN, pyb.Pin.PULL_UP),(pyb.Pin.IN, pyb.Pin.PULL_UP),(pyb.Pin.IN, pyb.Pin.PULL_UP),(pyb.Pin.IN, pyb.Pin.PULL_UP)]},
    'led':{'pins':['PC13','PC15'] },
    'sdcard':{'spi_bus':3, 'spi_cs':'PB8'},
    'ads7843':{'spi_bus':3, 'spi_cs':'PE2', 'busy':'PD7', 'irq':'PA8'},
    'ads7843':{'spi_bus':3, 'spi_cs':'PE2', 'busy':'PD7'}, # Touch panel controller
    'ssd1289':{'data':['PD0', 'PD1', 'PD2', 'PD3', 'PE4', 'PE5', 'PE6', 'PE7', 'PE8', 'PE9', 'PE10', 'PE11', 'PE12', 'PE13', 'PE14', 'PE15', 'PE16'],
               'wr':'PC2',
               'rd':'PC1',
               'rs':'PC0',
               'cs':'PD10',
               'reset':'PC5',
               'led-a':'PA15'},
    'sd':{'spi_bus':3, 'spi_cs':'PB8'},
    'led_matrix':{'red':['PD0','PD3'], 'green':['PD1','PE4'], 'blue':['PD2','PE5'],
                  'color':['PD0','PD3', 'PD1','PE4', 'PD2','PE5'],
                  'a':'PE6', 'b':'PE8','c':'PE7','d':'PE9',
                  'line_sel':['PE6', 'PE8','PE7', 'PE9'],
                  'clk':'PE11',
                  'latch':'PE10',
                  'oe':'PE12'},
    'pmod':{'p3':{'uart':3, 'reset':'PC4','one_pps':'PB1','fix':'PC14'},
            'p7':{'i2c_bus':1,  'lps22hb_addr': 0x5C,  'int_1':'pc9',  'int_2':'pc6'},
            'p8':{'uart':1, 'pin_1':'PA0', 'pin_4':'PA1'} # UART TX/RX is used as ST-LINK UART VCP is wired.
           },
    'at86rf215':{'spi_bus': 3, 'spi_cs': 'PB8', 'spi_polarity':0, 'spi_phase':0, 'reset':'PE2', 'irq':'PD10',
                 'spi_bit_bang':{'sck':'PB14', 'miso':'PD9','mosi':'PD8','nss':'PD11'},
                 'spi_bit_bang_P3':{'sck':'PB14', 'miso':'PD9','mosi':'PD8','nss':'PC4'}
                 }
}
