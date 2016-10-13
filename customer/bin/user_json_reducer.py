#!/bin/python
#coding=utf-8

import sys
import copy
from json import *

reload(sys)
sys.setdefaultencoding('utf-8')

def run(input):

    current_ucid = ""
    ucid = ""
    user_dict = dict()

    for line in sys.stdin:
        line = line.strip()
        if (len(line.split('\t')) != 5):
            continue
        ucid, phone, type, timestamp, house_pkid = line.split('\t')
        if current_ucid == ucid:
            if not user_dict.has_key(type):
                user_dict[type] = []
            dtl_format(user_dict, type, timestamp, house_pkid)
        else:
            if current_ucid:
                user_json = JSONEncoder().encode(user_dict)
                print user_json
            current_ucid = ucid
            user_dict.clear()
            user_dict["ucid"] = ucid
            user_dict["phone"] = phone
            user_dict[type] = []
            dtl_format(user_dict, type, timestamp, house_pkid)
    if current_ucid == ucid:
        user_json = JSONEncoder().encode(user_dict)
        print user_json

def dtl_format(user_dict, type, timestamp, house_pkid):
    type_dict = dict()
    type_dict["ts"] = timestamp
    type_dict["house_pkid"] = house_pkid
    user_dict[type].append(copy.deepcopy(type_dict))
    type_dict.clear()

if __name__ == '__main__':
    run(sys.stdin)
