#/usr/bin/env python
#coding:utf-8
import os,sys

ices=''
if len(sys.argv) > 1:
    ices = sys.argv[1]
#    print ices

iceFiles=os.popen("find /Users/zaoheer/deploy  -name " + ices + "*.zip |grep ice")
for ice in  iceFiles.readlines():
    icePath=ice.strip("\n").split("/")
    Len=len(icePath)
    iceDir=icePath[:Len-1]
    icename=icePath[Len-2]
    iceDir="/".join(iceDir)
    print "start update "+ icename +"....."
    autoResult=os.popen("cd " + iceDir + " && " + " unzip *.zip "  + "&&  rm -f *.zip " + "echo "+icename + " && tar  -czf " + icename + ".tgz * --remove-files ")
    print icename +  "\tupdate"
