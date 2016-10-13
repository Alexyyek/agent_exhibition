#!/bin/python
#coding=utf-8

import sys
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

def run(start_date, end_date, separator='\t'):

    # extract dtl & fav
    phone_ucid_dict = dict()
    type_dict = {"ershoufang_fav":"fav", "mobile":"dtl", "pc":"dtl"}
    for line in open('ucid_mobile','r'):
        line = line.strip()
        if len(line.split(separator)) != 2 : continue
        ucid, phone = line.split(separator)
        phone = phone.replace("-","")
        if ucid != "" and phone != "":
            phone_ucid_dict[ucid] = phone

    # filter spider user
    spider_set = set()
    for line in open('spider','r'):
        line = line.strip()
        spider_set.add(line)


    for line in sys.stdin:
        line = line.strip()
        if len(line.split(separator)) != 4 : continue
        ucid, timestamp, house_pkid, type = line.split(separator)
        # train data period
        if isFit(timestamp, start_date, end_date):
            pass
        else:
            continue
        # remain house fav & build mapping
        if not type_dict.has_key(type):
            continue
        else:
            type = type_dict[type]
        if phone_ucid_dict.has_key(ucid):
            phone = phone_ucid_dict[ucid]
            if not phone in spider_set:
                print '{ucid}\t{phone}\t{type}\t{timestamp}\t{house_pkid}'.format(
                        ucid = ucid,
                        phone = phone,
                        type = type,
                        timestamp = timestamp,
                        house_pkid = house_pkid)

def isFit(timestamp, start_date, end_date):
    timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    start_date = '2016-04-01'
    end_date = '2016-07-31'
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    if timestamp >= start_date and timestamp <= end_date:
        return True
    else:
        return False

if __name__ == "__main__":
    start_date=sys.argv[1]
    end_date=sys.argv[2]
    run(start_date, end_date)
