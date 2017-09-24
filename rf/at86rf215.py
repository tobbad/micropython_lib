
'''
Driver for Atmel AT86RF215.

'''
from micropython_lib.lib.i2cspi import COM_SPI
from micropython_lib.lib.multibyte import multibyte
import time

def mode_iter(_dict):
    for k, v in _dict.items():
        if k.upper() != k:
            # Skip items with lowercase chars
            continue
        yield k,v

def key_from_value(_dict, value):
    res = tuple(k for k, v  in _dict.items() if (value == v and k.upper() == k))
    if len(res) > 1:
        raise ValueError("Given value is not unique in dictionary")
    if len(res) == 0:
        raise ValueError("Given value does not exist in dictionary")
    return res[0]

class AT86_BASECLASS:

    BAND = {
        'RF09':0,
        'RF24':1
    }

    DEBUG = False

    def __init__(self, parent, frequency_band_str, debug=False):
        self.parent = parent
        self.band = frequency_band_str
        self.DEBUG = debug
        self.base_addr = self.BASE_ADDR[frequency_band_str]

    def _register(self, addr, bit_field=None, value=None):
        addr+=self.base_addr
        return self.parent._register(addr, bit_field, value)

    def reg_to_dict(self, register, value):
        _dict = {}
        for bf_name, v in mode_iter(register):
            _dict[bf_name] = (value & v['mask'])>>v['shift']
        return _dict

