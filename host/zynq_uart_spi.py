#
# SPI for the remote control of a zynq spi item
#

class SPI:

    MASTER = 260
    SLAVE = 0
    LSB = 128
    MSB = 0

class ZYNQ_UART_SPI:

    DEBUG = True

    def __init__(self, phy, dev_nr=0, inst_nr=0,  mode=SPI.MASTER, polarity=1, phase=0, firstbit = SPI.MSB, debug=True):
        if mode == SPI.SLAVE:
            raise ValueError("SPI slave is not supported for bit bang")
        self.mode = SPI.MASTER
        self.polarity = 1 if polarity>0 else 0
        self.phase = 1 if phase>0 else 0
        self.firstbit = SPI.LSB if firstbit == SPI.LSB else SPI.MSB
        self.DEBUG=debug
        self.dev_nr = dev_nr
        self.inst_nr = inst_nr
        self.phy = phy
        self.cmd_fmt =  "spi_test -p "
        self.cmd_fmt += "-O " if self.polarity==0 else ""
        self.cmd_fmt += "-H " if self.phase==1 else ""
        self.cmd_fmt += "-D /dev/spidev%d.%d" % (self.dev_nr, self.inst_nr)
        self.cmd_fmt += " %s"

    def _bus_io(self, send_data = None, recv_data = None):
        if send_data is None and recv_data is None:
            raise ValueError("send_data and recv_data both None")
        cnt = len(send_data) if send_data is not None else len(recv_data)
        if send_data is None:
            send_data = bytearray(len(recv_data))
        if recv_data is None:
            recv_data = bytearray(len(send_data))
        data_str = " ".join(["0x%02x" % d for d in send_data])
        cmd = self.cmd_fmt % data_str
        self.phy.write(cmd)
        res = self.phy.read()
        #if self.DEBUG:
        print(res)
        res = eval(res[1].split('=')[1])
        for byte_nr, item in enumerate(res):
            send_data[byte_nr] = item[0]
            recv_data[byte_nr] = item[1]
            if self.DEBUG:
                print("Byte[%2d] send: 0x%02x recv: 0x%02x" % (byte_nr, item[0], item[1]))
        return recv_data

    def recv(self, recv):
        if isinstance(recv, int):
            res = bytearray(recv)
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
            raise ValueError("Unsupported send datatyep %s" % (type(send)))
        return self._bus_io(None, data)

    def send_recv(self, send, recv=None):
        if recv is None:
            recv = bytearray(len(send))
        return self._bus_io(send, recv)


