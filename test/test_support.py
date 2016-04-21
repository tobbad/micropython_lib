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

def cmd_exec(cmd, path=".", env = {}, verbose = True):
    '''
    Execute a command (tuple) in a subprocess and return
    the output as list
    '''
    cmdStr = " ".join(cmd)
    res = None
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

####################################################
#
#   Test code
#
####################################################
def get_serial_device(board, device, fd):
    rePat = re.compile('MicroPython ([\S]+) on ([\S]+) ([\S]+) with ([\S]+)')
    for dev in glob.glob('/dev/ttyACM*'):
        ser = serial.Serial(dev, 115200, timeout=0.1)
        if serial:
            cond_log(fd, "Succeeded access port %s\n" % dev)
        else:
            cond_log(fd, "Failed access port %s\n" % dev)
            continue
        ser.write(b'\x04')
        out = ser.read(1000).decode('latin-1').split("\r\n")
        cond_log(fd, out)
        if len(out)<3:
            continue
        mpid = out[3]
        mtch = rePat.match(mpid)
        version, date, board, chip = mtch.groups()
        chip = chip.lower()
        if chip == device:
            cond_log(fd, "Found %s on %s" % (device, dev))
            return ser, version, board
        ser.close()
    return None

def check_valid_software(git_hash, ser_version, fd):
    '''
    Valid softweare is
    - non dirty software
    - with the expected git hash.
    '''
    rePat = re.compile('[\S]+-g([a-f0-9]+)[-]*([\S]*)')
    mtch = rePat.match(ser_version)
    if mtch:
        grps = mtch.groups()
        ser_hash = grps[0]
        cond_log(fd, "Found hash (%s) in version string %s" % (ser_hash, ser_version))
        if ser_hash == git_hash[0:len(ser_hash)]:
            cond_log(fd, "%s software on the serial device" % ("Clean" if len(grps[1])==0 else grps[1].title()))
            return len(grps[1])==0
        else:
            return False
    else:
        raise Exception("Nothing found in \"%s\"" % ser_version)
    return False

def test_bin(board, device, git_hash, fd=None):
    ser, version, board = get_serial_device(board, device, sys.stdout)
    if not check_valid_software(git_hash, version, sys.stdout):
        ser.close()
        cond_log(fd, ["No valid software fuound on the device.", "No test done"])
        return



