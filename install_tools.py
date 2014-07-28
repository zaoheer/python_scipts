#!/usr/bin/python
#coding: utf-8

import os,sys
import urllib
import tarfile

configFile="all_in_one.conf"
if len(sys.argv) < 3 :
    print "Usage:  ./install_tools  list|install|update   group|groupname|items"
    sys.exit(1)

#传参赋值
action1=sys.argv[1]
action2=sys.argv[2]

if action1 not in ('update','list','install'):
    print "Usage:  ./install_tools  list|install|update   group|groupname|items"
    sys.exit(1)
    

itemType=('TOMCAT','ICE')
Baseurl="ftp://soft.uuzz.com/"

#加载配置文件
try:
    configfileUrl=Baseurl+"base/all_in_one.conf"
    urllib.urlretrieve(configfileUrl,'all_in_one.conf')
except:
    print "The configure file is not exists !!!"
    sys.exit(1)

def listGroup(configFile,):
    '''This function return groups list in configfile  !!!!'''
    if os.path.exists(configFile) is not True:
        print "ERROR,config file "+configFile+" is not exists,exit"
        sys.exit()
    else:
        groups=[]
        command="grep group "+configFile +" | grep -v \#"
        #print command
        results=os.popen(command)
        for group in results.readlines():
            group=group.strip('\n').split(":")[1]
            #print group
            groups.append(group)
        return groups
        
        
def listGroupItems(configFile,type1):
    if os.path.exists(configFile) is not True:
        print "ERROR,config file "+configFile+" is not exists,exit"
        sys.exit()
    else:
        Items=[]
        command="grep "+type1 +" "+configFile+"|grep -v group"+ " | grep -v '#'"
        #print command
        results=os.popen(command)
        #print results.readlines()
        for item in results.readlines():
            item=item.strip('\n')
            Items.append(item)
        return Items
    
def listItems(configFile,listType1,listType2="'.*'"):
    '''This funtion return  icenodes list in configfile'''
    
    if os.path.exists(configFile) is not True:
        print "ERROR,config file "+configFile+" is not exists,exit"
        sys.exit()
    else:
        Items=[]
        command="egrep "+listType2+"  "+configFile +"|egrep "+listType1 + " | grep -v '#'"
        #print command
        results=os.popen(command)
        #print results.readlines()
        for item in results.readlines():
            #item=item.strip('\n')
            item=item.strip('\n').split(":")
            
            Items.append(item)
        return Items        
  
def listItem(configFile,itemname):
    ''' retun item String '''
    if os.path.exists(configFile) is not True:
        print "ERROR,config file "+configFile+" is not exists,exit"
        sys.exit()
    
    else:
        command="grep "+ itemname +" " + configFile + " | grep -v '#'"
        #print command
        results=os.popen(command)
     

        for item in results.readlines():
            item = item.strip('\n')
        return item   

def installIcenode(baseurl,icenode):
    os.system("rm -rf /tmp/uuzz/*")
    os.system("mkdir -p /tmp/uuzz/")
    os.system("mkdir -p /lottery")
    icenode=icenode.split(":")
    Len=len(icenode)
    pkgname=icenode[Len-1]
    installDir=icenode[Len-2]
    tmpPath='/tmp/uuzz/'+pkgname
    #print tmpPath
    #下载到临时目录
    url=baseurl+"packages/"+pkgname
    urllib.urlretrieve(url,tmpPath)
    #解压到目标目录
    if os.path.exists(installDir+"/bin"):
        print "Warning, "+installDir +" aleady  exists , Skip !!!"
    else:
        os.system("mkdir -p "+installDir)
        tar=tarfile.open(tmpPath)   
        tar.extractall(installDir)
        command="cd "+installDir +" &&  cd  *ice*  && mv * .. && cd .. && rmdir *ice*"
        result=os.system(command)
        if result == 0:
            print "Install "+pkgname +" Successfull !!!"
        else:
            print "ERROR, Install "+pkgname
    
    
def installTomcat(baseurl,tomcatnode) :
    os.system("rm -rf /tmp/uuzz/*")
    os.system("mkdir -p /tmp/uuzz/")
    tomcatnode=tomcatnode.split(":")
    
    Len=len(tomcatnode)
    pkgname=tomcatnode[Len-1]
    installPath=tomcatnode[Len-2]
    tomcatName=os.path.basename(installPath)+".tgz"
    tomcaturl=baseurl+"tomcat/"+tomcatName  
    pkgurl=baseurl+"packages/"+pkgname
    
    tmpPath='/tmp/uuzz/'+tomcatName
    urllib.urlretrieve(tomcaturl,tmpPath)
    if os.path.exists(installPath+"/bin"):
            print "Warning, "+installPath +" aleady  exists, Skip  !!!"  
    else:
        
        result=os.system("tar -xzp -f "+tmpPath +" -C /usr/local/  &&  rm -rf  /tmp/uuzz")
        #判断是否解压成功
        if result == 0:
                    print "Uncompress "+tomcatName +" Successfull !!!"
                    if os.path.exists(installPath+"/webapps"):
                        urllib.urlretrieve(pkgurl,installPath+"/webapps/"+pkgname)
                        print pkgname + " install successfull !"
                           
                    
        
        
    
if __name__=='__main__':
    #列出有多少组
    if action1=='list' and action2=='group' :
        print listGroup(configFile)
    #按类型列出
    elif action1=='list' and action2 in itemType :
        list = listItems(configFile,action2)
        for item in list:
            item=":".join(item)
            print item
    #按组列出
    elif action1=='list' and  action2 in listGroup(configFile):
        list = listGroupItems(configFile,action2)
        for item in list:
            #item=":".join(item)
            print item 
    #列出单个项目
    elif action1=='list' and action2 not in listGroup(configFile) and action2 not in itemType:
        list=listItem(configFile, action2)
        print list
    #安装组    
    elif action1=='install' and  action2 in listGroup(configFile):
        lists = listGroupItems(configFile,action2)
        for list in lists:
            #print list
            item=list.split(":")
            #print item
            updateType=item[2]
            if updateType=='TOMCAT':
                installTomcat(Baseurl,list)
                #print "install  Tomcat"
            if updateType=='ICE':
                installIcenode(Baseurl, list)
                #print "install  ICE"
        
        
        
    else:
        print "Usage:  ./install_tools  list|install|update   group|groupname|items"




