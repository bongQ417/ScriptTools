# -*- coding:utf-8 -*-

import time
from sys import argv
import json
import urllib2
import socket
import fcntl
import struct
import logging
import os

dirname = os.path.dirname(os.path.realpath(__file__)) + '/'

# 配置参数
with open(dirname + 'config.json', 'r') as file:
    configs = json.load(file)
    config = configs['error_monitor']

    # 参数获取
    webhook_token = config['webhook_token']
    keywords = config['keywords']

# 日志配置
logging.basicConfig(
    filename=dirname + 'error_monitor.log',
    level=logging.INFO,
    format='[%(levelname)s],%(asctime)s,%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

# 默认headers
Headers = {"Content-Type": "application/json", "charset": "utf-8"}


# 获取liunx的ip
def get_ip_address(ifname):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(
            fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                                        ifname[:15]))[20:24])
    except Exception:
        return ""


# 获取ip
Ip = get_ip_address("eth0")


# 请求text
def webhook(system, text):
    markdown = {
        "msgtype": "markdown",
        "markdown": {
            "title": system + "有异常错误",
            "text": "# 系统:" + system + "\n# ip:" + Ip + "\n> " + text
        }
    }
    jsondate = json.dumps(markdown)
    logging.info(system + ',' + Ip + 'has error message:' + text)
    request = urllib2.Request(
        url=webhook_token, data=jsondate, headers=Headers)
    urllib2.urlopen(request)


# tailf命令 跟踪日志文件
def follow(self, system="", s=1):
    file = open(self, 'r')
    try:
        file.seek(0, 2)
        while True:
            curr_position = file.tell()
            line = file.readline()
            if not line:
                file.seek(curr_position)
                # 先关闭原先文件,再打开新文件
                if (os.path.exists(self)):
                    if not (os.stat(self).st_size == curr_position):
                        file.close()
                        file = open(self, 'r')
                        file.seek(0, 2)
                        logging.warn('file is reopen:' + self)
            else:
                for key in keywords:
                    if (key in line):
                        webhook(system, line)
                        break
            time.sleep(s)
    finally:
        file.close()


if __name__ == '__main__':
    if (len(argv) < 3):
        logging.error('less than 2 params')
    else:
        follow(argv[1], argv[2])
