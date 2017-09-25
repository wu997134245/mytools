# coding=utf-8
import re
import sys
'''修改cmdf.txt文件'''




def mod_file(file):
    datadict = {}
    with open(file) as fobj:
        for line in fobj:
            linelist = line.split('!')
            try:
                id = linelist[0]
                replace = linelist[1].strip()
            except IndexError:
                continue
            datadict[id] = replace
    return datadict


def list_replace(file, datadict, num=1):
    with open(file) as fobj:
        data = fobj.read()
    for i in datadict:
        id = i
        replace = datadict[i]
        m = re.findall('(%s)!(.+?)!' % (id), data)
        if not m:
            continue
        data = data.replace(m[0][num], replace)
    with open(file, 'w') as fobj:
        fobj.write(data)


def main(modfile, datafile):
    datadict = mod_file(modfile)
    list_replace(datafile, datadict)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
