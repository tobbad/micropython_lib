#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Support functions for running a test.
    Created on 20.4.2016
    @author: Tobias Badertscher

"""
import os
import sys
import git
import subprocess
import glob
import serial
import re
import time

def cond_log(fd, data):
    if fd != None:
        if isinstance(data, (tuple, list)):
            fd.write(os.linesep.join(data))
        else:
            fd.write(data)
        fd.write("\n")
    return

def error_func(errList):
    print(os.linesep.join(errList))
    sys.exit()

def cmd_exec(cmd, path=".", env = None, verbose = True):
    '''
    Execute a command (tuple) in a subprocess and return
    the output as list
    '''
    cmdStr = " ".join(cmd)
    res = None
    if env == None:
        env = os.environ
    with subprocess.Popen(cmdStr, universal_newlines=True, env = env, shell=True, stdout = subprocess.PIPE, cwd=path) as proc:
        res = proc.stdout.read().split(os.linesep)
    if verbose:
        print("Command \"%s\" finished" % cmdStr)
    return res

def check_build_success(log):
    '''
    Check if build suceeded. Other posibility would be to check
    the existence of the firmware.elf file.
    '''
    return log[-2].split()[0]=='arm-none-eabi-objcopy'

def build_bin(swGitRepo, buildSubPath, board, error_function, fd = None, res = None):
    '''
    Clean build of the binary with the given info.
    '''
    cmdBuild = ["make","BOARD=%s" % board,"V=1"]
    cmdClean = cmdBuild[:]
    cmdClean.append( "clean" )
    buildPath = os.sep.join(swGitRepo+buildSubPath)
    res = cmd_exec(cmdClean, buildPath)
    cond_log(fd, res)
    res = cmd_exec(cmdBuild, buildPath)
    cond_log(fd, res)
    if not check_build_success(res):
        error_function(["Build did not succeed",])

def git_checkout_branch(swGitRepoPath, branch, error_function, fd = None):
    '''
    Check if branch exists, is not dirty and check it out.
    Return hash of last commit.
    '''
    if not os.path.exists(swGitRepoPath):
        error_function(["%s does not exist" % swGitRepoPath,])
    repo = git.Repo(swGitRepoPath)
    br = [str(r) for r in repo.branches]
    if branch not in br:
        error_function(["Branch \'%s\' does not exist" % branch,])
    if repo.is_dirty():
        error_function(["Branch \'%s\' is dirty." % branch,])
    if str(repo.active_branch) != branch:
        cond_log(fd, "Checkout branch %s" % branch)
        repo.git.checkout(branch)
    return str(repo.commit())

def scan_para(para, error_function):
    if len(para[0])<1:
        error_function(["No branch given",])
    branch = para[0][0]
    return branch

def get_usb_bus_dev(vendors):
    '''
    Get bus address and device number of the connected usb
    device for the given verndor list/tuple.
    '''
    res = []
    cmd_out = cmd_exec(["lsusb",])
    for line in cmd_out:
        if len(line)==0:
            continue
        line=line.split()
        vend, dev = (int(i,16) for i in line[5].split(':'))
        if vend in vendors:
            res.append( (int(line[1]), int(line[3].replace(':',''))))
    return res

def get_usb_bus_dev_old(vendor):
    '''
    Get bus address and device number of the connected usb
    device for the given verndor list/tuple.

    Does not work as bus adress and device number can not be retrieved
    from the data - or I do not knoe how (?).
    '''
    res = []
    busses = usb.busses()
    for bus in busses:
        devices = bus.devices
        for dev in devices:
            if dev.idVendor in vendor:
                res.append((bus, dev ))
    return res

def get_st_link_chip_id(usb_dev, fd=None):
    '''
    Get for the given usb devices (bus number, device address) tuples
    the chip ID with st-info utility. The information must be put in
    the 'STLINK_DEVICE' member variable to be used by the utility.
    '''
    res = {}
    env=os.environ
    for bus, devNr in usb_dev:
        env['STLINK_DEVICE'] = "%d:%d" % (bus, devNr)
        out = cmd_exec(["st-info","--chipid"], env = env)
        cond_log(fd, out)
        chip_id = int(out[0],16)
        res[chip_id] = (bus, devNr)
    return res

def stlink_program(binFilePath, env, base_addr):
    '''
    Programm the given binary to the base address. The usb device to
    programm is given in the environment passed into the function.

    binFilePath: full path to the binary
    env: Environment with STLINK_DEVICE set to bus_adress:dev_number
    base_addr: Base address where the binary will be put on the device.
    '''
    path = os.sep.join(binFilePath)
    return cmd_exec(["st-flash","write", "%s" % (path), "0x%08x" % (base_addr)], env = env)

def stlink_deploy(swGitRepo, buildSubPath, board, device, expected_git_hash, error_function, fd = None):
    '''
    Scan usb devices for a chip of the given device.
    '''
    vendor_stm = 0x0483
    dev2id={}
    dev2id['stm32l476'] = 0x0415
    dev2id['stm32f407'] = 0x0413
    if device not in dev2id:
        error_function(["Unknown device %s" % device,])
    devId = dev2id[device]
    bus_dev = get_usb_bus_dev([vendor_stm,])
    bus_dev_chipid = get_st_link_chip_id(bus_dev)
    if devId not in bus_dev_chipid:
        error_function(["No board for device %s connected" % (device),])
    env=os.environ
    env['STLINK_DEVICE'] = "%d:%d" % (bus_dev_chipid[devId][0],bus_dev_chipid[devId][1])
    path =  swGitRepo + buildSubPath + ("build-%s" % board, "firmware0.bin")
    out = stlink_program(path, env, 0x08000000)
    cond_log(fd, out)
    path =  swGitRepo + buildSubPath + ("build-%s" % board, "firmware1.bin")
    out = stlink_program(path, env, 0x08020000)
    cond_log(fd, out)
    time.sleep(10)


####################################################
#
#   Test code
#
####################################################
def mp_extract_version_info(soft_reset_string):
    rePat = re.compile('MicroPython ([\S]+) on ([\S]+) ([\S]+) with ([\S]+)')
    if len(soft_reset_string)<3:
        return None, None, None, None
    mpid = soft_reset_string[3]
    mtch = rePat.match(mpid)
    if mtch:
        version, date, board, chip = mtch.groups()
        chip = chip.lower()
        return version, date, board, chip
    else:
       return None, None, None, None


class mp_board():

    ser_cr=b'\x0a\x0d'
    ser_soft_reset = b'\x04'

    def __init__(self, ser_dev=None, fd=None):
        self.__fd = fd
        self.__buffer = b''
        self.__ser_dev = None
        if ser_dev!=None:
            self.open(ser_dev)

    def __exit__(self, _type, value, traceback):
        self.close()

    def __str__(self):
        res = []
        res.append("Device : %s" % self.__ser_dev )
        res.append("Board: %s" % self.__board )
        res.append("Chip : %s" % self.__chip )
        res.append("Version : %s" % self.__version )
        res.append("Date : %s" % self.__date )
        return os.linesep.join(res)

    def open(self, ser_dev):
        self.__ser_dev = ser_dev
        cond_log(self.__fd, "Open serial on: \"%s\"" % ser_dev)
        self.__serial = serial.Serial(ser_dev, 115200, timeout=0.1)
        self.soft_reset()

    def write(self, data, add_crlf=True, wait = True):
        if self.__serial:
            if isinstance(data, str):
                self.write(bytearray(data, 'latin-1'))
            elif isinstance(data, (bytes, bytearray)):
                cond_log(self.__fd, "Write: %s" % (data))
                data += b'' if not add_crlf else self.ser_cr
                self.__serial.write(data)
                if wait:
                    self.__buffer+=self.__read()
                else:
                    self.__buffer+=self.__serial.read(1000)
            elif isinstance(data, (list, tuple)):
                for item in data:
                    self.write(item)
            else:
                print("Unknown type: %s " % (type(data)))
        else:
            raise Exception("mp_board is not connected")

    def __read(self):
        ret = b""
        recon_cnt = 100
        while len(ret)==0:
            ret = self.__serial.read(1000)
        if recon_cnt==0:
            raise serial.serialutil.SerialException("Read failed")
        return ret

    def read(self):
        if self.__serial:
            data = self.__buffer[:]
            data += self.__serial.read()
            data = data.decode('latin-1').split("\r\n")
            cond_log(self.__fd, "Read from serial:\n%s\n" % os.linesep.join(data))
            self.__buffer = b''
            return data
        else:
             raise Exception("mp_board is not connected")

    def close(self):
        if self.__serial:
            self.read()
            self.__serial.close()

    def mp_ver_str(self, mpid):
        rePat = re.compile('MicroPython ([\S]+) on ([\S]+) ([\S]+) with ([\S]+)')
        mtch = rePat.match(mpid)
        cond_log(self.__fd, "Decode mp string: \"%s\"" % mpid)
        if mtch:
            version, date, board, chip = mtch.groups()
            chip = chip.lower()
            self.__version = version
            self.__date = date
            self.__board = board
            self.__chip = chip
        else:
            self.__version = None
            self.__date = None
            self.__board = None
            self.__chip = None

    def mp_info(self, soft_reset_string):
        if len(soft_reset_string)<3:
            cond_log(self.__fd, "Soft reset string to short: \"%s\"" %(str(soft_reset_string)))
            return
        mpid = soft_reset_string[3]
        self.mp_ver_str(mpid)

    def soft_reset(self):
        self.write(self.ser_cr)
        self.read()
        self.write(self.ser_soft_reset)
        out = self.read()
        self.mp_info(out)

    def is_version_matching(self, git_hash):
        '''
        a matching software is
        - non dirty software
        - with the expected git hash.
        '''
        rePat = re.compile('[\S]+-g([a-f0-9]+)[-]*([\S]*)')
        mtch = rePat.match(self.version)
        if mtch:
            grps = mtch.groups()
            ser_hash = grps[0]
            cond_log(self.__fd, "Found hash (%s) in version string %s" % (ser_hash, self.version))
            git_short_hash = git_hash[0:len(ser_hash)]
            if ser_hash == git_short_hash:
                cond_log(self.__fd, "%s software on the serial device" % ("Clean" if len(grps[1])==0 else grps[1].title()))
                return len(grps[1])==0
            else:
                cond_log(self.__fd, "Hash do not match: %s != %s" % (ser_hash, git_short_hash))
                return False
        else:
            raise Exception("Nothing found in \"%s\"" % self.version)
        return False

    def run(self, code):
        if isinstance(code, str):
            self.write(code)
        if isinstance(code,(list, tuple)):
            cType = code[0].split(':')[0].lower()
            if "code" == cType:
                self.write(code[1:])
            else:
                raise Exception("Code type %s not supported." % cType)

    @property
    def version(self):
        return self.__version

    @property
    def date(self):
        return self.__date

    @property
    def board(self):
        return self.__board

    @property
    def chip(self):
        return self.__chip


def get_serial_device(board, device, fd):
    for dev in glob.glob('/dev/ttyACM*'):
        mpb = mp_board(dev, fd)
        if mpb.chip == device:
            cond_log(fd, "Found %s on %s" % (device, dev))
            return mpb
        mpb.close()
    return None

def test_bin(board, device, git_hash, tests, fd=None):
    mpb = get_serial_device(board, device, fd)
    if not mpb.is_version_matching(git_hash):
        mpb.close()
        cond_log(fd, ["No valid software found on the device.", "No test done"])
        return
    #
    # Start run code on the board and check results
    #
    ok_cnt = 0
    for test in tests:
        test_name, test_code, expected = test
        mpb.run(test_code)
        res = mpb.read()
        if not res[-2] == expected:
            cond_log(fd, "\"%s\" failed" % (test_name))
            print("%s failed:" % (test_name))
            print("\n".join(res))
        else:
            cond_log(fd, "\"%s\" succeeded" % (test_name))
            ok_cnt+=1
    print("%3d of %3d tests Successfull." % (ok_cnt, len(tests)))


