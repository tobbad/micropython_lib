#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    HW server stubs for different HW items on python board.
    Created on 8.7.2016
    @author: Tobias Badertscher

"""

class server:

    def __init__(self):
        ''' Create USB_VCP device on the python board as
        server for the client on the PC.'''
        self._com = pyb.USB_VCP()
        if not self._com.isconnected():
            print("No client connected")
        # This is a raw data stream .. os disable the CTRL-C interrupt
        self._com.setinterrupt(-1)

    def _l2str(self, data):
        hex_str = " ".join(["0x%02x" % (ord(i) ) for i in data])
        text_str = "".join(["%s" % (i if i.isalnum() else '.') for i in data])
        return hex_str +"\n" + text_str

    def clear_serial(self):
        data = 1
        while data:
            data=self._com.read()

    def read(self, cnt):
        return self._com.read(cnt)

    def write(self, data):
        if self.DEBUG:
            bStr = " ".join(["0x%02x" % i for i in data])
            print("Send bytes: %s" % bStr)
        for item in data:
            if item == self.ESC:
                self._com.write(self.ESC)
            self._com.write(item)
        return

    def ioctl(self, cmd, data=None):
        self._com.write(self.ESC)
        self._com.write(cmd)
        self._com.write(len(data))
        self.write(data)

    def run(self):
        if not self._com.isconnected():
            print("No client connected")
        # This is a raw data stream .. os disable the CTRL-C interrupt
        self._com.setinterrupt(-1)
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
            self._com.write(answ)
            if self.DEBUG:
                bStr = "".join([" 0x%02x"% i for i in answ ])
                print("Send bytes: %s" % bStr)
   

