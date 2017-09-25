# coding=utf-8
import subprocess
from pymongo import MongoClient
import time
import ConfigParser


'''
mongodb 归档脚本，将数据备份并删除库中备份的数据，
如当前时间20170601，则会备份4月份，并删除数据库中4月份数据
'''


configfile = './config.ini'
source = 'mongodb'
cf = ConfigParser.ConfigParser()
cf.read(configfile)
host = cf.get(source,'host')
port = int(cf.get(source,'port'))
user = cf.get(source,'user')
passwd = cf.get(source,'passwd')
db = cf.get(source,'db')
collection = cf.get(source,'collection')
key = cf.get(source,'key')
backscrip = cf.get(source,'backscrip')
restorescrip = cf.get(source,'restorescrip')




def datesum(num=1):
    num += 1
    monthtime = 2678400  # one month = 31 day
    today = time.time()
    today2 = time.localtime(today).tm_mday
    if today2 < 6:
        monthtime = 2419200  # one month = 28 day
    lasttime = today - monthtime * num
    lastmonth = time.strftime('%Y%m', time.localtime(lasttime))
    return lastmonth




how_month = 1  # 保留一个月数据
query =datesum(how_month)     #计算日期
backpath = './mongoback/' + db + query
backupcmd = '''%s -h %s:%s -u %s -p %s -d %s -q '{%s:{$regex:"%s"}}' -c %s -o %s ''' \
            % (backscrip, host, port, user, passwd, db, key,query, collection, backpath)
restorecmd = '''%s -d %s -h %s:%s -u %s -p %s --dir %s/%s''' % \
            (restorescrip, db, host, port, user, passwd, backpath, db)




def restore(cmd):
    status = subprocess.call(cmd, shell=True)
    return status



def backup(cmd):
    data_count = find_data(query).count()
    if data_count:
        status = subprocess.call(cmd, shell=True)
        return not status
    else:
        print 'No such data'
        return False


def get_mongoclinet():
    client = MongoClient(host, port)
    dbc = client.get_database(db)
    dbc.authenticate(user, passwd)
    return dbc,client



def del_Data(conditions):
    dbc,client = get_mongoclinet()
    table = dbc.get_collection(collection)
    table.delete_many({key: {'$regex': conditions}})
    client.close()


def find_data(conditions):
    dbc,client = get_mongoclinet()
    table = dbc.get_collection(collection)
    data = table.find({key: {'$regex': conditions}})
    client.close()
    return data



def test():
    status = backup(backupcmd)
    if status:
        del_Data(query)
    else:
        print 'backup failure'



if __name__ == '__main__':
    test()
