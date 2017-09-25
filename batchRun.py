# coding=utf-8
import subprocess
import sys

'''在远程主机批量执行脚本程序，
   使用方法，将需要批量执行的脚本文件放在/opt/,第一个参数是脚本文件
   python batchRun.py script.sh
'''


#主机列表，需先做好免密登陆

host_list = ['192.168.9.9',
             '192.168.9.32',
             '192.168.9.33'
            ]


def run_cmd(cmd):
    subprocess.call(cmd,shell=True)



def main():
    scriptFile=sys.argv[1]
    filePath = '/opt/'             #脚本存放目录
    for i in host_list:
        run_cmd('scp {2}{0} {1}:{2} && ssh {1} "cd {2};bash {0}"'.format(scriptFile,i,filePath))



if __name__ == '__main__':
    main()