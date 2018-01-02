# -*- coding:utf-8 -*-

from sys import argv
import os
import datetime
import shutil
import tarfile
import logging

# 日志配置
logging.basicConfig(
    filename=os.environ["HOME"] + '/script/log_archive.log',
    level=logging.INFO,
    format='[%(levelname)s],%(asctime)s,%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')


# 获取昨天日期YYYY-MM-DD
def getYesterday():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    return str(yesterday)


def archive_log(basepath, system):
    yesterday = getYesterday()
    logdir = system + '-log.' + yesterday
    archive = 'archive'
    # 存储脚本原始路径
    # originPath = os.getcwd()
    # 修改路径到日志根目录
    os.chdir(basepath)
    if not (os.path.exists(archive)):
        os.mkdir(archive, 0755)
        logging.info('create ' + archive)

    # 判断是否已经今天是否压缩过
    tarname = logdir + '.tar.bz2'
    if not (os.path.exists(archive + '/' + tarname)):
        logging.info('archive log is started')
        # 判断日志文件夹是否存在
        targetdir = archive + '/' + logdir
        if not (os.path.exists(targetdir)):
            os.mkdir(targetdir, 0755)
            logging.info('create ' + targetdir)
        # 移动日志文件
        filelist = os.listdir('.')
        today = datetime.date.today()
        for file in filelist:
            # 判断文件名包含log字段的文件
            mtime = datetime.date.fromtimestamp(os.path.getmtime(file))
            dt = today - mtime
            if (('log' in file) and (dt.days > 0) and (os.path.isfile(file))):
                shutil.move(file, targetdir)
                logging.info(file + ' has moved')
        # tar -jcvf压缩文件
        os.chdir(archive)
        tar = tarfile.open(tarname, "w:bz2")
        tar.add(logdir)
        tar.close()
        logging.info('tar file is finally')
        # 删除多余文件夹
        shutil.rmtree(logdir)
        logging.info('archive log is finally')
    else:
        logging.warn('has exist ' + tarname)


if __name__ == '__main__':
    if (len(argv) < 3):
        logging.error('less than 2 params')
    else:
        logging.info('---------------archive_log function start-------------')
        archive_log(argv[1], argv[2])
        logging.info('---------------archive_log function end---------------')
