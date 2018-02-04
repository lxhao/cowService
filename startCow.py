#!/usr/bin/env python
# encoding: utf-8
import os
import time
import subprocess

DIR_THIS = os.path.dirname(os.path.abspath(__file__))

def runCow():
    ret = os.system('curl -x localhost:7777 www.baidu.com')
    if ret:
        subprocess.call('/usr/local/bin/cow')

def killOldProcess():
    # kill 已有的进程id
    with open(DIR_THIS + '/startCowpid.txt', 'a+') as f:
        old_pid = f.readline()
        if old_pid :
            # 确定进程id是运行的当前程序，防止误杀
            ps_info = os.popen("ps -ef | grep %s | awk '{print $2}'" % __file__)
            if old_pid in ps_info:
                os.system('kill -9 %s' % old_pid)
    # 保存当前进程id
    with open(DIR_THIS + '/startCowpid.txt', 'w') as f :
        f.write('%d\n' % os.getpid())

if __name__ == '__main__' :
    killOldProcess()
    while(True):
        print 'run'
        runCow()
        time.sleep(60)


