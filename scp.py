# -*- coding:utf-8 -*-
import paramiko
import os
import sys
import time
import argparse

# get function name
FuncName = lambda n=0: sys._getframe(n + 1).f_code.co_name

def ssh_scp_put(ip,port,user,password,local_file,remote_file):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, 'root', password)
        a = ssh.exec_command('date')
        stdin, stdout, stderr = a
        print stdout.read()
        sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        sftp = ssh.open_sftp()
        sftp.put(local_file, remote_file)
    except Exception, e:
        print '{0} : {1}'.format(FuncName(), e)

def ssh_scp_get(ip, port, user, password, remote_file, local_file):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, 'root', password)
        a = ssh.exec_command('date')
        stdin, stdout, stderr = a
        print stdout.read()
        sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        sftp = ssh.open_sftp()
        sftp.get(remote_file, local_file)
    except Exception, e:
        print '{0} : {1}'.format(FuncName(), e)

if __name__ == '__main__':
    port = 22
    # help message
    parser = argparse.ArgumentParser(description='SCP')
    parser.add_argument('-i', '--ip', 
                        help='IP address', required=True)
    parser.add_argument('-u', '--user', 
                        help='username', required=True)
    parser.add_argument('-p', '--password', 
                        help='password', required=True)
    parser.add_argument('-m', '--mode', 
                        help='get or put', required=True)
    parser.add_argument('-l', '--local', 
                        help='local path', required=True)
    parser.add_argument('-r', '--remote', 
                        help='remote path', required=True)
    parser.add_argument('-f', '--file',
                        help='filename', required=True)

    options = parser.parse_args()
    mode = options.mode.lower()
    if mode == 'get':
        ssh_scp_get(options.ip, port, options.user, options.password, options.remote+'/'+options.file, options.local+'/'+options.file)
    elif mode == 'put':
        ssh_scp_put(options.ip, port, options.user, options.password, options.local+'/'+options.file, options.remote+'/'+options.file)
    else:
        print "Invalid mode: " + options.mode
