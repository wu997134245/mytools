# coding=utf-8
import urllib
import time
import subprocess
#检测一个url 地址，根据返回状态执行不同操作

def url_check(url):
    try:
        f = urllib.urlopen(url)
        status_id = f.getcode()
        f.close()
    except IOError:
        return 404
    if status_id == 404:
        return 404
    return 200



def restart(cmd):
    subprocess.call('%s>/dev/null' % (cmd), shell=True)


def check_six(url):
    t = 0
    while t <=60:
        status=url_check(url)
        if status == 200 :
            return True
        else:
            t +=1
            time.sleep(1)
    return False


def main(url,cmd):
    status = url_check(url)
    if status == 404:
        time.sleep(10)
        status = url_check(url)
    if status == 404:
        restart(cmd)
        re_status = check_six(url)
        return re_status
    else:
        return status




if __name__ == '__main__':
    url = 'http://127.0.0.1'
    cmd = 'ls'
    main(url,cmd)
