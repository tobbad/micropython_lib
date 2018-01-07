#
#
#
import pyb

config = {
    'stlink_uart':{'uart':2},
    'switch':{'pin':'C13', 
              'name':'btn',
              'mode':pyb.Pin.IN,
              'pull':pyb.Pin.PULL_UP},
    'led':{'pins':['A5',], 
           'name':'red' },
    'a2stm':{'A0':'A0', 
             'A1':'A1', 
             'A2':'A4', 
             'A3':'B0', 
             'A4':'C1', 
             'A5':'C0',
             'D0':'A3',
             'D1':'A2',
             'D2':'A10',
             'D3':'B3',
             'D4':'B5',
             'D5':'B4',
             'D6':'B10',
             'D7':'A8',
             'D8':'A9',
             'D9':'C7',
             'D10':'B6',
             'D11':'A7',
             'D12':'A6',
             'D13':'A5',
             'D14':'B9',
             'D15':'B8',
             },
}

