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
        print(data)
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





if __name__ == '__main__':
    unittest.main()