class RF_TRANCEIVER(AT86_BASECLASS):

    REG_STATE = {
        'addr':2,
        'STATE': {
            'shift':0,
            'mask': 0x07,
            0x02:'RF_TRXOFF',
            0x03:'RF_TXPREP',
            0x04:'RF_TX',
            0x05:'RF_RX',
            0x06:'RF_TRANSITION',
            0x07:'RF_RESET'
        }
    }

    REG_CMD = {
        'addr':3,
        'CMD': {
            'shift':0,
            'mask': 0x07,
            'RF_NOP': 0x0,
            'RF_SLEEP':0x1,
            'RF_TRXOFF':0x2,
            'RF_TXPREP':0x3,
            'RF_TX':0x4,
            'RF_RX':0x5,
            'RF_RESET':0x7,
        }
    }

    REG_TXDFE = {
        'addr':0x13,
        'RCUT': {
            'shift':5,
            'mask': 0xE0,
            '0.25FS/2':0x00,
            '0.375FS/2':0x01,
            '0.5FS/2':0x02,
            '0.75FS/2':0x03,
            'FS/2':0x04,
        },
        'DM':{ 'shift': 4, 'mask':0x01},
        'SR': {
            'shift':0,
            'mask': 0x0F,
            '4000KSPS':0x01,
            '2000KSPS':0x02,
            '4000/3KSPS':0x03,
            '1000KSPS':0x04,
            '800KSPS':0x05,
            '2000/3KSPS':0x06,
            '500KSPS':0x08,
            '400KSPS':0x0A,
        }
    }

    REG_RXDFE = {
        'addr':0x0a,
        'RCUT': REG_TXDFE['RCUT'],
        'SR': REG_TXDFE['SR'],
    }

    REG_TXCUTC = {
        'addr':0x12,
        'LPFCUT':{
            'shift':0,
            'mask':0x0f,
            'RF_FLC80KHZ' : 0x0,  #fLPFCUT = 80kHz
            'RF_FLC100KHZ': 0x1,  #fLPFCUT = 100kHz
            'RF_FLC125KHZ': 0x2,  #fLPFCUT = 125kHz
            'RF_FLC160KHZ': 0x3,  #fLPFCUT = 160kHz
            'RF_FLC200KHZ': 0x4,  #fLPFCUT = 200kHz
            'RF_FLC250KHZ': 0x5,  #fLPFCUT = 250kHz
            'RF_FLC315KHZ': 0x6,  #fLPFCUT = 315kHz
            'RF_FLC400KHZ': 0x7,  #fLPFCUT = 400kHz
            'RF_FLC500KHZ': 0x8,  #fLPFCUT = 500kHz
            'RF_FLC625KHZ': 0x9,  #fLPFCUT = 625kHz
            'RF_FLC800KHZ': 0xA,  #fLPFCUT = 800kHz
            'RF_FLC1000KHZ': 0xB, #fLPFCUT = 1000kHz
        }
    }

    REG_RXBWC = {
        'addr':0x09,
        'IFS':{'shift':4, "mask":0x10},
        'BW':{
            'shift':0,
            'mask':0x0f,
            'RF_BW160KHZ':  0x0,  # fBW =160kHz; fIF=250kHz
            'RF_BW200KHZ':  0x1,  # fBW =200kHz; fIF=250kHz
            'RF_BW250KHZ':  0x2,  # fBW =250kHz; fIF=250kHz
            'RF_BW320KHZ':  0x3,  # fBW =320kHz; fIF=500kHz
            'RF_BW400KHZ':  0x4,  # fBW =400kHz; fIF=500kHz
            'RF_BW500KHZ':  0x5,  # fBW =500kHz; fIF=500kHz
            'RF_BW630KHZ':  0x6,  # fBW =630kHz; fIF=1000kHz
            'RF_BW800KHZ':  0x7,  # fBW =800kHz; fIF=1000kHz
            'RF_BW1000KHZ': 0x8,  # fBW =1000kHz; fIF=1000kHz
            'RF_BW1250KHZ': 0x9,  # fBW =1250kHz; fIF=2000kHz
            'RF_BW1600KHZ': 0xA,  # fBW =1600kHz; fIF=2000kHz
            'RF_BW2000KHZ': 0xB,  # fBW =2000kHz; fIF=2000kHz
        }
    }

    REG_IRQS = {
        'addr':-1,
        'IQIFSF':{ 'shift':5, 'mask':0x20},
        'TRXERR':{ 'shift':4, 'mask':0x10},
        'BATLOW':{ 'shift':3, 'mask':0x08},
        'EDC':{ 'shift':2, 'mask':0x04},
        'TRXRDY':{ 'shift':1, 'mask':0x02},
        'WAKEUP':{ 'shift':0, 'mask':0x01},
    }

    REG_RF_PAC = {
        'addr': 0x14,
        'TXPWR':{ 'shift':0, 'mask':0x1f}
    }


    BASE_ADDR = {'RF09':0x0100, 'RF24':0x0200}
    FREQ_RANGES_HZ = {'RF09':((389500000, 510000000, 1),(779000000, 1020000000,2)),
                   'RF24':((2400000000, 2483500000, 3),) }
    FREQ_OFFSET_HZ = {'RF09':0, 'RF24':1500000000 }
    FREQ_BASE_HZ   = {'RF09':868000000, 'RF24':2400000000 }
    FREQ_SPACING_HZ= {'RF09':100000, 'RF24':100000 }
    SYNC_WORD = {'RF09':0xB547, 'RF24':0xB547 }
    FREQ_RESOLUTION_HZ = 25000
    IEEE_COMPLIANT_FREQ_CHANNEL = True
    IRQ_REG_ADDR= {'RF09':0x0000, 'RF24':0x0001}

    def __init__(self, parent, frequency_band_str, debug=False):
        super().__init__(parent, frequency_band_str, debug)
        self.__saved_state = None

    def setup_freq_default(self):
        self.base_freq(self.FREQ_BASE_HZ[self.band])
        self.channel_spacing(self.FREQ_SPACING_HZ[self.band])

    def state(self):
        addr = self.REG_STATE['addr']
        bit_field = self.REG_STATE['STATE']
        value =self._register(addr, bit_field)
        return self.REG_STATE['STATE'][value]

    def push_and_new_state(self, new_state='RF_TRXOFF'):
        if self.__saved_state != None:
            raise Exception("Already pushed state")
        self.__saved_state = self.state()

    def pop_state(self):
        if self.__saved_state == None:
            raise Exception("No state was pushed")
        if self.DEBUG:
            print("Saved state: %s" % (self.__saved_state))
        cur_state = self.state()
        if self.__saved_state != cur_state:
            if self.__saved_state in ('RF_TX', 'RF_RX'):
                self.command(self.__saved_state)
        self.__saved_state = None

    def irqs(self):
        addr = self.IRQ_REG_ADDR[self.band]
        value = self.parent.read_u8(addr)
        return self.reg_to_dict(self.REG_IRQS, value)

    def irqm(self, value):
        return self._register(0x00, value = value)

    def command(self, command):
        addr = self.REG_CMD['addr']
        bit_field = self.REG_CMD['CMD']
        value = self.REG_CMD['CMD'][command]
        self._register(addr, bit_field, value)

    def check_freq(self, freq_hz):
        freq_ok = False
        cnm_cm_ok = -1
        for f_low, f_high, cnm_cm in self.FREQ_RANGES_HZ[self.band]:
            if f_low <= freq_hz <= f_high:
                freq_ok=True
                cnm_cm_ok = cnm_cm
        if self.DEBUG:
            print("Frequency %.2f MHz: %s" %(freq_hz/1E6, "OK" if freq_ok else "NOK"))
        return freq_ok, cnm_cm_ok

    def base_freq(self, freq_hz=None):
        RF_CCF0 = 0x05 + self.base_addr
        if freq_hz is None:
            freq_nr = self.parent.read_u16(RF_CCF0)
            if self.DEBUG:
                print("Freq Nr read = 0x%04x" % (freq_nr))
            freq_hz = (freq_nr*self.FREQ_RESOLUTION_HZ)+self.FREQ_OFFSET_HZ[self.band]
        else:
            freq_nr = int((freq_hz - self.FREQ_OFFSET_HZ[self.band])/self.FREQ_RESOLUTION_HZ+0.5)
            if self.DEBUG:
                print("Freq Nr write= 0x%04x" % freq_nr)
            self.parent.write_u16_r(RF_CCF0, freq_nr)
        return freq_hz

    def channel_spacing(self, dfreq_hz=None):
        RF_CS = 0x04 + self.base_addr
        if dfreq_hz is None:
            value = self.parent.read_u8(RF_CS)
            dfreq_hz = value*self.FREQ_SPACING_HZ[self.band]
        else:
            value = int(dfreq_hz/self.FREQ_SPACING_HZ[self.band])
            self.parent.write_u8(RF_CS, value)
        return dfreq_hz

    def freq(self, freq_hz=None):
        freg_offset_hz = self.FREQ_OFFSET_HZ[self.band]
        if freq_hz is None:
            freq_hz = self.channel()
            freq_hz *=self.channel_spacing()
            freq_hz += self.base_freq()
        else:
            freq_ok , cnm_cm_ok = self.check_freq(freq_hz)
            if not freq_ok:
                raise ValueError("Non supported frequency %.2f MHz" % (freq_hz/1E6))
            b_freq = self.base_freq()
            channel_nr = (freq_hz- b_freq)/self.channel_spacing()
            self.channel(channel_nr)
        return freq_hz

    def channel(self, channel_nr=None):
        RF_CNL = 0x07 + self.base_addr
        if channel_nr is None:
            channel_nr = (self.parent.read_u16(RF_CNL)&0x01FF)
        else:
            channel_nr = int(round(channel_nr)) & 0x01FF
            ch_low = channel_nr & 0x00FF
            ch_hi = (channel_nr>>8) | 0x00 if self.IEEE_COMPLIANT_FREQ_CHANNEL else 0x40
            self.parent.write_u8(RF_CNL, ch_low)
            self.parent.write_u8(RF_CNL+1, ch_hi) # Commit the change to
        return channel_nr

    def sample_rate(self, is_rx, value=None):
        if is_rx:
            addr = self.REG_RXDFE['addr']
            bit_field = self.REG_RXDFE['SR']
        else:
            addr = self.REG_TXDFE['addr']
            bit_field = self.REG_TXDFE['SR']
        if value is None:
            value = self._register(addr, bit_field)
        else:
            if isinstance(value, str):
                value = bit_field[value]
            self._register(addr, bit_field, value)
        return value

    def tx_lowpass(self, mode=None):
        addr = self.REG_TXCUTC['addr']
        bit_field = self.REG_TXCUTC['LPFCUT']
        if mode is not None:
            mode = bit_field[mode]
            self._register(addr, bit_field, mode)
        else:
            value = self._register(addr, bit_field)
            mode = key_from_value(bit_field, value)
            return mode

    def rx_bw_if(self, mode=None):
        addr = self.REG_RXBWC['addr']
        bit_field = self.REG_RXBWC['BW']
        if mode is not None:
            value = bit_field[mode]
            self._register(addr, bit_field, value)
        else:
            value = self._register(addr, bit_field)
            mode = key_from_value(bit_field, value)
        return mode

    def rx_if_shift(self, value=None):
        addr = self.REG_RXBWC['addr']
        bit_field = self.REG_RXBWC['IFS']
        if value is not None:
            self._register(addr, bit_field, value)
        else:
            value = self._register(addr, bit_field)
        return value

    def digi_cut_off(self, is_rx, mode=None):
        if mode is None:
            if is_rx:
                value = self._register(self.REG_RXDFE['addr'], self.REG_RXDFE['RCUT'])
                mode = key_from_value(self.REG_RXDFE['RCUT'], value)
            else:
                value = self._register(self.REG_TXDFE['addr'], self.REG_TXDFE['RCUT'])
                mode = key_from_value(self.REG_TXDFE['RCUT'], value)
            if self.DEBUG:
                print("Get %s cut off %s" % (("RX" if is_rx else "TX"), mode))
        else:
            value = None
            if is_rx:
                value =  self.REG_RXDFE['RCUT'][mode]
                self._register(self.REG_RXDFE['addr'], self.REG_RXDFE['RCUT'], value)
            else:
                value =  self.REG_TXDFE['RCUT'][mode]
                self._register(self.REG_TXDFE['addr'], self.REG_TXDFE['RCUT'], value)
            if self.DEBUG:
                print("Set %s cut off %s/0x%02x" % (("RX" if is_rx else "TX"), mode, value))
        return mode

    def pa_power(self, value = None):
        addr = self.REG_RF_PAC['addr']
        bit_field = self.REG_RF_PAC['TXPWR']
        if value is not None:
            self._register(addr, bit_field, value)
        else:
            value = self._register(addr, bit_field)
        return value

    def rssi(self):
        addr = 0x0d + self.base_addr
        value = self.parent.read_s8(addr)
        return value

