'''
Driver for Samtech SX1276/77/78/79 which is
the same chip as HopeRF RF-96

Some code was taken from pySX127x python driver for raspberry Pi:
https://github.com/mayeranalytics/pySX127x.git
and micropytonized.
'''
from i2cspi import COM_SPI
from multibyte import multibyte
from sx127x_const import *
import pyb

CH={}
CH[868]={}
CH[868][10] = 0xD84CCC  # channel 10, central freq = 865.20MHz
CH[868][11] = 0xD86000  # channel 11, central freq = 865.50MHz
CH[868][12] = 0xD87333  # channel 12, central freq = 865.80MHz
CH[868][13] = 0xD88666  # channel 13, central freq = 866.10MHz
CH[868][14] = 0xD89999  # channel 14, central freq = 866.40MHz
CH[868][15] = 0xD8ACCC  # channel 15, central freq = 866.70MHz
CH[868][16] = 0xD8C000  # channel 16, central freq = 867.00MHz
CH[868][17] = 0xD90000  # channel 17, central freq = 868.00MHz
CH[868][18] = 0xD90666  # 868.1MHz for LoRaWAN test
CH[900]={}
CH[900][00] = 0xE1C51E  # channel 00, central freq = 903.08MHz
CH[900][01] = 0xE24F5C  # channel 01, central freq = 905.24MHz
CH[900][02] = 0xE2D999  # channel 02, central freq = 907.40MHz
CH[900][03] = 0xE363D7  # channel 03, central freq = 909.56MHz
CH[900][04] = 0xE3EE14  # channel 04, central freq = 911.72MHz
CH[900][05] = 0xE47851  # channel 05, central freq = 913.88MHz
CH[900][06] = 0xE5028F  # channel 06, central freq = 916.04MHz
CH[900][07] = 0xE58CCC  # channel 07, central freq = 918.20MHz
CH[900][08] = 0xE6170A  # channel 08, central freq = 920.36MHz
CH[900][09] = 0xE6A147  # channel 09, central freq = 922.52MHz
CH[900][10] = 0xE72B85  # channel 10, central freq = 924.68MHz
CH[900][11] = 0xE7B5C2  # channel 11, central freq = 926.84MHz
CH[900][12] = 0xE4C000  # default channel 915MHz, the module is configured with it
FSK_BANDWIDTH = (
    ( 2600  , 0x17 ),
    ( 3100  , 0x0F ),
    ( 3900  , 0x07 ),
    ( 5200  , 0x16 ),
    ( 6300  , 0x0E ),
    ( 7800  , 0x06 ),
    ( 10400 , 0x15 ),
    ( 12500 , 0x0D ),
    ( 15600 , 0x05 ),
    ( 20800 , 0x14 ),
    ( 25000 , 0x0C ),
    ( 31300 , 0x04 ),
    ( 41700 , 0x13 ),
    ( 50000 , 0x0B ),
    ( 62500 , 0x03 ),
    ( 83333 , 0x12 ),
    ( 100000, 0x0A ),
    ( 125000, 0x02 ),
    ( 166700, 0x11 ),
    ( 200000, 0x09 ),
    ( 250000, 0x01 ),
    ( 300000, 0x00 ), # Invalid Badwidth
)


class ModemException(Exception):
    pass


################################################## Some utility functions ##############################################

def set_bit(value, index, new_bit):
    """ Set the index'th bit of value to new_bit, and return the new value.
    :param value:   The integer to set the new_bit in
    :type value:    int
    :param index: 0-based index
    :param new_bit: New value the bit shall have (0 or 1)
    :return:    Changed value
    :rtype: int
    """
    mask = 1 << index
    value &= ~mask
    if new_bit:
        value |= mask
    return value


def getter(register_address):
    """ The getter decorator reads the register content and calls the decorated function to do
        post-processing.
    :param register_address: Register address
    :return: Register value
    :rtype: int
    """
    def decorator(func):
        def wrapper(self):
            return func(self, self.spi.xfer([register_address, 0])[1])
        return wrapper
    return decorator


def setter(register_address):
    """ The setter decorator calls the decorated function for pre-processing and
        then writes the result to the register
    :param register_address: Register address
    :return: New register value
    :rtype: int
    """
    def decorator(func):
        def wrapper(self, val):
            return self.read_u8(register_address, func(self, val))
        return wrapper
    return decorator

############################################### Definition of the SX127X class ###########################################

