#!/bin/python
#coding=utf-8

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def run():
    uuid_dict = dict()
    for line in open('uuid_dict','r'):
        line = line.strip()
        uuid, ucid, timestamp = line.split('\t')
        uuid_dict[uuid] = ucid

    for line in sys.stdin:
        line = line.strip()
        if (len(line.split('\t')) != 5):
            continue
        uuid, ucid, timestamp, house_pkid, type = line.split('\t')
        if ucid.find("NULL") == -1:
            print '{user_id}\t{timestamp}\t{house_pkid}\t{type}'.format(
                    user_id = ucid,
                    timestamp = timestamp,
                    house_pkid = house_pkid,
                    type = type)
        elif uuid.find("NULL") == -1:
            if uuid_dict.has_key(uuid):
                print '{user_id}\t{timestamp}\t{house_pkid}\t{type}'.format(
                        user_id = uuid_dict[uuid],
                        timestamp = timestamp,
                        house_pkid = house_pkid,
                        type = type)
        else:
            continue

if __name__ == '__main__':
    run()
