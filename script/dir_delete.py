# -*- coding:utf-8 -*-

from sys import argv
import os
import datetime
import logging
import json
import shutil

dirname = os.path.dirname(os.path.realpath(__file__)) + '/'

# 配置参数
#with open(dirname + 'config.json', 'r') as file:
    #configs = json.load(file)
    #config = configs['dir_delete']
    #keywords = config['keywords']
# 日志配置
logging.basicConfig(
    filename=dirname + 'dir_delete.log',
    level=logging.INFO,
    format='[%(levelname)s],%(asctime)s,%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')


# 删除指定路径过期的日志
def dir_delete(basepath, delta=7):
    logging.info('-----------start delete dir-----------')
    logging.info('path:' + basepath)
    # cd到日志路径
    os.chdir(basepath)
    # 遍历文件,判断mtime<day
    filelist = os.listdir('.')
    # 获取当天date
    today = datetime.date.today()
    for file in filelist:
        if (os.path.isdir(file)):
            # 获取文件的mtime时间
            mtime = datetime.date.fromtimestamp(os.path.getmtime(file))
            dt = today - mtime
            if (dt.days >= delta):
                logging.info('delete [' + file + '],and mtime=' + str(mtime))
                # 删除过期文件夹
                shutil.rmtree(file,True)
    logging.info('-----------end delete log-----------')


if __name__ == '__main__':
    if (len(argv) < 2):
        logging.error('less than 1 params')
    elif (len(argv) == 2):
        dir_delete(argv[1])
    else:
        dir_delete(argv[1], int(argv[2]))
