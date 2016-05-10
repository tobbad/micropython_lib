"""
"""

from pyb import delay

class ILI9341:
    # Level 1 Commands 
    SWRESET = 0x01   # Software Reset 
    READ_DISPLAY_ID = 0x04   # Read display identification information 
    RDDST = 0x09   # Read Display Status 
    RDDPM = 0x0A   # Read Display Power Mode 
    RDDMADCTL = 0x0B   # Read Display MADCTL 
    RDDCOLMOD = 0x0C   # Read Display Pixel Format 
    RDDIM = 0x0D   # Read Display Image Format 
    RDDSM = 0x0E   # Read Display Signal Mode 
    RDDSDR = 0x0F   # Read Display Self-Diagnostic Result 
    SPLIN = 0x10   # Enter Sleep Mode 
    SLEEP_OUT = 0x11   # Sleep out register 
    PTLON = 0x12   # Partial Mode ON 
    NORMAL_MODE_ON = 0x13   # Normal Display Mode ON 
    DINVOFF = 0x20   # Display Inversion OFF 
    DINVON = 0x21   # Display Inversion ON 
    GAMMA = 0x26   # Gamma register 
    DISPLAY_OFF = 0x28   # Display off register 
    DISPLAY_ON = 0x29   # Display on register 
    COLUMN_ADDR = 0x2A   # Colomn address register  
    PAGE_ADDR = 0x2B   # Page address register  
    GRAM = 0x2C   # GRAM register    
    RGBSET = 0x2D   # Color SET    
    RAMRD = 0x2E   # Memory Read    
    PLTAR = 0x30   # Partial Area    
    VSCRDEF = 0x33   # Vertical Scrolling Definition    
    TEOFF = 0x34   # Tearing Effect Line OFF    
    TEON = 0x35   # Tearing Effect Line ON    
    MAC = 0x36   # Memory Access Control register
    VSCRSADD = 0x37   # Vertical Scrolling Start Address    
    IDMOFF = 0x38   # Idle Mode OFF    
    IDMON = 0x39   # Idle Mode ON    
    PIXEL_FORMAT = 0x3A   # Pixel Format register 
    WRITE_MEM_CONTINUE = 0x3C   # Write Memory Continue    
    READ_MEM_CONTINUE = 0x3E   # Read Memory Continue    
    SET_TEAR_SCANLINE = 0x44   # Set Tear Scanline    
    GET_SCANLINE = 0x45   # Get Scanline    
    WDB = 0x51   # Write Brightness Display register 
    RDDISBV = 0x52   # Read Display Brightness    
    WCD = 0x53   # Write Control Display register
    RDCTRLD = 0x54   # Read CTRL Display    
    WRCABC = 0x55   # Write Content Adaptive Brightness Control    
    RDCABC = 0x56   # Read Content Adaptive Brightness Control    
    WRITE_CABC = 0x5E   # Write CABC Minimum Brightness    
    READ_CABC = 0x5F   # Read CABC Minimum Brightness    
    READ_ID1 = 0xDA   # Read ID1 
    READ_ID2 = 0xDB   # Read ID2 
    READ_ID3 = 0xDC   # Read ID3 

    # Level 2 Commands 
    RGB_INTERFACE = 0xB0   # RGB Interface Signal Control 
    FRMCTR1 = 0xB1   # Frame Rate Control (In Normal Mode) 
    FRMCTR2 = 0xB2   # Frame Rate Control (In Idle Mode) 
    FRMCTR3 = 0xB3   # Frame Rate Control (In Partial Mode) 
    INVTR = 0xB4   # Display Inversion Control 
    BPC = 0xB5   # Blanking Porch Control register 
    DFC = 0xB6   # Display Function Control register 
    ETMOD = 0xB7   # Entry Mode Set 
    BACKLIGHT1 = 0xB8   # Backlight Control 1 
    BACKLIGHT2 = 0xB9   # Backlight Control 2 
    BACKLIGHT3 = 0xBA   # Backlight Control 3 
    BACKLIGHT4 = 0xBB   # Backlight Control 4 
    BACKLIGHT5 = 0xBC   # Backlight Control 5 
    BACKLIGHT7 = 0xBE   # Backlight Control 7 
    BACKLIGHT8 = 0xBF   # Backlight Control 8 
    POWER1 = 0xC0   # Power Control 1 register 
    POWER2 = 0xC1   # Power Control 2 register 
    VCOM1 = 0xC5   # VCOM Control 1 register 
    VCOM2 = 0xC7   # VCOM Control 2 register 
    NVMWR = 0xD0   # NV Memory Write 
    NVMPKEY = 0xD1   # NV Memory Protection Key 
    RDNVM = 0xD2   # NV Memory Status Read 
    READ_ID4 = 0xD3   # Read ID4 
    PGAMMA = 0xE0   # Positive Gamma Correction register 
    NGAMMA = 0xE1   # Negative Gamma Correction register 
    DGAMCTRL1 = 0xE2   # Digital Gamma Control 1 
    DGAMCTRL2 = 0xE3   # Digital Gamma Control 2 
    INTERFACE = 0xF6   # Interface control register 

    # Extend register commands 
    POWERA = 0xCB   # Power control A register 
    POWERB = 0xCF   # Power control B register 
    DTCA = 0xE8   # Driver timing control A 
    DTCB = 0xEA   # Driver timing control B 
    POWER_SEQ = 0xED   # Power on sequence register 
    GAMMA_EN = 0xF2   # 3 Gamma enable register 
    PRC = 0xF7   # Pump ratio control register 

    # Size of read registers 
    READ_ID4_SIZE = 3      # Size of Read ID4 
    
    def __init__(self, csx, wrx, rdx, ser_dev):
        self._csx = csx
        self._wrx = wrx
        self._rdx = rdx
        self._ser = ser_dev
        #Configure LCD */
        self.write_reg(0xCA)
        self.write_data(0xC3)
        self.write_data(0x08)
        self.write_data(0x50)
        self.write_reg(self.POWERB)
        self.write_data(0x00)
        self.write_data(0xC1)
        self.write_data(0x30)
        self.write_reg(self.POWER_SEQ)
        self.write_data(0x64)
        self.write_data(0x03)
        self.write_data(0x12)
        self.write_data(0x81)
        self.write_reg(self.DTCA)
        self.write_data(0x85)
        self.write_data(0x00)
        self.write_data(0x78)
        self.write_reg(self.POWERA)
        self.write_data(0x39)
        self.write_data(0x2C)
        self.write_data(0x00)
        self.write_data(0x34)
        self.write_data(0x02)
        self.write_reg(self.PRC)
        self.write_data(0x20)
        self.write_reg(self.DTCB)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_reg(self.FRMCTR1)
        self.write_data(0x00)
        self.write_data(0x1B)
        self.write_reg(self.DFC)
        self.write_data(0x0A)
        self.write_data(0xA2)
        self.write_reg(self.POWER1)
        self.write_data(0x10)
        self.write_reg(self.POWER2)
        self.write_data(0x10)
        self.write_reg(self.VCOM1)
        self.write_data(0x45)
        self.write_data(0x15)
        self.write_reg(self.VCOM2)
        self.write_data(0x90)
        self.write_reg(self.MAC)
        self.write_data(0xC8)
        self.write_reg(self.GAMMA_EN)
        self.write_data(0x00)
        self.write_reg(self.RGB_INTERFACE)
        self.write_data(0xC2)
        self.write_reg(self.DFC)
        self.write_data(0x0A)
        self.write_data(0xA7)
        self.write_data(0x27)
        self.write_data(0x04)

        #Colomn address set */
        self.write_reg(self.COLUMN_ADDR)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xEF)
        #Page address set */
        self.write_reg(self.PAGE_ADDR)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x3F)
        self.write_reg(self.INTERFACE)
        self.write_data(0x01)
        self.write_data(0x00)
        self.write_data(0x06)

        self.write_reg(self.GRAM)
        delay(200)

        self.write_reg(self.GAMMA)
        self.write_data(0x01)

        self.write_reg(self.PGAMMA)
        self.write_data(0x0F)
        self.write_data(0x29)
        self.write_data(0x24)
        self.write_data(0x0C)
        self.write_data(0x0E)
        self.write_data(0x09)
        self.write_data(0x4E)
        self.write_data(0x78)
        self.write_data(0x3C)
        self.write_data(0x09)
        self.write_data(0x13)
        self.write_data(0x05)
        self.write_data(0x17)
        self.write_data(0x11)
        self.write_data(0x00)
        self.write_reg(self.NGAMMA)
        self.write_data(0x00)
        self.write_data(0x16)
        self.write_data(0x1B)
        self.write_data(0x04)
        self.write_data(0x11)
        self.write_data(0x07)
        self.write_data(0x31)
        self.write_data(0x33)
        self.write_data(0x42)
        self.write_data(0x05)
        self.write_data(0x0C)
        self.write_data(0x0A)
        self.write_data(0x28)
        self.write_data(0x2F)
        self.write_data(0x0F)

        self.write_reg(self.SLEEP_OUT)
        delay(200)
        self.write_reg(self.DISPLAY_ON)
        #GRAM start writing */
        self.write_reg(self.GRAM)
        self.display_off()
        
    def write_data(self, regvalue):
        self._wrx.high()
        self._csx.low()
        self._ser.send(regvalue)
        self._csx.high()
    
    def write_reg(self, reg):
        self._wrx.low()
        self._csx.low()
        self._ser.send(reg)
        self._csx.high()
    
    def read_data(self, regvalue, readsize):
        self._csx.low()
        self._wrx.low()
        readvalue = self._ser.recv(readsize)
        self._wrx.high()
        self._csx.high()
        return readvalue
    
    def read_id(self):
        res = self.read_data(self.READ_ID4, self.READ_ID4_SIZE)
        return res

    def display_off(self):
        self.write_reg(self.DISPLAY_OFF)

    def display_on(self):
        self.write_reg(self.DISPLAY_ON)
