#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Unit test for at86rf215
#
import unittest
# DUT
from micropython_lib.rf.at86rf215 import AT86RF215, RF_TRANCEIVER, BASEBAND, mode_iter
# Helper
test_conf = 'zybo'

def create_dut(debug = False):
    dut = None
    if test_conf == 'zybo':
        from micropython_lib.boards.zybo.zybo import ZYBO
        dev_name = '/dev/ttyUSB1'
        zybo = ZYBO(dev_name, debug)
        dut = AT86RF215(zybo.spi, None, debug)
    else:
        raise ValueError("ONLY ZYBO configuration supported")
    return dut, zybo

@unittest.skip("Skipping control")
class CHECK_CONTROL(unittest.TestCase):

    DEBUG = False

    def setUp(self):
        dut, zybo = create_dut(self.DEBUG)
        self.dut = dut
        self.zybo = zybo
        self.dut.reset()

    def test_wakup_irq(self):
        # Wakeup IRQ on RF09?
        value = self.dut.read(0x00)
        self.assertEqual(value &0x01, 1)
        # Wakeup IRQ on RF24?
        value = self.dut.read(0x01)
        self.assertEqual(value &0x01, 1)

    def test_chip_modes(self):
        modes = AT86RF215.REG_RF_IQIFC1['CHPM']
        for mode,v in mode_iter(modes):
            self.dut.chip_mode(mode)
            obt = self.dut.chip_mode(mode)
            self.assertEqual(obt, mode)
            value  = (self.dut.read(0x0b)>>4)&0x07
            self.assertEqual(value, v)
            self.dut.reset()
            value  = (self.dut.read(0x0b)>>4)&0x07
            self.assertEqual(value, AT86RF215.REG_RF_IQIFC1['CHPM']['RF_MODE_BBRF'])

    def test_get_transceiver_state(self):
        for tr in RF_TRANCEIVER.BAND.keys():
            obt = self.dut.transceiver_state(tr)
            self.assertTrue(obt in RF_TRANCEIVER.REG_STATE['STATE'].values())

    @unittest.skip("There is no equivalence between a command and a state")
    def test_set_command(self):
        for tr in RF_TRANCEIVER.BAND.keys():
            for cmd, value in mode_iter(RF_TRANCEIVER.REG_CMD['CMD']):
                self.dut.transceiver_command(tr, cmd)
                obt = self.dut.transceiver_state(tr)
                self.assertEqual(obt, cmd)


@unittest.skip("Skip frequency config")
class RF_FREQ_CONFIG(unittest.TestCase):

    DEBUG = False

    def setUp(self):
        dut, zybo = create_dut(self.DEBUG)
        self.dut = dut
        self.zybo = zybo
        self.dut.reset()
        self.dut.setup_freq_default()

    #@unittest.skip("Speed up")
    def test_freq_band(self):
        freq = {'RF09':((389000000, False, -1), (389500000, True, 1), (510000000, True, 1), (510100000, False, -1),
                        (778900000, False, -1), (779000000, True, 2),(1019900000, True, 2), (1020000000, True, 2),(1020100000, False, -1)),
                'RF24':((2399900000, False, -1), (2400000000, True,3 ), (2483500000, True, 3), (2483600000, False, -1))
                }
        for band, v in freq.items():
            for freq_hz, exp, exp_cnm_cm in v:
                freq_ok_obt, cnm_cm_obt = self.dut.transceiver[band].check_freq(freq_hz)
                self.assertEqual(freq_ok_obt, exp, "Freq: %.2f MHz, Obt != Exp" %(freq_hz/1E6))
                self.assertEqual(cnm_cm_obt, exp_cnm_cm, "CMM.CM: %.2f MHz, Obt != Exp" %(freq_hz/1E6))

    #@unittest.skip("Speed up")
    def test_base_freq(self):
        freq = {'RF09':868000000, 'RF24':2440000000}
        for band in RF_TRANCEIVER.BAND.keys():
            b_freq = freq[band]
            reg_addr = self.dut.transceiver[band].base_addr + 5
            obt = (self.dut.transceiver[band].base_freq(b_freq) - self.dut.transceiver[band].FREQ_OFFSET_HZ[band])
            obt /= self.dut.transceiver[band].FREQ_RESOLUTION_HZ
            obt = int(round(obt))
            low_obt = self.dut.read_u8(reg_addr)
            hi_obt = self.dut.read_u8(reg_addr+1)
            self.assertEqual(obt>>8, hi_obt, "High base freq byte not correct")
            self.assertEqual(obt&0x00FF, low_obt, "Low base freq byte not correct")
            freq_obt = self.dut.transceiver[band].base_freq()
            self.assertEqual(freq_obt, b_freq, "Returned base frequency not correct")

    #@unittest.skip("Speed up")
    def test_cannel_spacing(self):
        dfreq = {'RF09':200000, 'RF24':400000}
        for band in RF_TRANCEIVER.BAND.keys():
            df = dfreq[band]
            self.dut.transceiver[band].channel_spacing(df)
            obt = self.dut.transceiver[band].channel_spacing()
            self.assertEqual(obt, df)

    #@unittest.skip("Speed up")
    def test_channel(self):
        freq = {'RF09':(0,1,511), 'RF24':2440000000}
        for band in RF_TRANCEIVER.BAND.keys():
            for ch in 0,1,511:
                self.dut.transceiver[band].channel(ch)
                obt = self.dut.transceiver[band].channel()
                self.assertEqual(obt, ch)

    #@unittest.skip("Speed up")
    def test_freq(self):
        freq = {'RF09':868500000, 'RF24':2440000000}
        for band in RF_TRANCEIVER.BAND.keys():
            f = freq[band]
            self.dut.transceiver[band].freq(f)
            obt = self.dut.transceiver[band].freq()
            self.assertEqual(obt, f)

