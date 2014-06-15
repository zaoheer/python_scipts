#!/usr/bin/env python
import time
import paramiko
curr_time = time.strftime('%Y%m%d%H%M%S')
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect("172.16.30.38",22,"root","rootroot")
stdin, stdout, stderr = ssh_client.exec_command("echo hello")
out = stdout.readlines()
for o in out:
    print o
print stderr.readlines()

sftp_client = ssh_client.open_sftp()
#sftp_client.chdir("/")   #sftp working dir
#sftp_client.rename("/root/test3","/root/test1")
#sftp_client.put(localfile,remotefile)
#dirs=sftp_client.listdir()
#for dir in dirs:
#    print dir
#sftp_client.chmod("/root/test1",0700)
#sftp_client.mkdir("testtest")
#sftp_client.rmdir("testtest")
sftp_client.rename("/lottery/tomcat7.CustomerService8085/webapps","/lottery/tomcat7.CustomerService8085/webapps"+curr_time)
sftp_client.mkdir("/lottery/tomcat7.CustomerService8085/webapps")
sftp_client.put("/Users/zaoheer/python_script/hello.txt","/lottery/tomcat7.CustomerService8085/webapps/hello.war")
#sftp_client.chown()
sftp_client.close()
ssh_client.close()
