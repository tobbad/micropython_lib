#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Testing the code tor teh moduil test.
    Created on 21.4.2016
    @author: Tobias Badertscher

"""
import sys
import os
import unittest
from test_support import *

class TestGitCode(unittest.TestCase):

    def setUp(self):
        self.errMsgPat = None
        self.errMsgFound = False

    def tearDown(self):
        pass

    def error_callback(self, data):
        if self.errMsgPat:
            mtch = self.errMsgPat.match(data[0])
            if mtch:
                self.errMsgFound = len(mtch.groups())>0
            else:
                self.errMsgFound = False
        raise Exception("Error: %s" % os.linesep.join(data))

    def test_checkout_non_existing_folder(self):
        swGitRepoPath='/uagadougou'
        branch = 'master'
        self.errMsgPat = re.compile("(.*) does not exist")
        self.assertRaises(Exception, git_checkout_branch,swGitRepoPath, branch, self.error_callback)
        self.assertTrue(self.errMsgFound)

    def test_checkout_non_existing_branch(self):
        swGitRepoPath='..'
        branch = 'sidekick'
        self.errMsgPat = re.compile("Branch (.*) does not exist")
        self.assertRaises(Exception, git_checkout_branch,swGitRepoPath, branch, self.error_callback)
        self.assertTrue(self.errMsgFound)

    def test_checkout_dirty(self):
        swGitRepoPath='..'
        branch = 'master'
        with open('dirty.txt','w') as fd:
            fd.write("Hello dirty branch")
        self.errMsgPat = re.compile("Branch (.*) is dirty.")
        self.assertRaises(Exception, git_checkout_branch,swGitRepoPath, branch, self.error_callback)
        self.assertTrue(self.errMsgFound)
        with open('dirty.txt','w') as fd:
            fd.write("")

class TestValidSoftware(unittest.TestCase):

    def setUp(self):
        self.dut = mp_board(fd=sys.stdout)

    def test_dirty_version(self):
        ser_version = "MicroPython v1.7-237-g55773af-dirty on 2016-04-20; L476-DISCO with STM32L476"
        git_hash= '55773af311fe782dcaf8a366df426360bbe3a49e'
        self.dut.mp_ver_str(ser_version)
        print(self.dut)
        self.assertFalse(self.dut.is_version_matching(git_hash))

    def test_novalid_version(self):
        ser_version = ''
        git_hash= '55773af311fe782dcaf8a366df426360bbe3a49e'
        self.dut.mp_ver_str(ser_version)
        self.assertRaises(Exception, self.dut.is_version_matching,git_hash)

    def test_non_matching_hash(self):
        ser_version = "MicroPython fin_l4-6-g9b48fff on 2016-04-20; F4DISC with STM32F407"
        git_hash= '14b8969aca02e8e6da6a882a71345117c916a4eb'
        self.dut.mp_ver_str(ser_version)
        self.assertFalse(self.dut.is_version_matching(git_hash))

    def test_valid_version(self):
        ser_version = "MicroPython v1.7-237-g55773af on 2016-04-20; L476-DISCO with STM32L476"
        git_hash= '55773af311fe782dcaf8a366df426360bbe3a49e'
        self.dut.mp_ver_str(ser_version)
        self.assertTrue(self.dut.is_version_matching(git_hash))

class TestMicropythonSoftResetString(unittest.TestCase):
    mp_ser_str=[ "",
                "PYB: sync filesystems",
                "PYB: soft reboot","MicroPython fin_l4-6-g9b48fff on 2016-04-20; F4DISC with STM32F407",
                "Type \"help()\" for more information.",
                ">>>"]

    def test_empty(self):
        sreset_str = ["",]
        ret = mp_extract_version_info(sreset_str)
        res = not any(ret)
        self.assertTrue(res)

    def test_succeed(self):
        sreset_str = self.mp_ser_str
        ret = mp_extract_version_info(sreset_str)
        res = all(ret)
        self.assertTrue(res)


if __name__ == '__main__':
    unittest.main()

