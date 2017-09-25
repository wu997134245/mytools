# coding=utf-8
import os
import subprocess
import sys
import time
import urlcheck
import requests
import json

'''
cmdf.txt format
Example:apache-tomcat:ps aux|grep 'apache-tomcat-7.0.64' | grep -v 'grep' : /usr/local/tomcat/apache-tomcat-7.0.64/bin/startup.sh
Script that executes the shell command, if the execution is not successful, then execute the command of colon
'''


# 一个服务检测程序


class CheckApp(object):
    def __init__(self, cmdf, env):
        #加载配置文件和设置环境名称
        self.env = env
        self.cmdf = cmdf
        dirname = os.path.dirname(sys.argv[0])
        abspath = os.path.abspath(dirname)
        os.chdir(abspath)
        with open(cmdf) as fobj:
            data = fobj.readlines()
        self.data = data

    def restart(self, cmd):
        #执行重启
        subprocess.call('%s>/dev/null' % (cmd), shell=True)

    def output_file(self, output):
        #写入日志
        with open('appcheck.log', 'a') as fobj:
            fobj.write(output + '\n')

    def chk_app(self, cmd):
        #检查服务是否运行命令
        sub = subprocess.call('%s > /dev/null' % (cmd), shell=True)
        return sub

    def restart_all(self, ):
        pass

    def chk_helth(self, url, cmd):
        #网址访问方式检测，可获取该网址返回的状态
        status_id = urlcheck.main(url, cmd)
        return status_id

    def disable_app(self):
        #获取ops数据，不检测已停止的服务
        a = requests.get(url='http://127.0.0.1:8888')
        aj = json.loads(a.text)
        dset = {i.split('!')[0] for i in self.data}
        try:
            ajset = set(aj[self.env])
        except KeyError:
            ajset = set({})
        dis_app = dset & ajset
        if dis_app:
            f = open(self.cmdf, 'w')
            for i in self.data:
                for y in dis_app:
                    if y in i:
                        i = '#' + i
                f.write(i)
            f.close()
            self.__init__(self.cmdf, self.env)

    def test(self):
        self.disable_app()
        for cm in self.data:
            cmlist = cm.rstrip('\r\n').split('!')
            if '#' in cm:
                continue

            if cmlist[3] == 'check':
                status_id = self.chk_helth(cmlist[1], cmlist[2])
                if status_id == 200:
                    continue
                elif status_id:
                    output2 = '%s  %s Process does not exist' % (time.strftime('%Y%m%d %H:%M'), cmlist[0])
                    self.output_file(output2)
                    continue
                else:
                    output2 = '%s  %s restart timeout' % (time.strftime('%Y%m%d %H:%M'), cmlist[0])
                    self.output_file(output2)
                    return

            ca = self.chk_app(cmlist[1])
            if ca:
                self.restart(cmlist[2])
                output = '%s  %s Process does not exist' % (time.strftime('%Y%m%d %H:%M'), cmlist[0])
                self.output_file(output)
                time.sleep(3)


if __name__ == '__main__':
    cmdf = 'cmdf.txt'
    env = 'remove_licai'
    chk1 = CheckApp(cmdf, env)
    chk1.test()
