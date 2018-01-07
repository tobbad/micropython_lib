#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Datalink layer which does the framing , escape and CRC check.
    Created on 8.7.2016
    
    Packet looks as follows:
    | Start of Frame byte [0x01] | packet_type byte [One of Datalink.PACKET_TYPE] | data* N bytes | CRC 1 byte|
    packet_type is NOT escaped by the Datalink.ESCAPE characters.
    Datafield is escaped to not contain one of the Datalink.ESCAPE characters.
    CRC is calculated over packet_type AND data fields.
    
    @author: Tobias Badertscher
"""
import struct
from time import sleep

class Datalink:
    
    DEBUG = False
    
    ESCAPE = {
        'SOF': 0x01,
        'EOF': 0x04,
        'ESC': 0x1B,
    }
    
    PACKET_TYPE = {
        'DATA': 48,
        'CONTROL':49,
        }
    
    STATES = {'ACK': 0, 'NACK': 128 }
    
    ESC = 0x1B

    CRC_QUOTIENT = 0xD9     # This is the quotient for CRC-8 WCDMA 
    
    def __init__(self,  phy, retry_cnt=5, baudrate=115200, debug=False):
        ''' Constructor
        phy: Low level physical interface with minimal functions:
             read: Read available chars and return as byte buffer,
             write: Write byte buffer to the phy
             any: Return True if there are any characters waiting for reading
        retry_cnt: Count of retries that should be done on the interface till 
                   None is returned for reading. The total time out will therefore
                   be retry_cnt*Timeout_on_phy
        debug: Either True or False: Output debug information.
        '''
        self.retry_cnt =retry_cnt
        self._baudrate = baudrate
        self.DEBUG = debug        
        self.__phy = phy
        self.REV_ESC_MAP={}
        self.ESC_MAP={}
        val = [ i for i in self.ESCAPE.values()]
        val.sort()
        for i, v in enumerate(val):
            self.ESC_MAP[v] = (0x1B, 0x30+i)
            self.REV_ESC_MAP[0x30+i] = v
        self.raw_data = b''

    def add_to_crc(self, byte, crc):
        b2 = byte
        if (byte < 0):
            b2 = byte + 256
        for i in range(8):
            odd = ((b2^crc) & 0x01) == 0x01
            crc >>= 1
            b2 >>= 1
            if (odd):
                crc ^= self.CRC_QUOTIENT 
        return crc

    def crc(self, data):
        ''' Calculate CRC from polynom x^8+x^7+x^6+x^4+x^2+1
        '''
        crc = 0x00
        for byte in data:
            crc = self.add_to_crc(byte, crc)
        return crc
    
    def header(self, packet_type):
        if packet_type not in self.PACKET_TYPE:
            raise ValueError("Unknown packet type %d" % packet_type)
        return [self.ESCAPE['SOF'], self.PACKET_TYPE[packet_type]]
        
    def write_raw(self, data, packet_type):
        if isinstance(data,  int):
            data = [data, ]
        if isinstance(data,  str):
            try:
                data = bytearray(data, 'ascii')
            except:
                data = bytearray(data)
        res = self.header(packet_type)
        for item in data:
            val = self.ESC_MAP.get(item, [item,])
            res.extend(val)
        crc = self.crc(data)
        res.extend(self.ESC_MAP.get(crc, [crc,]))
        res.append(self.ESCAPE['EOF'])
        fmt = "%dB" % len(res)
        res = struct.pack(fmt,  *res)
        byte_cnt = self.__phy.write(res)
        if self.DEBUG:
            print("Raw written \"%s\"" % (res))
        return byte_cnt
        

    def write(self, data):
        '''Send data in a frame to the phy.
        data: int, list or tuple of data to be sent
        
        return True on ACK from other side
               False on NACK from other side
               None if no answer from other side after retry_cnt of tries.'''
        self.write_raw(data, 'DATA')
        state = self.recv_state()
        if self.DEBUG:
            print("Final write state: %s" % state)
        if state is not None:
            state = state == self.STATES['ACK']
        return state
            
    def send_state(self, state):
        if state not in self.STATES:
            raise ValueError("Unknown control status %s" % state)
        self.write_raw([self.STATES[state],], 'CONTROL')
        
    def scan_raw_data(self,  data):
        ''' Scan data to the package structure
        - Drop all bytes up to SOF 
        - Check packet type
        - Read data up to EOF and unescape content
        - Check CRC of packet_type and data:
            - ACK data package with matching CRC
            - NACK data package with not matching CRC
        - Do not send any ACK/NACK on control packets
        - Return packet_type, result data and unparsed data.
        '''
        res = []
        result = None
        is_escape = False
        sof_detected = False
        packet_type = None
        unparsed_data = b''
        if self.DEBUG:
            print("Scan data of lenght %d" % (len(data)))
        for idx, character in enumerate(data):
            if self.DEBUG:
                pchr = '%s' % chr(character) if 32<=character<127 else '.'
                print("CHAR 0x%02x (%s)" % ( character,  pchr), end="")
            if character == self.ESCAPE['SOF']:
                sof_detected = True
                if self.DEBUG:
                    print("  ==> SOF" )
                continue
            if not sof_detected:
                if self.DEBUG:
                    print("  ==> SKIP" )
                continue
            if packet_type is None:
                if self.DEBUG:
                    print("  ==> PACKET Type 0x%02x" % character )
                packet_type = character
                continue
            if character == self.ESCAPE['EOF']:
                if self.DEBUG:
                    print("  ==> EOF Datasize %d" % len(res))
                if len(res) < 2:
                    data_str = ", ".join(["0x%02x" % d for d in res ])
                    raise Exception("Data (%s) too short" % data_str)
                unparsed_data = data[idx+1:]
                remote_crc = res[-1]
                my_crc=self.crc(res[:-1])
                if self.DEBUG:
                    print("  ==> Check CRC: 0x%02x == 0x%02x (%s)" 
                          %(my_crc, remote_crc, 
                            "OK" if my_crc == remote_crc else "FAIL") )
                if my_crc != remote_crc:
                    if self.DEBUG:
                        print("  ==> CRC Does not match")
                    if packet_type == self.PACKET_TYPE['DATA']:
                        if self.DEBUG:
                            print("  ==> CRC for data does not match: NACK") 
                        self.send_state('NACK')
                    return None, None, unparsed_data
                if packet_type == self.PACKET_TYPE['DATA']:
                    if self.DEBUG:
                        print("  Send ACK")
                    self.send_state('ACK')
                result = res[:-1] # Remove CRC
                break
            if is_escape:
                res.append(self.REV_ESC_MAP[character])
                if self.DEBUG:
                    print("  ==> Escape 0x%02x 0x%02x ==> 0x%02x" % (self.ESC ,character, res[-1]))
                is_escape = False
                continue
            else:
                if character == self.ESC:
                    if self.DEBUG:
                        print("  ==> ESCAPE (0x%02x)" % (self.ESC))
                    is_escape = True
                    continue
                else:
                    if self.DEBUG:
                        print("  ==> Data(0x%02x)" % (character))
                    res.append(character)
                    continue
        if result is  None:
            packet_type = None
            unparsed_data = data
        return packet_type,  result,  unparsed_data
     
     
    def read_raw(self, timeout=1.0):
        ''' Read data form the communication interface
        '''
        sleep_step_s = 0.005
        packet_type = None
        result = None
        wait_time_s = 0
        while wait_time_s < timeout:
            while self.__phy.any():
                self.raw_data += self.__phy.read()
            if len(self.raw_data) == 0:
                sleep(sleep_step_s)
                wait_time_s += sleep_step_s
                continue
            packet_type,  result, self.raw_data = self.scan_raw_data(self.raw_data)
            if packet_type is not None:
                break
        if self.DEBUG and result is not None:
            print("Received %s : %s (wait %f s)" % (str(packet_type),  result, wait_time_s))
        return packet_type, result
    
    
    def read(self):
        packet_type = self.PACKET_TYPE['CONTROL']
        while ( packet_type is not None ) and \
              packet_type == self.PACKET_TYPE['CONTROL']:
            packet_type, data = self.read_raw()
        return data
    
    def read_str(self):
        data = self.read()
        if isinstance(data, list):
            data = "".join([chr(i) for i in data])
        return data

    def recv_state(self):
        res = None
        packet_type, data = self.read_raw()
        if packet_type is not None and packet_type == self.PACKET_TYPE['CONTROL']:
            res = data[0]
            if self.DEBUG:
                print("Received state 0x%02x" % ( res ))
        return res
           
    def echo(self):
        data = self.read()
        self.write(data)
