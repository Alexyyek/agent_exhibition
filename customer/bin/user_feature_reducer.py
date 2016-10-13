#!/bin/python
#coding=utf-8

import sys
sys.path.append('./')
from feature_common import CommonFealib
import math
import copy
import json
from json import *
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

house_field_list = ["house_pkid","hdic_id","resblock_id","resblock_name","buildYear","buildArea","buildUsage"]
feature_field_list = ["buildYear","buildArea","meanPrice","buildUsage"]
action_type_list = ["dtl","fav"]
meanPrice_fliedname = "meanPrice"

def get_feature_json(separator='\t'):


    resblock_dict = load_resblock()
    house_dict = load_house(resblock_dict, house_field_list, meanPrice_fliedname)

    for line in sys.stdin:
        line = line.strip()
        del_time, detail = line.split(separator)
        user_json = json.loads(detail)
        phone = user_json["phone"]

        user_dict = dict()

        for action_type in action_type_list:
            if user_json.has_key(action_type):
                user_dict[action_type] = dict()
                details = user_json[action_type]
                for detail in details:
                    ts = time_format(detail["ts"])
                    house = detail["house_pkid"][-8:]
                    if house_dict.has_key(house) and ts <= del_time:
                        common = CommonFealib()
                        for field in feature_field_list:
                            common.updateFea(house_dict[house][field], field, user_dict[action_type])

        user_dict = JSONEncoder().encode(user_dict)
        outpt_str = '{phone}\t{timestamp}\t{user_dict}'.format(
                      phone = phone,
                      timestamp = del_time,
                      user_dict = user_dict)
        print outpt_str

def load_resblock():
    resblock_dict = dict()
    for line in open('resblock_price','r'):
        line = line.strip()
        resblock_id, resblock_name, price = line.split('\t')
        resblock_dict[resblock_id] = price
    return resblock_dict

def load_house(resblock_dict, house_field_list, meanPrice_fliedname):
    res_dict = dict()
    for line in open('house_detail','r'):
        house_dict = dict()
        line = line.strip()
        details = line.split('\t')
        house_pkid = details[0][-8:]
        for i in range(1, len(house_field_list)):
            house_dict.update({house_field_list[i]:details[i]})
        if resblock_dict.has_key(details[2]):
            house_dict.update({meanPrice_fliedname:resblock_dict[details[2]]})
        else:
            house_dict.update({meanPrice_fliedname:0})
        res_dict.update({house_pkid:house_dict})
    return res_dict

def time_format(timestamp):
    timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    timestamp = datetime.datetime.strftime(timestamp, '%Y%m%d')
    return timestamp

if __name__ == '__main__':

    get_feature_json()