@unittest.skip("Skip frontend config")
class RF_FRONTEND_CONFIG(unittest.TestCase):

    DEBUG = False

    def setUp(self):
        dut, zybo = create_dut(self.DEBUG)
        self.dut = dut
        self.zybo = zybo
        self.dut.reset()
        self.dut.setup_freq_default()

    #@unittest.skip("Speed up")
    def test_push_state(self):
        for band in RF_TRANCEIVER.BAND.keys():
            self.dut.transceiver[band].push_and_new_state()
            self.assertRaises(Exception, self.dut.transceiver[band].push_and_new_state)

    #@unittest.skip("Speed up")
    def test_pop_state(self):
        for band in RF_TRANCEIVER.BAND.keys():
            self.assertRaises(Exception, self.dut.transceiver[band].pop_state)
            self.dut.transceiver[band].push_and_new_state()
            self.dut.transceiver[band].pop_state()

    #@unittest.skip("Speed up")
    def test_sample_rate(self):
        for band in RF_TRANCEIVER.BAND.keys():
            reg_addr = self.dut.transceiver[band].base_addr + 0x0A
            for is_rx in (True, False):
                if not is_rx:
                    reg_addr +=  (0x13-0x0a)
                for sr in range(5):
                    self.dut.sample_rate(band, is_rx, sr)
                    obt = self.dut.sample_rate(band, is_rx)
                    self.assertEqual(sr, obt)
                    reg_value = self.dut.read_u8(reg_addr)&0x0f
                    self.assertEqual(sr, reg_value)

    #@unittest.skip("Speed up")
    def test_digital_cut_off(self):
        for band in RF_TRANCEIVER.BAND.keys():
            reg_addr = self.dut.transceiver[band].base_addr + 0x0A
            for is_rx in (True, False):
                if not is_rx:
                    reg_addr +=  (0x13-0x0a)
                for cutoff, coff_val in mode_iter(self.dut.transceiver[band].REG_TXDFE['RCUT']):
                    self.dut.digi_cut_off(band, is_rx, cutoff)
                    obt = self.dut.digi_cut_off(band, is_rx)
                    self.assertEqual(cutoff, obt, "Read back cut off not correct")
                    reg_value = (self.dut.read_u8(reg_addr)&0xE0)>>5
                    self.assertEqual(coff_val, reg_value)

    #@unittest.skip("Speed up")
    def test_tx_low_pass(self):
        for tr in RF_TRANCEIVER.BAND.keys():
            for coff, value in mode_iter(RF_TRANCEIVER.REG_TXCUTC['LPFCUT']):
                self.dut.tx_lowpass(tr, coff)
                obt  =self.dut.tx_lowpass(tr)
                self.assertEqual(coff, obt)

    #@unittest.skip("Speed up")
    def test_rx_bw_if(self):
        for tr in RF_TRANCEIVER.BAND.keys():
            for mode, value in mode_iter(RF_TRANCEIVER.REG_RXBWC['BW']):
                self.dut.rx_bw_if(tr, mode)
                obt  =self.dut.rx_bw_if(tr)
                self.assertEqual(mode, obt)

    #@unittest.skip("Speed up")
    def test_pa_power(self):
        for band in RF_TRANCEIVER.BAND.keys():
            for p in range(0x1F):
                self.dut.pa_power(band, p)
                p_obt = self.dut.pa_power(band)
                self.assertEqual(p, p_obt)

    #@unittest.skip("Speed up")
    def test_rssi(self):
        for band in RF_TRANCEIVER.BAND.keys():
            exp_state = 'RF_RX'
            self.dut.transceiver_command(band, exp_state)
            obt_state = self.dut.transceiver_state(band)
            self.assertEqual(exp_state,obt_state)
            sum = 0
            for i in range(10):
                rssi_val = self.dut.rssi(band)
                self.assertTrue(rssi_val!=127, "Invalid RSSI value")
                sum+=rssi_val
            self.assertTrue(sum/i<=4)
            self.dut.transceiver_command(band, 'RF_TRXOFF')

