#!/usr/bin/python
# -*- coding: utf-8 -*-
import paramiko
import os
import json

# 配置参数
dirname = os.path.dirname(os.path.realpath(__file__)) + '/'
with open(dirname + 'config.json', 'r') as file:
    hosts = json.load(file)

localfile = '/Users/bongq/CodeHub/Git/ScriptTools/script.tar'


# 上传文件
def transferFile(hostname, username, password, remotepath):
    s = paramiko.Transport((hostname, 22))
    s.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(s)
    sftp.put(localfile, remotepath+'/script.tar')
    s.close()


# 脚本安装流程
for host in hosts:
    # 参数获取
    hostname = host['hostname']
    username = host['username']
    password = host['password']
    remotepath = host['remotepath']
    system = host['system']
    log_delete = host['log_delete']
    log_archive = host['log_archive']
    error_monitor = host['error_monitor']
    # 上传文件
    transferFile(hostname, username, password, remotepath)
    # 登录主机
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, 22, username, password, timeout=5)
    # 执行bash命令
    commandList = []
    commandList.append('cd ' + remotepath)
    commandList.append('tar -xvf script.tar')
    commandList.append('chown -R root script')
    commandList.append('chgrp -R root script')
    # commandList.append('chmod -R 755 script')
    commandList.append('crontab -l > crontab.txt')
    # log_archive
    for params in log_archive:
        logpath = params['logpath']
        commandList.append(
            'echo "30 0 * * * python ' + remotepath + '/script/log_archive.py '
            + logpath + ' ' + system + '" >> crontab.txt')
    # log_delete
    for params in log_delete:
        logpath = params['logpath']
        day = params['day']
        commandList.append(
            'echo "0 1 * * * python ' + remotepath + '/script/log_delete.py ' +
            logpath + ' ' + str(day) + '" >> crontab.txt')
    # error_monitor
    for params in error_monitor:
        logpath = params['logpath']
        commandList.append(
            'sh script/error_monitor.sh ' + logpath + ' ' + system)
    commandList.append('crontab crontab.txt')
    semicolon = ';'
    command = semicolon.join(commandList)
    client.exec_command(command)
    client.close()
