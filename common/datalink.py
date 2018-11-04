#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Datalink layer which does the framing , escape and CRC check.
    Created on 8.7.2016
    
    Packet looks as follows:
    | Start of Frame byte(s) [...] | packet_type byte [One of Datalink.PACKET_TYPE]| PACKET_LENGTH | data* N bytes | CRC 1 byte|
    Packet type, Packe Length CRC and EOF si optional. 
    Escape is optional and only done when a ESC enbtry is given by the ESCAPE dictionary
    packet_type is NOT escaped by the Datalink.ESCAPE characters.
    Datafield is escaped to not contain one of the Datalink.ESCAPE characters.
    CRC is calculated over full header and data fields.
    
    @author: Tobias Badertscher
"""
import struct
from time import sleep
import logging

class Datalink:
    
    DEBUG = False
    
    ESCAPE = {
        'SOF': [0x01,],
        'EOF': [0x04,], # Only 1 entry currently supported
        'ESC': [0x1B,], # Only allowed to have 1 entry!
    }
    
    PACKET_TYPE = {
        'DATA': 48,
        'CONTROL':49,
        }

    STATES = {'ACK': 0, 'NACK': 128 }
    
    USE_CRC = True
    USE_PACKET_TYPE = True
    USE_LENGTH_FIELD = False
    INCLUDE_HEADER_IN_LENGTH = True
    
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
        self._log = logging.getLogger("Datalink")
        self.retry_cnt =retry_cnt
        self._baudrate = baudrate
        self.DEBUG = debug        
        self.__phy = phy
        self.REV_ESC_MAP={}
        self.ESC_MAP={}
        self._header_size = len(self.ESCAPE['SOF'])
        self._header_size += 1 if self.USE_PACKET_TYPE else 0
        self._header_size += 1 if self.USE_LENGTH_FIELD else 0
        if 'ESC' in self.ESCAPE:
            val = []
            for i in self.ESCAPE.values():
                val.extend(i)
            val.sort()
            for i, v in enumerate(val):
                self.ESC_MAP[v] = (0x1B, 0x30+i)
                self.REV_ESC_MAP[0x30+i] = v
        self.raw_data = b''
        if self.DEBUG:
            self._log.debug("Created")

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

    def crc(self, data, crc=None):
        ''' Calculate CRC from polynom x^8+x^7+x^6+x^4+x^2+1
        '''
        if crc is None:
            crc = 0x00
        for byte in data:
            crc = self.add_to_crc(byte, crc)
        return crc
    
    def header(self, packet_type, payload_size):
        if packet_type not in self.PACKET_TYPE:
            raise ValueError("Unknown packet type %d" % packet_type)
        header = self.ESCAPE['SOF'][:]
        if self.USE_PACKET_TYPE:
            header.append(self.PACKET_TYPE[packet_type])
        if self.USE_LENGTH_FIELD:
            if self.INCLUDE_HEADER_IN_LENGTH:
                payload_size += self._header_size
            header.append(payload_size)
        return header
        
    def write_raw(self, data, packet_type):
        if isinstance(data,  int):
            data = [data, ]
        if isinstance(data,  str):
            try:
                data = bytearray(data, 'ascii')
            except:
                data = bytearray(data)
        if data is None:
            return 0
        payload =[]
        for item in data:
            val = self.ESC_MAP.get(item, [item,])
            payload.extend(val)
        packet = self.header(packet_type, len(payload))
        crc = self.crc(packet[len(self.ESCAPE['SOF']):])
        crc = self.crc(data, crc)
        packet.extend(payload)
        if self.USE_CRC:
            crc = self.ESC_MAP.get(crc, [crc,])
            packet.extend(crc)
        if 'EOF' in self.ESCAPE:
            packet.extend(self.ESCAPE['EOF'])
        elif not self.USE_LENGTH_FIELD:
            raise ValueError("Can not produce package without length and without END OF FRAME (EOF")
        fmt = "%dB" % len(packet)
        packet = struct.pack(fmt,  *packet)
        byte_cnt = self.__phy.write(packet)
        if self.DEBUG:
            self._log.debug("Raw written \"%s\"" % (packet))
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
        length_index  = len(self.ESCAPE['SOF'])
        length_index += (1 if self.USE_PACKET_TYPE else 0)
        res = []
        result = None
        is_escape = False
        sof_idx = 0
        packet_type = None
        type_index = len(self.ESCAPE['SOF']) 
        exp_pkt_length = 0
        pkt_index = 0
        unparsed_data = b''
        end_of_pkt = False
        if self.DEBUG:
            self._log.debug("Scan data of lenght %d" % (len(data)))
        for idx, character in enumerate(data):
            log_start=""
            if self.DEBUG:
                pchr = '%s' % chr(character) if 32<=character<127 else '.'
                log_start = "CHAR[%2d] 0x%02x (%s)" % (idx, character,  pchr)
            if sof_idx < len(self.ESCAPE['SOF']) and \
               character == self.ESCAPE['SOF'][sof_idx]:
                pkt_index = sof_idx
                if self.DEBUG:
                    self._log.debug("%s  ==> SOF[%d/%d]" % (log_start, sof_idx, len(self.ESCAPE['SOF'])) )
                sof_idx += 1
                continue
            if sof_idx < len(self.ESCAPE['SOF']):
                sof_idx = 0
                if self.DEBUG:
                    self._log.debug("%s  ==> SKIP" % (log_start)  )
                continue
            pkt_index += 1
            # End of packet
            if is_escape:
                res.append(self.REV_ESC_MAP[character])
                if self.DEBUG:
                    self._log.debug("%s  ==> Escape 0x%02x 0x%02x ==> 0x%02x" % (log_start, self.ESCAPE['ESC'][0] ,character, res[-1]))
                is_escape = False
            else:
                if 'ESC' in self.ESCAPE and character == self.ESCAPE['ESC'][0]:
                    if self.DEBUG:
                        self._log.debug("%s  ==> ESCAPE (0x%02x)" % (log_start, self.ESCAPE['ESC'][0]))
                    is_escape = True
                    continue
                else:
                    if self.DEBUG:
                        self._log.debug("%s  ==> Data(0x%02x)" % (log_start, character))
                    res.append(character)
            if (self.USE_LENGTH_FIELD is True) and (pkt_index == length_index):
                exp_pkt_length = res[-1]
                if not self.INCLUDE_HEADER_IN_LENGTH:
                    exp_pkt_length += self._header_size
                if self.DEBUG:
                    self._log.debug("%s      ==> PACKERLENGTH(0x%02x)" % (log_start, exp_pkt_length))
            if (self.USE_PACKET_TYPE is True) and (pkt_index == type_index):
                packet_type = res[-1]
                if self.DEBUG:
                    self._log.debug("%s      ==> PACKETTYPE(0x%02x)" % (log_start, packet_type))
            if ('EOF' in self.ESCAPE) and (character == self.ESCAPE['EOF'][0]):
                end_of_pkt = True
                if self.DEBUG:
                    self._log.debug("%s  ==> REMOVE EOF" % (log_start))
                res = res[:-1]
            if (pkt_index == exp_pkt_length):
                end_of_pkt = True
            if end_of_pkt:  
                if self.DEBUG:
                    self._log.debug("%s  ==> End of Packet %d" % (log_start, len(res)))
                if len(res) < 2:
                    data_str = ", ".join(["0x%02x" % d for d in res ])
                    raise Exception("Data (%s) too short" % data_str)
                unparsed_data = data[idx+1:]
                if self.USE_CRC:
                    remote_crc = res[-1]
                    my_crc=self.crc(res[:-1])
                    if self.DEBUG:
                        self._log.debug("%s  ==> Check CRC: 0x%02x == 0x%02x (%s)"
                              %(log_start, my_crc, remote_crc,
                                "OK" if my_crc == remote_crc else "FAIL") )
                    if my_crc != remote_crc:
                        if self.DEBUG:
                            self._log.debug("%s  ==> CRCs Do not match" % (log_start))
                        if self.USE_PACKET_TYPE  and (packet_type == self.PACKET_TYPE['DATA']):
                            if self.DEBUG:
                                self._log.debug("%s  ==> CRC for data does not match: NACK" % (log_start)) 
                            if 'NACK' in self.STATES:
                                self.send_state('NACK')
                        return None, None, unparsed_data
                if packet_type == self.PACKET_TYPE['DATA']:
                    if self.DEBUG:
                        self._log.debug("%s  Send ACK" % (log_start))
                    if 'ACK' in self.STATES:
                        self.send_state('ACK')
                start_idx = self._header_size -len(self.ESCAPE['SOF'])
                result = res[start_idx:-1] # Remove CRC and header without SOF
                break
        if result is  None:
            packet_type = None
            unparsed_data = data
        return packet_type,  result,  unparsed_data
     
     
    def read_raw(self, timeout=1.0):
        ''' Read data form the communication interface
        '''
        sleep_step_s = timeout/self.retry_cnt
        timeout= max(timeout, sleep_step_s)
        packet_type = None
        result = None
        wait_time_s = 0
        while wait_time_s < timeout:
            new_data = b''
            while self.__phy.any():
                new_data += self.__phy.read()
                if self.DEBUG and new_data is not None:
                    self._log.debug("New data %s" % (new_data))
            if new_data is None or len(new_data) == 0:
                sleep(sleep_step_s)
                wait_time_s += sleep_step_s
                continue
            else:
                self.raw_data += new_data
            packet_type,  result, self.raw_data = self.scan_raw_data(self.raw_data)
            if packet_type is not None:
                break
            if result is not None:
                break
        if self.DEBUG and result is not None:
            self._log.debug("Received: %s (wait %f s)" % (bytearray(result), wait_time_s))
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