@unittest.skip("Skip baseband config")
class RF_BASEBAND_CONFIG(unittest.TestCase):

    DEBUG = False

    def setUp(self):
        dut, zybo = create_dut(self.DEBUG)
        self.dut = dut
        self.zybo = zybo
        self.dut.reset()
        self.dut.setup_freq_default()

    @unittest.skip("Speed up")
    def test_set_phy(self):
        for band in RF_TRANCEIVER.BAND.keys():
            for phy, value in mode_iter(BASEBAND.REG_PC['PT']):
                self.dut.phy(band, phy)
                obt = self.dut.phy(band)
                self.assertEqual(phy, obt)

    @unittest.skip("Speed up")
    def test_read_irq(self):
        for band in RF_TRANCEIVER.BAND.keys():
            res = self.dut.irqs(band)
            self.assertIsNotNone(res)

    @unittest.skip("Speed up")
    def test_bben(self):
        for band in RF_TRANCEIVER.BAND.keys():
            for state in (1,0):
                self.dut.bb_en(band, state)
                obt = self.dut.bb_en(band)
                self.assertEqual(state, obt)

    @unittest.skip("Speed up")
    def test_set_fsk_symbol_rate(self):
        for band in RF_TRANCEIVER.BAND.keys():
            for rate in (50, 100, 150, 200, 300, 400):
                self.dut.fsk_symbol_rate(band, rate)

    @unittest.skip("Speed up")
    def test_fsk_preamble_length(self):
        for band in RF_TRANCEIVER.BAND.keys():
            for cnt in (1, 50, 100, 1000, 1023):
                self.dut.fsk_preamble_length(band, cnt)
                obt = self.dut.fsk_preamble_length(band)
                self.assertEqual(cnt, obt)

    @unittest.skip("Speed up")
    def test_fsk_sfd(self):
        for band in RF_TRANCEIVER.BAND.keys():
            for cnt in (0xFFFF, 0x0100, 0x55aa, 0xaa55):
                self.dut.fsk_sfd(band, cnt)
                obt = self.dut.fsk_sfd(band)
                self.assertEqual(cnt, obt)

    def test_rx_irq_mode(self):
        res = self.dut.rx_iq_mode('RF09')
        self.assertTrue(res)

#@unittest.skip("Skip RSD09 config")
class RXD09_CONFIG(unittest.TestCase):

    DEBUG = False

    def setUp(self):
        dut, zybo = create_dut(self.DEBUG)
        self.dut = dut
        self.zybo = zybo
        self.dut.reset()
        self.dut.setup_freq_default()
        self.base_addr = (0x43c00000, 0x43c10000)
        self.dut.rx_iq_mode('RF09')

    @unittest.skip("Speed up")
    def test_control_bits(self):
        bit_pos = [0,1,2,3,4,5,6,7,8, 16, 17, 18]
        register = 3
        for addr in self.base_addr:
            r_addr = addr+register*4
            for bshift in bit_pos:
                exp = 1<<bshift
                val1 = self.zybo.memory(r_addr)
                self.zybo.memory(addr+register*4, exp)
                val2 = self.zybo.memory(r_addr)
                self.assertTrue((val2&exp) !=0, "@ 0x%08x: Exp 0x%08x, Obt: 0x%08x" % (r_addr, exp, val2))
                self.zybo.memory(r_addr, val1)
            self.zybo.memory(r_addr, 0x3F)

    @unittest.skip("Speed up")
    def test_read_fifo(self):
        register = 0
        inst = 1
        r_addr = self.base_addr[inst]+register*4
        self.zybo.reset_fifo(inst,1)
        self.zybo.reset_fifo(inst,0)
        for i in range(16):
            val = self.zybo.memory(r_addr)
            self.assertEqual(i, val)
            print("%3d 0x%08x 0x%08x" % (i, r_addr, val))

    def test_read_data_fifo(self):
        register = 0
        inst = 0
        r_addr = self.base_addr[inst]+register*4
        self.zybo.reset_deser(inst,1)
        self.zybo.reset_deser(inst,0)
        for j in range(1):
            self.zybo.reset_fifo(inst,1)
            self.zybo.reset_fifo(inst,0)
            for i in range(16):
                #val = self.zybo.memory(r_addr)
                val = self.zybo.fifo(inst)
                #self.assertEqual(i, val)
                bval = "{0:032b}".format(val)
                print("%3d 0x%08x 0x%08x %s" % (i, r_addr, val, bval))
            self.zybo.bitslip(0)
        self.assertTrue(self.zybo.sync_rxd(inst))




if __name__ == '__main__':
    unittest.main()