class BASEBAND(AT86_BASECLASS):

    REG_PC = {
        'addr': 0x01,
        'CTX':{ 'shift':7, 'mask':0x80},
        'FCSFE':{ 'shift':6, 'mask':0x40},
        'FCSOK':{ 'shift':5, 'mask':0x20},
        'TXAFCS':{ 'shift':4, 'mask':0x10},
        'FCST':{ 'shift':3, 'mask':0x08},
        'BBEN':{ 'shift':2, 'mask':0x04},
        'PT': {
            'shift':0,
            'mask':0x03,
            'BB_PHYOFF':0x00,
            'BB_MRFSK': 0x01,
            'BB_MROFDM':0x02,
            'BB_MROQPSK':0x03,
        }
    }

    REG_IRQS = {
        'addr':-1,
        'FBU':{ 'shift':7, 'mask':0x80},
        'AGCR':{ 'shift':6, 'mask':0x40},
        'AGCH':{ 'shift':5, 'mask':0x20},
        'TXFE':{ 'shift':4, 'mask':0x10},
        'RXEM':{ 'shift':3, 'mask':0x08},
        'RXAM':{ 'shift':2, 'mask':0x04},
        'RXFE':{ 'shift':1, 'mask':0x02},
        'RXFS':{ 'shift':0, 'mask':0x01},
    }

    REG_FSKC1 = {
        'addr': 0x61,
        'FSKPLH':{ 'shift':6, 'mask':0xC0},
        'FI':  { 'shift':5, 'mask':0x20},
        'SRATE':{ 'shift':0, 'mask':0x0F},
    }

    DEBUG = False
    BASE_ADDR = {'RF09':0x0300, 'RF24':0x0400}
    IRQ_REG_ADDR= {'RF09':0x0002, 'RF24':0x0003}

    def __init__(self, parent, frequency_band_str, debug=False):
        super().__init__(parent, frequency_band_str, debug)
        self.phy('BB_PHYOFF')

    def phy(self, mode=None):
        addr = self.REG_PC['addr']
        bit_field = self.REG_PC['PT']
        if mode is not None:
            value = bit_field[mode]
            self._register(addr, bit_field, value)
            self.phy = mode
        else:
            value = self._register(addr, bit_field)
            mode = key_from_value(bit_field, value)
        return mode

    def enable(self, value=None):
        addr = self.REG_PC['addr']
        bit_field = self.REG_PC['BBEN']
        if value is not None:
            self._register(addr, bit_field, value)
        else:
            value = self._register(addr, bit_field)
        return value

    def irqs(self):
        addr = self.IRQ_REG_ADDR[self.band]
        value = self.parent.read_u8(addr)
        return self.reg_to_dict(self.REG_IRQS, value)

    def irqm(self, value):
        return self._register(0x00, value = value)

    def fsk_symbol_rate(self, value=None):
        addr = self.REG_FSKC1['addr']
        bit_field = self.REG_FSKC1['SRATE']
        if value is not None:
            self._register(addr, bit_field, value)
        else:
            value = self._register(addr, bit_field)
        return value

    def fsk_preamble_length(self, byte_cnt=None):
        REG_FSKPLL = 0x65
        addr = self.REG_FSKC1['addr']
        bit_field = self.REG_FSKC1['FSKPLH']
        if byte_cnt is not None:
            self._register(addr, bit_field, (byte_cnt>>8)&0x03)
            self._register(REG_FSKPLL, None, byte_cnt&0x00FF)
        else:
            byte_cnt = self._register(addr, bit_field)<<8
            byte_cnt += self._register(REG_FSKPLL, None)
        return byte_cnt

    def fsk_sfd(self, sfd=None):
        REG_FSKSFD0L = 0x66 +  self.base_addr
        if sfd is None:
            sfd = self.parent.read_u16(REG_FSKSFD0L)
        else:
            self.parent.write_u16_r(REG_FSKSFD0L, sfd)
        return sfd


