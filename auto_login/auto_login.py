# -*- coding:utf-8 -*-

from sys import argv
from pymongo import MongoClient
import pexpect
# from bson import json_util as jsonb

conn = MongoClient('127.0.0.1', 27017)
db = conn.auto_login
host_cluster = db.host_cluster


def auto_login(user, password, ip):
    patterns = ['.*yes/no.*', '[Pp]assword:', '#']
    CONTINUES, PASSWD, OPFLAG = range(len(patterns))
    child = pexpect.spawn('ssh %s@%s' % (user, ip))
    while True:
        i = child.expect(patterns)
        if i == CONTINUES:
            child.sendline('yes')
        elif i == PASSWD:
            child.sendline(password)
        elif i == OPFLAG:
            break
    child.interact()


def add_host(argv):
    # 获取参数
    hostname = argv[2]
    user = argv[3]
    password = argv[4]
    ip = argv[5]
    host = {
      'hostname': hostname,
      'user': user,
      'password': password,
      'ip': ip
    }
    # 插入数据
    hostname_json = {'hostname': hostname}
    result = host_cluster.count(hostname_json)
    if result:
        host_cluster.update(hostname_json, {"$set": host})
        print '更新数据成功'
    else:
        host_cluster.insert(host)
        print '插入数据成功'


def remove_host(argv):
    hostname = argv[2]
    hostname_json = {
      'hostname': hostname
    }
    host_cluster.remove(hostname_json)
    print '删除数据成功'


def list_host(argv):
    result = host_cluster.find()
    i = 1
    for host in result:
        print '%s. %s' % (str(i), host['hostname'])
        i = i+1


def login(hostname):
    hostname_json = {
      'hostname': hostname
    }
    result = host_cluster.find_one(hostname_json)
    auto_login(result['user'], result['password'], result['ip'])


if __name__ == '__main__':
    if (len(argv) < 2):
        print '1. list'
        print '2. add [hostname, user, password, ip]'
        print '3. remove hostname'
        print '4. hostname'
    else:
        cmd = argv[1]
        if('list' == cmd):
            list_host(argv)
        elif ('add' == cmd):
            add_host(argv)
        elif('remove' == cmd):
            remove_host(argv)
        else:
            login(cmd)
