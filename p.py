#!/usr/bin/env python
import paramiko
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect("172.16.23.35",22,"root","rootroot")
stdin, stdout, stderr = ssh_client.exec_command("echo hello")
print stdout.readlines()
print stderr.readlines()

sftp_client = ssh_client.open_sftp()
sftp_client.chdir()   #sftp working dir
sftp_client.rename(oldpath,newpath)
sftp_client.put(localfile,remotefile)
sftp_client.listdir()
sftp_client.chmod()
sftp_client.chown()
sftp_client.close()
ssh.close()
