#
# Emulate a SPI interface by directly manipulate IO Pins
#
import pyb

class SPI:

    DEBUG = True
    def __init__(self, SCK, MOSI, MISO, mode=pyb.SPI.MASTER, polarity=1, phase=0, firstbit = pyb.SPI.MSB, debug=True):
        if mode == pyb.SPI.SLAVE:
            raise ValueError("SPI slave is not supported for bit bang")
        self.mode = pyb.SPI.MASTER
        self.sck = SCK
        self.mosi = MOSI
        self.miso = MISO
        self.polarity = 1 if polarity>0 else 0
        self.phase = i if phase>0 else 0
        self.firstbit = pyb.SPI.LSB if firstbit == pyb.SPI.LSB else pyb.SPI.MSB
        self.sck.value(self.polarity)
        self.DEBUG=debug
        if self.DEBUG:
            print("firstbit = %s" % 'LSB' if self.firstbit == pyb.SPI.LSB else 'MSB')


    def _bus_io(self, in_data = None, out_data = None):
        if in_data is None and out_data is None:
            raise ValueError("in_data and out_data both None")
        cnt = len(in_data) if in_data is not None else len(out_data)
        if self.DEBUG:
            print("firstbit = %s" % 'LSB' if self.firstbit == pyb.SPI.LSB else 'MSB')
        for byte_nr in range(cnt):
            if self.DEBUG:
                print("Byte[%2d]:" % byte_nr)
            in_value = 0
            out_value = 0 if out_data is None else out_data[byte_nr]
            for bit_nr in range(8):
                shift_cnt = bit_nr if self.firstbit==pyb.SPI.LSB else (7-bit_nr)
                bit_value = 0 if (out_value&(1<<shift_cnt))==0 else 1
                clk_value = self.sck.value()
                self.sck.value(0 if clk_value>0 else 1)
                if self.phase == 0:
                    self.mosi.value(bit_value)
                    in_value |= self.miso.value()
                self.sck.value(clk_value)
                if self.phase == 1:
                    self.mosi.value(bit_value)
                    in_value |= self.miso.value()
                if self.DEBUG:
                    print(" > Bit[%d] = %d, %d" % (bit_nr, bit_value, shift_cnt))
            if in_data is not None:
                in_data[byte_nr] = in_value
        return in_data


    def recv(self, recv):
        if isinstance(recv, int):
            res =bytearray(recv)
        elif isinstance(recv, bytearray):
            res = recv
        else:
            raise ValueError("Unsupported recv datatyep %s" % (type(recv)))
        return self._bus_io(res)

    def send(self, send):
        if isinstance(send, int):
            data = [send,]
        elif isinstance(send, bytearray):
            data = send
        else:
            raise ValueError("Unsupported send datatyep %s" % (type(recv)))
        return self._bus_io(None, data)

    def send_recv(self, send, recv=None):
        if recv is None:
            recv = bytearray(len(send))
        return self._bus_io(send, recv)
