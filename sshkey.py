#!/usr/bin/env python
#coding=utf8

import os
import subprocess

# 无交互式免密登陆

''' 使用方法，填写好主机列表，执行python sshkey.py'''

#host_list = [['192.168.9.3','1'],
#              ['192.168.9.4','1'],
#              ['192.168.9.9','1']
#              ]


host_list = [['192.168.9.9','1'],
             ['192.168.9.32','1'],
             ['192.168.9.33','1']
	     
]   # 主机ip和密码列表




#发送公钥到远程主机
send_pub= lambda x,y : 'sshpass -p %s ssh-copy-id -i ~/.ssh/id_rsa.pub %s' %(y,x)
#创建公钥命令
create_pub = 'ssh-keygen -t rsa'
#公钥路径
pub_key = '/root/.ssh/id_rsa.pub'


#公钥不存在则创建
if not os.path.exists(pub_key):
    subprocess.call(create_pub, shell=True)

#循环主机列表
for i in host_list:
    subprocess.call(send_pub(*i), shell=True)