class SX127X(COM_SPI, multibyte):

    WHO_IAM_REG = 0x42
    WHO_IAM_ANSWER = 0x12

    MODE = {'SLEEP': 0x00, 'STDBY':0x01, 'FSTX':0x02, 'TX':0x03, 'FSRX':0x04, 'RX':0x05}

    READ_CMD = 0x00
    WRITE_CMD = 0x80
    MULTIPLEBYTE_CMD = 0x00

    DEFAULT_CONF = (
        [REG.FSK_OOK.LNA            , 0x23],
        [REG.FSK_OOK.RX_CONFIG      , 0x1E],
        [REG.FSK_OOK.RSSI_CONFIG    , 0xD2],
        [REG.FSK_OOK.PREAMBLE_DETECT, 0xAA],
        [REG.FSK_OOK.OSC            , 0x07],
        [REG.FSK_OOK.SYNC_CONFIG    , 0x12],
        [REG.FSK_OOK.SYNC_VALUE_1   , 0xC1],
        [REG.FSK_OOK.SYNC_VALUE_2   , 0x94],
        [REG.FSK_OOK.SYNC_VALUE_3   , 0xC1],
        [REG.FSK_OOK.PACKET_CONFIG_1, 0xD8],
        [REG.FSK_OOK.FIFO_THRESH    , 0x8F],
        [REG.FSK_OOK.IMAGE_CAL      , 0x02],
        [REG.FSK_OOK.DIO_MAPPING_1  , 0x00],
        [REG.FSK_OOK.DIO_MAPPING_2  , 0x30]
    )

    def __init__(self, communication, dev_selector, reset_pin, dio_pins, verbose = False, xtal_freq=32000000):
        self.DEBUG=verbose
        super().__init__(communication, dev_selector,
                         addr_size=self.ADDR_MODE_8,
                         msb_first=self.TRANSFER_MSB_FIRST)
        self.__freq_band = 868
        self.__freq_step = 5000.0/0x52 # FRom default value in reg 0x05
        self.__calib_ch = 17 if self.__freq_band == 868 else 05
        self.__xtal_freq = xtal_freq
        # reset devices
        self.__reset_pin = reset_pin
        self.set_up()
        
    def set_up(self):
        self.reset()
        self.rx_chain_calib()
        self.set_op_mode('SLEEP')
        self.set_op_mode('FSK')
        self.init()
        self.set_op_mode('LORA')
        self.write_u8(REG.LORA.PAYLOAD_LENGTH, 0x40)
        self.set_op_mode('FSK')

    def reset(self):
        self.__reset_pin.low()
        pyb.delay(2)
        self.__reset_pin.high()
        pyb.delay(6)

    def set_pa(self, pa_select=0, max_power=0x04, output_power=0x0f):
        ''' Set pa to given state: Maps to the signals in REG_PACONFIG'''
        pa_select = min(pa_select, 1)
        max_power = min(max_power, 0x07)
        output_power = min(output_power, 0x0f)
        val = pa_select << 7 | max_power << 4 | output_power
        self.write_u8(REG.LORA.PA_CONFIG, val)

    def set_op_mode(self, mode):
        MODULATION_MASK=0xE0
        MODE_MASK = 0x07
        mod_mode={'FSK':0x20,'OOK':0x00, 'LORA':0x80}
        if mode in mod_mode:
            val = self.read_u8(REG.LORA.OP_MODE)
            cMode = val & MODE_MASK
            val &= ~(MODULATION_MASK | MODE_MASK)
            val |= mod_mode[mode]
            self.write_u8(REG.LORA.OP_MODE, val)
            val |= cMode
            self.write_u8(REG.LORA.OP_MODE, val)
            self.modem = mode
        elif mode in self.MODE:
            val = self.read_u8(REG.LORA.OP_MODE)
            val &= ~MODE_MASK
            val |= self.MODE[mode]
            self.write_u8(REG.LORA.OP_MODE, val)
            self.mode = mode
        else:
            raise ModemException("Unknown mode %s" % mode)

    def start_calib(self):
        val = self.read_u8(REG.FSK_OOK.IMAGE_CAL)
        val |= CALIBRATE.MODE.start
        self.write_u8(REG.FSK_OOK.IMAGE_CAL, val)

    def rx_chain_calib(self):
        # Goto standby
        self.set_op_mode('STDBY')
        # Save configuration
        pa_conf = self.read_u8(REG.LORA.PA_CONFIG)
        ch_conf =self.get_channel()
        # Prepare
        self.set_pa(0,0,0)
        self.start_calib()
        self.set_channel(self.__calib_ch)
        while self.read_u8(REG.FSK_OOK.IMAGE_CAL) & CALIBRATE.MODE.running == CALIBRATE.MODE.running:
            pyb.delay(1)
        # Restore configuratiuon
        self.write_u8(REG.LORA.PA_CONFIG, pa_conf)
        self.set_channel(ch_conf)


    def set_channel(self, chNr):
        if chNr not in CH[self.__freq_band]:
            raise ModemException("Channel %d not supportet in frequency band %d" % (chNr, self.__freq_band))
        self.write_u24_r(REG.LORA.FR_MSB, CH[self.__freq_band][chNr])

    def get_channel(self):
        freq = self.read_u24_r(REG.LORA.FR_MSB)
        for chIdx, ch in zip(range(len(CH[self.__freq_band])),CH[self.__freq_band]):
            if CH[self.__freq_band][ch] == freq:
                break
        if chIdx == len(CH[self.__freq_band]):
            raise ModemException("Read back unknown frequency 0x%06x" % (freq))
        return ch

    def version(self):
        return self.read_u8(self.WHO_IAM_REG)

    def available_modulation(self):
        return (self.MODULATION_FSK|self.MODULATION_GFSK|
                self.MODULATION_MSK|self.MODULATION_GMSK|
                self.MODULATION_OOK|self.MODULATION_LORA)


    def data_rate(self, datarate=None):
        if datarate is None:
            val = self.read_u16_r(REG.FSK_OOK.BIT_RATE_MSB)
            val = self.__xtal_freq/val if val>0 else 0
            return val
        val = int(round(float(self.__xtal_freq)/datarate))
        val = 1<<16-1 if val>1<<16 else val
        self.write_u16(REG.FSK_OOK.BIT_RATE_MSB, val)

    def freq_dev(self, freq_dev_Hz=None):
        if freq_dev_Hz is None:
            val = self.read_u16_r(REG.FSK_OOK.FREQ_DEV_MSB)
            val *= self.__freq_step
            return val
        val = int(round(float(freq_dev_Hz)/self.__freq_step))
        val = 1<<16-1 if val>1<<16 else val
        self.write_u16_r(REG.FSK_OOK.FREQ_DEV_MSB, val)

    def get_fsk_bandwidth_reg_value(self, bw):
        idx_len = len(FSK_BANDWIDTH)-1
        for idx in range(idx_len):
            if FSK_BANDWIDTH[idx][0] <= bw < FSK_BANDWIDTH[idx+1][0]:
                break
        if idx == idx_len:
            raise ModemException("FSK bandwidth %d not supported" % (bw))
        val = FSK_BANDWIDTH[idx][1]
        return val

    def set_fsk_rx_bw(self, bw):
        val = self.get_fsk_bandwidth_reg_value(bw)
        self.write_u16(REG_RXBW, val)

    def set_fsk_afc_bw(self, bw):
        val = self.get_fsk_bandwidth_reg_value(bw)
        self.write_u16(REG_AFCBW, val)

    def set_fsk_preamble_length(self, length):
        self.write_u16_r(REG_PREAMBLEMSB, length)

    def set_payload_length(self, fix_length, length):
        if fix_length:
            value = 1
        else:
            value = 0xFF
        self.write_u8(REG_PAYLOADLENGTH, value)

    def set_packet_config(self, fix_length, crcOn):
        val = self._read_u8(REG_PACKETCONFIG1)
        val &= RF_PACKETCONFIG1_CRC_MASK
        val &= RF_PACKETCONFIG1_PACKETFORMAT_MASK
        val |= ( RF_PACKETCONFIG1_PACKETFORMAT_FIXED if fix_length
                 else RF_PACKETCONFIG1_PACKETFORMAT_VARIABLE )
        val |= ( crcOn << 4 )
        self.write_u8(REG_PACKETCONFIG1, val)

    def set_rx_config(self, modem, bandwidth, datarate, coderate,
                         bandwidthAfc, preambleLen,
                         symbTimeout, fixLen, payloadLen,
                         crcOn, freqHopOn, hopPeriod,
                         iqInverted, rxContinuous ):
        self.set_op_mode(modem)
        if modem in ('FSK', 'OOK'):
            self.set_data_rate(datarate)
            self.set_fsk_rx_bw(bandwidth)
            self.set_fsk_afc_bw(bandwidthAfc)
            self.set_payload_length(fixLen, payloadLen)
            self.set_packet_config(fixLen, crcOn)
        else:
            raise ModemException("%s modulation not supported" % modem)

    def set_tx_config(self, modem, power, fdev,
                         bandwidth,  datarate,
                         coderate,  preambleLen,
                         fixLen,  crcOn, freqHopOn,
                         hopPeriod,  iqInverted,  timeout):
         self.set_op_mode(modem)
         self.cofig_pa()




