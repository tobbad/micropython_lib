

import pyb
import os
import struct

class Matrix_Server():
    ##
    #   Following functions convert this class in a 
    #   USB_VCP controlled device
    #   As client use the led_matrix_client class 
    #   on the host.
    #
    def get_cmd_from_client(self):
        data = b''
        data_ready=False
        while not data_ready:
            byte = self.com.readline()
            if not byte:
                continue
            data +=byte 
            if self.DEBUG:
                bStr = "".join([" 0x%02x"% i for i in byte ])
                print("Received byte: %s" % bStr)
            for b in byte:
                if  b in ( 0x0d, 0x0a):
                    data = data[:-1]
                    data_ready = True
        return data

    def _check_buf(self, buf, fmt):
        ans_len = len(fmt)
        fmt_len = struct.calcsize(fmt)
        if len(buf) < fmt_len:
            return [ None for i in range(ans_len) ]
        else:
            return struct.unpack(fmt, buf)
        
    def get_coord(self, buf):
        fmt = "HH"
        fmt_size = struct.calcsize(fmt)
        x, y = self._check_buf(buf, fmt)
        if x == None:
            fmt_size=0
        return x, y, fmt_size

    def get_rgb(self, buf):
        fmt = "BBB"
        fmt_size = struct.calcsize(fmt)
        r, g, b = self._check_buf(buf, fmt)
        if r==None:
            fmt_size  =0
        return r,g,b, fmt_size

    def get_string(self, buf):
        fmt = "B"
        fmt_size = struct.calcsize(fmt)
        str_len = self._check_buf(buf, fmt)[0]
        if str_len == None:
            text  = None
            fmt_size = 0
            if self.DEBUG:
                print("No size field found")
        else:
            fmt = "%ds" % str_len
            fmt_size += struct.calcsize(fmt)
            if self.DEBUG:
                print("String format is \"%s\" with total lenght %d" % (fmt, fmt_size))
            text = struct.unpack(fmt, buf[1:])[0]
            text = "".join([chr(i) for i in text])
            if self.DEBUG:
                print("Found string \"%s\"  total size %d" % (text, fmt_size))
            if not text:
                text  = None
                fmt_size = 0
        return text, fmt_size

    def server(self):
        led = pyb.Pin('PC15', mode=pyb.Pin.OUT_PP)
        self.show()
        self.com = pyb.USB_VCP()
        if not self.com.isconnected():
            led.low()            
            print("No client connected")
        else:
            led.high()
        # This is a raw data stream .. os disable the CTRL-C interrupt
        self._com.setinterrupt(-1)
        HELLO, WIDTH, HEIGHT, DEPTH, PIXEL, FILL, CLEAR, TEXT = range(48, 48+8)
        ANSW_OK, ANSW_ERROR  = b'\0', b'\1'
        while True:
            answ = ANSW_OK
            data = self.get_cmd_from_client()
            if not data or len(data) == 0:
                continue
            data_idx = 0
            cmd = data[data_idx]
            data_idx +=1
            if self.DEBUG:
                print("Received command: %d" % cmd)
            if cmd == HELLO:
                text = bytes(os.uname()[-1], 'utf-8')
                answ += struct.pack('B', len(text))
                answ += text
            elif cmd == WIDTH:
                answ += struct.pack("H", self._width)
            elif cmd == HEIGHT:
                answ += struct.pack("H", self._height)
            elif cmd == DEPTH:
                answ += struct.pack("H", self._depth)
            elif cmd == PIXEL:
                x, y, cnt = self.get_coord(data[data_idx:])
                data_idx += cnt
                if cnt == 0:
                    answ = ANSW_ERROR
                else:
                    r, g, b, cnt = self.get_rgb(data[data_idx:])
                    data_idx += cnt
                    if cnt == 0:
                        color = self.pixel((x,y) )
                        answ += struct.pack('BBB', color[0], color[1], color[2])
                    else:
                        self.pixel((x,y), (r,g,b))
            elif cmd == FILL:
                r, g, b, cnt = self.get_rgb(data[data_idx:])
                data_idx += cnt
                if cnt == 3:
                    self.fill((r,g,b))
                else:
                    answ = ANSW_ERROR
            elif cmd == CLEAR:
                self.clear()
            elif cmd == TEXT:
                text, cnt = self.get_string(data[data_idx:])
                data_idx += cnt
                if cnt != 0:
                    x, y, cnt = self.get_coord(data[data_idx:])
                    data_idx += cnt
                    if cnt == 0:
                        answ = ANSW_ERROR
                    else:
                        r, g, b, cnt = self.get_rgb(data[data_idx:])
                        data_idx += cnt
                        if cnt == 3:
                            self.text(text, (x,y), (r,g,b))
                else:
                    answ = ANSW_ERROR
            else:
                answ = ANSW_ERROR
                
            answ+=b'\x0d\x0a'
            self.com.write(answ)
            if self.DEBUG:
                bStr = "".join([" 0x%02x"% i for i in answ ])
                print("Send bytes: %s" % bStr)
   
