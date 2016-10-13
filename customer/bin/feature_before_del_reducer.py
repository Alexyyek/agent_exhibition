#!/bin/python
#coding=utf-8

import sys
import datetime
import json

reload(sys)
sys.setdefaultencoding('utf-8')

def run(day_distance):

    user_dict = dict()
    for line in open('legal_delegation','r'):
        line = line.strip()
        phone, agent, timestamp, flag = line.split('\t')
        user_dict[phone] = timestamp

    phone_dict = dict()
    for line in open('ucid_mobile','r'):
        try:
            line = line.strip()
            ucid, phone = line.split('\t')
            phone_dict[ucid] = phone
        except Exception:
            continue

    user_feature_dict = dict()
    for line in sys.stdin:
        line = line.strip()
        if (len(line.split('\t')) != 4):
            continue
        ucid, type, timestamp, house_pkid = line.split('\t')

        if phone_dict.has_key(ucid) and user_dict.has_key(phone_dict[ucid]):
            phone = phone_dict[ucid].strip()
            del_time = user_dict[phone].strip()
            key = '{phone}\t{del_time}'.format(
                    phone = phone,
                    del_time = del_time)
            if not user_feature_dict.has_key(key):
                user_feature_dict[key] = dict()
                user_feature_dict[key]["dtl"] = set()
                user_feature_dict[key]["fav"] = set()

            flag = isFit(timestamp, del_time, day_distance)
            if flag:
                user_feature_dict[key][type].add(house_pkid)
            else:
                continue
    return user_feature_dict

def get_user_feature(user_feature_dict):

    for key, type_dict in user_feature_dict.iteritems():
        phone, timestamp = key.split('\t')
        outpt_dict = dict()
        outpt_dict["fav_cnt"] = len(user_feature_dict[key]["fav"])
        outpt_dict["dtl_cnt"] = len(user_feature_dict[key]["dtl"])
        outpt_json = json.dumps(outpt_dict)
        if outpt_dict["fav_cnt"] > 0 or outpt_dict["dtl_cnt"] > 0:
            print '{phone}\t{timestamp}\t{outpt_json}'.format(
                    phone = phone,
                    timestamp = timestamp,
                    outpt_json = outpt_json)

def isFit(timestamp, del_time, DAY_DICTANCE):
    timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    del_time = datetime.datetime.strptime(del_time, '%Y%m%d')
    if (del_time > timestamp) and (del_time - timestamp).days <= DAY_DICTANCE:
        return True
    else:
        return False

if __name__ == '__main__':
    day_distance = int(sys.argv[1])
    user_feature_dict = run(day_distance)
    get_user_feature(user_feature_dict)
