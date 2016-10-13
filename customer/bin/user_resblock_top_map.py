#!/bin/python
#coding=utf-8

import sys
import json
from json import *

reload(sys)
sys.setdefaultencoding('utf-8')

def run(separator='\t'):

    user_del_dict = dict()
    for line in open('legal_delegation','r'):
        line = line.strip()
        phone, agent, timestamp, type = line.split(separator)
        if not user_del_dict.has_key(phone):
            user_del_dict[phone] = dict()
            user_del_dict[phone][agent] = timestamp
        else:
            user_del_dict[phone][agent] = timestamp

    for line in sys.stdin:
        line = line.strip()
        user_json = json.loads(line)
        phone = user_json["phone"]
        if not user_del_dict.has_key(phone):
            continue
        else:
            time_set = set()
            for agent, timestamp in user_del_dict[phone].iteritems():
                if timestamp in time_set:
                    continue
                else:
                    time_set.add(timestamp)
                    print '{timestamp}\t{user_json}'.format(
                            timestamp = timestamp,
                            user_json = line)

if __name__ == '__main__':
    run()
