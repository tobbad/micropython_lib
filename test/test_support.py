#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Support functions for running a test.
    Created on 20.4.2016
    @author: Tobias Badertscher

"""
import os
import git
import subprocess
import usb


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
        print(os.linesep.join(res))
        print("Command \"%s\" finished" % cmdStr)
    return res

def check_build_success(log):
    '''
    Check if build suceeded
    '''
    return log[-2].split()[0]=='arm-none-eabi-objcopy'

def build_bin(swGitRepo, buildSubPath, board, error_function, res = None):
    '''
    Build the binary in the given path.
    '''
    cmdBuild = ["make","BOARD=%s" % board,"V=1"]
    cmdClean = cmdBuild[:]
    cmdClean.append( "clean" )
    buildPath = os.sep.join(swGitRepo+buildSubPath)
    cmd_exec(cmdClean, buildPath)
    if res == None:
        res = cmd_exec(cmdBuild, buildPath)
    if not check_build_success(res):
        error_function(["Build did not succeed",])

def git_checkout_branch(swGitRepoPath, branch, error_function):
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
        print("Checkout branch %s" % branch)
        repo.git.checkout(branch)
    return repo.commit()

def scan_para(para, error_function):
    if len(para[0])<1:
        error_function(["No branch given",])
    branch = para[0][0]
    return branch

def get_usb_bus_dev(vendors):
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
    res = []
    busses = usb.busses()
    for bus in busses:
        devices = bus.devices
        for dev in devices:
            if dev.idVendor in vendor:
                res.append((bus, dev ))
    return res

def get_st_link_chip_id(usb_dev):
    res = {}
    env=os.environ
    for bus, devNr in usb_dev:
        env['STLINK_DEVICE'] = "%d:%d" % (bus, devNr)
        chip_id = int(cmd_exec(["st-info","--chipid"], env = env)[0],16)
        res[chip_id] = (bus, devNr)
    return res

def stlink_program(binFilePath, env, base_addr):
    path = os.sep.join(binFilePath)
    cmd_exec(["st-flash","write", "%s" % (path), "0x%08x" % (base_addr)], env = env)

def stlink_deploy(swGitRepo, buildSubPath, board, device, expected_git_hash, error_function):
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
    stlink_program(path, env, 0x08000000)
    path =  swGitRepo + buildSubPath + ("build-%s" % board, "firmware1.bin")
    stlink_program(path, env, 0x08020000)