class AT86RF215(COM_SPI, multibyte):

    WHO_IAM_REG = 0x0d
    WHO_IAM_ANSWER = 0x35
    READ_CMD = 0x00
    WRITE_CMD = 0x80
    MULTIPLEBYTE_CMD = 0x00
    #
    # Identifies Transceiver mode
    # Each transceiver can be in one of these modes
    #
    BASE_BAND = 1   # IQ data generated in the chip
    IQ_RADIO = 2    # IQ data provided/returned over LVDS to/from the chip
    REG_RF_IQIFC1= {
        'addr': 0x0b,
        'CHPM':{
            'shift':4,
            'mask': 0x70,
            'RF_MODE_BBRF': 0,
            'RF_MODE_RF':  1,
            'RF_MODE_BBRF09': 4,
            'RF_MODE_BBRF24': 5
        },
    }
    FSK_SRATE_CONF = {
        # Sequence is for version 3 chips
        # Page 88 of datasheet
        # FSKC1.SRATE
        # TXDFE.SR
        # RXDFE.SR
        50:  [0, 8,  10],
        100: [1, 4,   5],
        150: [2, 2,   4],
        200: [3, 2,   4],
        300: [4, 1,   2],
        400: [5, 1,   2],
    }

    PART_NR = {0x34:"AT86RF215", 0x35:"AT86RF215IQ", 0x36:"AT86RF215M"}

    DEFAULT_CONF = (
        (0x0007, 0),    # Switch clock off
    )

    def __init__(self, communication, dev_selector, debug = False):
        self.DEBUG=debug
        super().__init__(communication, dev_selector,
                         addr_size=self.ADDR_MODE_16,
                         msb_first=self.TRANSFER_MSB_FIRST)
        self.transceiver={}
        self.transceiver['RF09'] =RF_TRANCEIVER(self, 'RF09', debug)
        self.transceiver['RF24'] =RF_TRANCEIVER(self, 'RF24', debug)
        self.baseband={}
        self.baseband['RF09'] =BASEBAND(self, 'RF09', debug)
        self.baseband['RF24'] =BASEBAND(self, 'RF24', debug)
        self.part_nr = self.PART_NR[self.read_u8(0x0d)]
        self.version = self.read_u8(0x0e)
        if self.version == 1:
            raise NotImplementedError("%s version %d is not supported" % (self.part_nr, self.version))
        if self.DEBUG:
            print("Detected %s version %d" % (self.part_nr, self.version))

    def setup_freq_default(self):
        for tr in self.transceiver.values():
            tr.setup_freq_default()

    def _register(self, addr, bit_field, value=None):
        current_value = self.read(addr)
        if bit_field is None:
            shift = 0
            mask = 0xFF
        else:
            shift= bit_field['shift']
            mask = bit_field['mask']
        if value == None:
            value = current_value
            value &= mask
            value>>= shift
        else:
            value <<= shift
            value &= mask
            value |= (current_value & ~mask)
            if value != current_value:
                self.write(addr, value)
        return value


    def reset(self):
        self.write(0x05, 0x07)

    def chip_mode(self, mode=None):
        '''
        Configuration of the transceivers.
        '''
        if mode is not None and mode not in self.REG_RF_IQIFC1['CHPM'].keys():
            raise ValueError("Unknown chip mode: 0x%02x" % (mode))
        addr = self.REG_RF_IQIFC1['addr']
        bit_field = self.REG_RF_IQIFC1['CHPM']
        if mode is not None:
            value = bit_field[mode]
            self._register(addr, bit_field, value)
        else:
            value = self._register(addr, bit_field)
            mode = key_from_value(bit_field, value)
        return mode

    def transceiver_state(self, transceiver):
        '''
        Get state of a transceiver.
        '''
        return self.transceiver[transceiver].state()


    def transceiver_command(self, transceiver, command):
        '''
        Execute command on a transceiver for state change.
        '''
        return self.transceiver[transceiver].command(command)

    def freq(self, transceiver, freq_hz):
        return self.transceiver[transceiver].freq(freq_hz)

    def sample_rate(self, transceiver, is_rx, value=None):
        return self.transceiver[transceiver].sample_rate(is_rx, value)

    def tx_lowpass(self, transceiver, mode=None):
        return self.transceiver[transceiver].tx_lowpass(mode)

    def rx_bw_if(self, transceiver, mode=None):
        return self.transceiver[transceiver].rx_bw_if(mode)

    def rx_if_shift(self, transceiver, mode=None):
        return self.transceiver[transceiver].rx_if_shift(mode)

    def digi_cut_off(self, transceiver, is_rx, value=None):
        return self.transceiver[transceiver].digi_cut_off(is_rx, value)

    def pa_power(self, transceiver, value=None):
        return self.transceiver[transceiver].pa_power(value)

    def rssi(self, transceiver):
        return self.transceiver[transceiver].rssi()

    def phy(self, band, mode=None):
        return self.baseband[band].phy(mode)

    def irqs(self, band):
        return self.baseband[band].irqs()

    def bb_en(self, band, value=None):
        return self.baseband[band].enable(value)

    def fsk_symbol_rate(self, band, symbol_rate):
        conf = self.FSK_SRATE_CONF[symbol_rate]
        self.baseband[band].fsk_symbol_rate(conf[0])
        self.transceiver[band].sample_rate(False, conf[1])
        self.transceiver[band].sample_rate(True, conf[2])

    def fsk_preamble_length(self, band, byte_cnt=None):
        return self.baseband[band].fsk_preamble_length(byte_cnt)

    def fsk_sfd(self, band, sfd=None):
        return self.baseband[band].fsk_sfd(sfd)

    def rx_iq_mode(self, band):
        self.transceiver[band].irqm(0x3F)
        self.chip_mode('RF_MODE_RF')
        self.rx_bw_if(band, 'RF_BW2000KHZ')
        self.rx_if_shift(band, 1)
        self.sample_rate(band, True, '4000KSPS')
        self.digi_cut_off(band, True, "FS/2")
        # SET AGC?
        # Frequency is already set
        self.transceiver_command(band, "RF_TXPREP")
        status = self.transceiver[band].irqs()
        timeout = 10
        while status['TRXRDY'] !=0:
            print("TRXRDY: %d" % (status['TRXRDY']))
            time.sleep(0.1)
            timeout-=1
            if timeout==0:
                break
            status = self.transceiver[band].irqs()
        if timeout>0:
            self.transceiver_command(band, "RF_RX")
        return timeout>0



