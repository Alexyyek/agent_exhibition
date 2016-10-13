#!/bin/python
#coding=utf-8

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def run():

    type_dict = {"pc":"dtl", "mobile":"dtl", "ershoufang_fav":"fav"}

    for line in sys.stdin:
        line = line.strip()
        if (len(line.split('\t')) != 4):
            continue
        ucid, timestamp, house_pkid, type = line.split('\t')
        if type_dict.has_key(type):
            type = type_dict[type]
        else:
            continue

        print '{ucid}\t{type}\t{timestamp}\t{house_pkid}'.format(
                ucid = ucid,
                type = type,
                timestamp = timestamp,
                house_pkid = house_pkid)

if __name__ == '__main__':
    run()
