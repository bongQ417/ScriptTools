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
import sys
import datetime

reload(sys)
sys.setdefaultencoding('utf8')

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
def webhook(system, message_list):
    text = '';
    for i in range(len(message_list)):
        text += message_list[i]
    markdown = {
        "msgtype": "markdown",
        "markdown": {
            "title":
            system + "有异常错误",
            "text":
            "# 系统:" + system + "\n# ip:" + Ip +
            "\n> " + text
        }
    }
    jsondata = json.dumps(markdown)
    logging.info(system + ',' + Ip + 'has error message:\n' + text)
    request = urllib2.Request(
        url=webhook_token, data=jsondata, headers=Headers)
    urllib2.urlopen(request)

# tailf命令 跟踪日志文件
def follow(self, system="", s=0.01):
    file = open(self, 'r')
    # 消息数组用的参数
    message_list = []
    start_date = datetime.datetime.now()
    try:
        file.seek(0, 2)
        while True:
            curr_position = file.tell()
            line = file.readline()
            hasError = False
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
                    #文件不存在的情况下sleep60秒
                    time.sleep(60)
            else:
                for key in keywords:
                    if (key in line):
                        hasError = True
                        # 多读一行日志
                        line += '\t'
                        line += file.readline()
                        break
            time.sleep(s)

            # 存储消息
            if (hasError):
                message_list.append(line)

            # 每隔30s发送一次消息
            now = datetime.datetime.now()
            dt = now - start_date
            if (dt.seconds > 10):
                # 消息大于1条则发送
                if (len(message_list) > 0):
                    webhook(system, message_list)
                start_date = datetime.datetime.now()
                message_list = []
    finally:
        file.close()


if __name__ == '__main__':

    if (len(argv) < 3):
        logging.error('less than 2 params')
    else:
        follow(argv[1], argv[2])
