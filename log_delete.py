# -*- coding:utf-8 -*-

from sys import argv
import os
import datetime
import logging

script = os.environ["HOME"] + '/script/'
if not (os.path.exists(script)):
    os.mkdir(script, 0755)
# 日志配置
logging.basicConfig(
    filename=script + 'log_delete.log',
    level=logging.INFO,
    format='[%(levelname)s],%(asctime)s,%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')


# 删除指定路径过期的日志
def log_delete(basepath, delta=7):
    logging.info('-----------start delete log-----------')
    logging.info('path:' + basepath)
    # cd到日志路径
    os.chdir(basepath)
    # 遍历文件,判断mtime<day
    filelist = os.listdir('.')
    # 获取当天date
    today = datetime.date.today()
    for file in filelist:
        # 判断文件名包含log字段的文件
        if (('log' in file) and (os.path.isfile(file))):
            # 获取文件的mtime时间
            mtime = datetime.date.fromtimestamp(os.path.getmtime(file))
            dt = today - mtime
            if (dt.days >= delta):
                logging.info('delete [' + file + '],and mtime=' + str(mtime))
                # 删除过期文件
                os.remove(file)
    logging.info('-----------end delete log-----------')


if __name__ == '__main__':
    if (len(argv) < 2):
        logging.error('less than 1 params')
    elif (len(argv) == 2):
        log_delete(argv[1])
    else:
        log_delete(argv[1], int(argv[2]))
