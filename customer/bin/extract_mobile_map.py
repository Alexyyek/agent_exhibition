#!/bin/python
#coding=utf-8

import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')

def run(city_id):
    for line in sys.stdin:
        vec = line.strip().split('\t')
        if len(vec) < 25:
            continue
        timestamp = vec[0]
        uuid = vec[2]
        ucid = vec[3]
        city_code = vec[17]
        channel_id = vec[18]
        detail_id = vec[23]
        detail_id_type = vec[24]
        if uuid.strip() == "" or uuid == '\\N':
            uuid = 'NULL'
        if ucid.strip() == "" or ucid == '\\N':
            ucid = 'NULL'
        if detail_id_type == '1' and city_code == city_id and (channel_id == '2' or channel_id == '11' or channel_id == '12' or channel_id == '13'):
            if uuid != 'NULL' or ucid != 'NULL':
                output_str = '{uuid}\t{ucid}\t{timestamp}\t{house_pkid}\tmobile'.format(
                              uuid = uuid,
                              ucid = ucid,
                              timestamp = timestamp,
                              house_pkid = detail_id)
                print output_str

if __name__ == '__main__':
    city_id = str(sys.argv[1])
    run(city_id)
