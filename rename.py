#/usr/bin/env python
import os

zipfiles=os.popen("find /Users/zaoheer/deploy  -name  *.zip")
for files in  zipfiles.readlines():
    spath=files.strip("\n").split("/")
    dpath=spath[:]
    Len=len(dpath)
    dpath[Len-1]=dpath[Len-2]+".zip"
    s_path="/".join(spath)
    d_path="/".join(dpath)
    result=os.popen("mv "+s_path+" " +d_path)
    print result.readlines()
