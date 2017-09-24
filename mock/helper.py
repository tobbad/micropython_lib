#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Unit test stub module
#
import crcmod.predefined
import struct

lib_crc = crcmod.predefined.mkCrcFun('crc-8-wcdma')


def calc_crc(data):
    fmt = ("%dB" % len(data))
    data_bin = struct.pack(fmt, *data)
    return lib_crc(data_bin)
