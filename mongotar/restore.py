import subprocess
import os
import sys
import ConfigParser


configfile = './config.ini'
source = 'mongodb'
datadir = './mongoback/'
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



arg = sys.argv[1]
if '/' in arg :
    data = arg
else:
    data = datadir + db + arg + '/' + db



restorecmd = '''%s -d %s -h %s:%s -u %s -p %s --dir %s''' % \
            (restorescrip, db, host, port, user, passwd, data)



def traverse_file(datadir):
    "This a Traverse the document sum,return a dir list"
    file_list = []
    dir_lsit = []
    for path,foler,files in os.walk(datadir):
        dir_lsit.append(path)
        for each_file in files:
            file = os.path.join(path,each_file)
            file_list.append(file)
    return dir_lsit




def restore_data(cmd):
    status = subprocess.call(cmd,shell=True)





if __name__ == '__main__':
    restore_data(restorecmd)


