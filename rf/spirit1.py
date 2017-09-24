'''
Driver for SPIRIT1 SubGhz transceiver of STMicro
'''

class SUBGHZ_RFRXTX:
     
    MODULATIOM={
                'FSK'         = 0x00, #/*!< 2-FSK modulation selected */
                'GFSK_BT05'   = 0x50, #/*!< GFSK modulation selected with BT=0.5 */
                'GFSK_BT1'    = 0x10, #/*!< GFSK modulation selected with BT=1 */
                'ASK_OOK'     = 0x20, #/*!< ASK or OOK modulation selected. ASK will use power ramping */
                'MSK'         = 0x30  #/*!< MSK modulation selected */
                }
}
    BAND={  
        'HIGH_BAND'     : 0x00, #/*!< High_Band selected: from 779 MHz to 915 MHz */
        'MIDDLE_BAND'   : 0x01, #/*!< Middle Band selected: from 387 MHz to 470 MHz */ 
        'LOW_BAND'      : 0x02, # /*!< Low Band selected: from 300 MHz to 348 MHz */
        'VERY_LOW_BAND' : 0x03  #/*!< Vary low Band selected: from 150 MHz to 174 MHz */
    }



class SPIRIT1(RFRXTX):
    
    DEBUG=False
    
    def __init__(self, com):
        self._com = com
        
        
    def 
        
    
