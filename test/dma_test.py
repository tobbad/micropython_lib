#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    ????
    Created on ??.??.????
    @author: Tobias Badertscher

"""
import sys
import os
import inspect
from test_support import *

swGitRepo =('','home','badi','projekte','sw','embedded','application','micropython')
swGitRepoPath = os.sep.join(swGitRepo)
buildPath = ('stmhal',)

thisModule = sys.modules[__name__]
svnRev=("$Rev: 6738 $").split()[1]
svnDate=("$Date: 2012-08-08 14:05:16 +0200 (Mi, 08 Aug 2012) $").split()[1]
pythonVersion=[int(i.replace('+','')) for i in sys.version.split()[0].split('.')]
exportPrefix='ex_'
#######################################
#
# helper functions
#
#######################################
board2chip={}
board2chip['STM32F4DISC']='stm32f407'
board2chip['STM32L476DISC']='stm32l476'
tests=[
("Carrige return",'',''),
("Hello world",'print("Hello world")',"Hello world")]
#######################################
#
# script functions
#
#######################################
def ex_STM32F4DISC(*para):
    '''
    STM32F4DISC branch
    Test dma for spi, i2c on STM32F4DISC.
    '''
    board = 'STM32F4DISC'
    logFile = "%s.log" % (board)
    fd = open(logFile, 'w')
    branch = scan_para(para, Usage)
    gHash = git_checkout_branch(swGitRepoPath, branch, Usage, fd)
    #build_bin(swGitRepo, buildPath, board, Usage, fd)
    #stlink_deploy(swGitRepo, buildPath, board, board2chip[board], gHash, Usage, fd)
    test_bin(board, board2chip[board], gHash, tests, sys.stdout)



def ex_STM32L476DISC(*para):
    '''
    STM32L476DISC branch
    Test dma for spi, i2c on STM32L476DISC.
    '''
    print("Run STM32L476DISC")

def ex_all(*para):
    '''
    all
    Test dma on all boards.
    '''
    ex_STM32F4DISC(para)
    ex_STM32L476DISC(para)

#######################################
#
# Collect all commands in this script.
#
#######################################
def getModuleInfo():
    #print("Items in the current context:")
    exPrefixlen=len(exportPrefix)
    cmds={}
    moduleDoc=""
    for name, item in inspect.getmembers(thisModule):
        if inspect.isfunction(item):
            if exportPrefix == item.__name__[0:exPrefixlen]:
                cmds[item.__name__]=item
        if inspect.ismodule(item):
            moduleDoc=item.__doc__
    return cmds, moduleDoc

def cleanUpTextList(tList):
    '''
    Remove empty lines in a \n separated test list
    '''
    text=[]
    for i in tList:
        i=i.strip()
        if len(i)>0:
            text.append(i)
    return text
#######################################
#
# Usage and main entrance of skript
#
#######################################
def Usage(error=None):
    skriptname=sys.argv[0].split(os.sep)[-1]
    CnCDict, moduleDoc =getModuleInfo()
    sCList  =   [i for i in CnCDict.keys()]
    sCList.sort()
    text=cleanUpTextList(moduleDoc.split("\n"))
    cmdStr="command"
    maxCmdLen=len(cmdStr)
    for cmd in sCList:
        maxCmdLen = maxCmdLen if len(cmd)<maxCmdLen else len(cmd)
    commentPos=12
    text.extend([
          "(SVN-Revision %s)" % (svnRev),
          "",
          "Comand line:",
          "  %s cmd parameter" % skriptname,
          " "*commentPos+"'cmd' and 'parameter' according to the following list:",
          " "*commentPos+"(Parameters in [xxx] are optional and should - if used - entered without [])",
          ])
    cmdHeader="    command      parameter"
    if pythonVersion[1]>5:
        cmdHeader="    {cmd:{cwidth}} {b}".format(cmd=cmdStr,b="Parameter(s)",cwidth=maxCmdLen+1)
    #text.append(cmdHeader)
    for cmdName in sCList:
        if CnCDict[cmdName].__doc__!=None:
            cmdInfo=cleanUpTextList(CnCDict[cmdName].__doc__.split("\n"))
            cmdName=cmdInfo[0].split()[0].strip()
            para=" ".join(cmdInfo[0].split()[1:])
            if pythonVersion[1]>5:
                text.append("    {a:{cwidth}} {b}".format(a=cmdName,b=para,cwidth=maxCmdLen+1))
            else:
                text.append("    %s %s" % (cmdInfo[0].strip(),cmdInfo[1].strip()))
            if len(cmdInfo)>1:
                for line in cmdInfo[1:]:
                    text.append(" "*commentPos+line.strip())
    res="\n".join(text)
    etext=[]
    if error != None:
        error.insert(0,"ERROR:")
        maxlen=max([len(i) for i in error])
        etext.append("*"*(maxlen+4))
        etext.append("*"*(maxlen+4))
        for i in error:
            etext.append("* "+i+"%s *" % (" "*(maxlen-len(i))))
        etext.append("*"*(maxlen+4))
        etext.append("*"*(maxlen+4))
        print("\n".join(etext))
    print(res)
    sys.exit()

def main():
    if len(sys.argv)<2:
        Usage(["No Command given",])
    cmd=sys.argv[1]
    cmds, moduleDoc = getModuleInfo()
    iCmd='ex_'+cmd
    if iCmd not in cmds:
        Usage()
    cmds[iCmd](sys.argv[2:])

if __name__ == '__main__':
    main()

