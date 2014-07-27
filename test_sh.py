#!/usr/bin/env python
import time,os,sys
import paramiko
from sh import grep

def getResultList(uLines):
    stringLines=lines.encode()
    return strLines
comm=grep(grep("-v","#","test.config"),"tomcat",_out=getResultList)
comm.wait()
tomcatlists=[]
#for line in results.readlines():
#    tomcatgroup=line.strip("\n").split("|")
#    tomcatlists.append(tomcatgroup)
#    print tomcatlists
