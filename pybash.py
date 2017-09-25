#!/usr/bin/env python
# coding=utf-8

import pty
import os
import sys
import functools
# 审计功能


def _read(fd, logf):
    logdata = os.read(fd, 4096)
    logf.write(logdata)
    logf.flush()
    return logdata


f = open('/mnt/shengji.log', 'a+')   # 审计日志路径
myread = functools.partial(_read, logf=f)    # 使用偏函数给一个默认值
pty.spawn('/bin/bash',master_read = myread)   #pty 提供一个bash ，并给一个读写的函数
f.close()

sys.exit(0)