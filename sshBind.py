#!/usr/bin/env python
# encoding: utf-8
import os
import time
import subprocess
import socket

DIR_THIS = os.path.dirname(os.path.abspath(__file__))

def killRunning(command):
    ps_info = os.popen("ps -ef | grep %s | awk '{print $2}'" % command)
    for pid in ps_info.readlines():
        os.system('kill -9 %s' % pid)

def sshBind():
    curl_ret = os.system('curl -x 120.25.203.182:7777 www.baidu.com')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'aliyun 7777 proxy is %s' % ('connect' if curl_ret == 0 else 'disconnect')
    socket_ret = sock.connect_ex(('localhost', 7777))
    # 代理网络异常且本地端口代理开启
    if curl_ret and socket_ret == 0:
        print '7777端口重启'
        killRunning('7777:localhost:7777')
        os.system('ssh -CfnNT -R 7777:localhost:7777 lxhao@120.25.203.182 -p 8866')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('120.25.203.182', 10001))
    print 'port 10001 is %s' % ('open' if result == 0 else 'close')
    if result:
        killRunning('10001:localhost:22')
        os.system('ssh -CfnNT -R 10001:localhost:22 lxhao@120.25.203.182 -p 8866')

def killOldProcess():
    # kill 已有的进程id
    with open(DIR_THIS + '/sshbindPid.txt', 'a+') as f:
        old_pid = f.readline()
        if old_pid :
            # 确定进程id是运行的当前程序，防止误杀
            ps_info = os.popen("ps -ef | grep %s | awk '{print $2}'" % __file__)
            if old_pid in ps_info:
                os.system('kill -9 %s' % old_pid)
    # 保存当前进程id
    with open(DIR_THIS + '/sshbindPid.txt', 'w') as f :
        f.write('%d\n' % os.getpid())

if __name__ == '__main__' :
    killOldProcess()
    while(True):
        sshBind()
        time.sleep(60)


