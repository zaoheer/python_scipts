#!/usr/bin/env python
import time,os,sys
import paramiko

def getHOST(config_file):
    if os.path.exists(config_file) is not True:
        print "The config file is not exists ! please check"
        sys.exit()
    results=os.popen("grep HOST " + config_file + " |grep -v \# ")
    hostlists=[]
    for line in results.readlines():
        hostgrow=line.strip('\n').split("|")
        hostlists.append(hostgrow)
    return hostlists


def getTomcat(config_file):
    if os.path.exists(config_file) is not True:
        print "The config file is not exists ! please check"
    results=os.popen("grep tomcat  "+ config_file +" |grep -v \#")
    tomcatlists=[]
    for line in results.readlines():
        tomcatgrow=line.strip('\n').split("|")
        tomcatlists.append(tomcatgrow)
    return tomcatlists

def getIcenodes(config_file):
    if os.path.exists(config_file) is not True:
        print "The config file is not exists ! please check"
    results=os.popen("grep icenode "+ config_file + " |grep -v \#")
    icenodelist=[]
    for line in results.readlines():
        icenodegrow=line.strip("\n").split("|")
        icenodelist.append(icenodegrow)
    return icenodelist




def getHostConn(ip,user,pwd,port=22):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(ip,port,user,pwd)
    return ssh_client

def checkfiles(ssh_client,remoteFiles):
    for file  in   remoteFiles:
        stdin, stdout, stderr = ssh_client.exec_command("ls " +file)
        err=stderr.readlines()
        if err is not null:
            print err

def update_tomcat_item(ssh_client,localdir,remotedir,localfile,remotefile):
    sftp_client = ssh_client.open_sftp()
    localdir=localdir.rstrip("/")
    remotedir=remotedir.rstrip("/")
    curr_time = time.strftime('%Y%m%d%H%M%S')
    sftp_client.rename(remotedir,remotedir+curr_time)
    sftp_client.mkdir(remotedir)
    sftp_client.put(localdir+"/"+localfile,remotedir+"/"+remotefile)
    sftp_client.close()


def update_icenode(ssh_client,localdir,remotedir,localfile,remotefile):
    curr_time = time.strftime('%Y%m%d%H%M%S')
    localdir=localdir.rstrip("/")
    remotedir=remotedir.rstrip("/")
    bakdir=remotedir+"/bak"+curr_time
    stdin, stdout, stderr = ssh_client.exec_command("mkdir "+bakdir)
    err= stderr.readlines()
    for e in err:
        print e
    stdin, stdout, stderr = ssh_client.exec_command("find " + remotedir +" -maxdepth 1 |egrep -v 'tpaydebit|tbingo|bak'| awk 'NR>=2{print $0}' |xargs -I {}  mv {} "+bakdir)
    err= stderr.readlines()
    for e in err:
        print e
    sftp_client = ssh_client.open_sftp()
    sftp_client.put(localdir+"/"+localfile,remotedir+"/"+remotefile)
    sftp_client.close()
    
    #stdin,stdout,stderr=ssh_client.exec_command("cd "+remotedir+"&&  /usr/bin/unzip -q "+ remotefile+" -d temp  && cd temp/* && mv * ../../ && cd ../../ && rm -rf  temp")
    stdin,stdout,stderr=ssh_client.exec_command("cd "+remotedir+" &&  mkdir temp  &&  tar -xzp -f "+ remotefile+" -C temp  && cd temp/* && mv * ../../ && cd ../../ && rm -rf  temp *.tgz")
    
    err= stderr.readlines()
    for e in err:
        print e
    

    


if __name__ == '__main__':
    config_file="44.config"
    #get hosts list config
    hosts=getHOST(config_file)
    #get tomcat config list
    tomcat_items=getTomcat(config_file)
    #get icenode config list
    icenode_items=getIcenodes(config_file)

    # for loop  get host connections
    for host in hosts:
        #get host connection
        ssh_client=getHostConn(host[2],host[3],host[4],int(host[5]))
        print "host " + host[2]+ " create ssh connection successfully ! "


        #for loop to update tomcat_items
        for tomcat_item in tomcat_items:
            if tomcat_item[1]==host[1]:
                #print tomcat_item
                tomcat_updater=update_tomcat_item(ssh_client,tomcat_item[4],tomcat_item[2],tomcat_item[5],tomcat_item[3])
                print "update " + tomcat_item[1]+" " + tomcat_item[5] +" successfully"

        

        #for loop to update icenodes
        for icenode in icenode_items:
            if icenode[1]==host[1]:
                #print icenode
                icenode_updater=update_icenode(ssh_client,icenode[4],icenode[2],icenode[5],icenode[3])
                print "update " +icenode[1] +" " + icenode[5] +" successfully"


        ssh_client.close()
