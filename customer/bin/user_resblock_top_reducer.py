#!/bin/python
#coding=utf-8

import sys
sys.path.append('./')
from feature_common import CommonFealib
import pdb
import math
import copy
import json
from json import *
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

house_field_list=["house_pkid","hdic_id","resblock_id","resblock_name","buildYear","buildArea","buildUsage"]
meanPrice_fliedname="meanPrice"

def get_user_resblock_top(topN, FAV_SCORE, DTL_SCORE, separator='\t'):

    resblock_dict = load_resblock()
    house_dict = load_house(resblock_dict, house_field_list, meanPrice_fliedname)

    for line in sys.stdin:
        line = line.strip()
        timestamp, detail = line.split(separator)
        user_json = json.loads(detail)
        phone = user_json["phone"]

        hot_resblock_fav_dict = dict()
        hot_resblock_dtl_dict = dict()

        if user_json.has_key("fav"):
            favs = user_json["fav"]
            for fav in favs:
                house = fav["house_pkid"][-8:]
                ts = time_format(fav["ts"])
                if house_dict.has_key(house):
                    house_vec = house_dict[house]
                    resblock_id = house_vec['resblock_id']
                    if ts <= timestamp:
                        #hot resblock list extract
                        if not hot_resblock_fav_dict.has_key(resblock_id):
                            hot_resblock_fav_dict[resblock_id] = FAV_SCORE
                        else:
                            hot_resblock_fav_dict[resblock_id] += FAV_SCORE

        if user_json.has_key("dtl"):
            dtls = user_json["dtl"]
            for dtl in dtls:
                house = dtl["house_pkid"][-8:]
                ts = time_format(dtl["ts"])
                if house_dict.has_key(house):
                    house_vec = house_dict[house]
                    resblock_id = house_vec['resblock_id']
                    if ts <= timestamp:
                        #hot resblock list extract
                        if not hot_resblock_dtl_dict.has_key(resblock_id):
                            hot_resblock_dtl_dict[resblock_id] = DTL_SCORE
                        else:
                            hot_resblock_dtl_dict[resblock_id] += DTL_SCORE

        resblock_dict = dict()
        for resblock, score in hot_resblock_dtl_dict.iteritems():
            if not resblock_dict.has_key(resblock):
                resblock_dict[resblock] = score
            else:
                resblock_dict[resblock] += score

        for resblock, score in hot_resblock_fav_dict.iteritems():
            if not resblock_dict.has_key(resblock):
                resblock_dict[resblock] = score
            else:
                resblock_dict[resblock] += score

        sorted_resblock_dict = sorted(resblock_dict.iteritems(), key=lambda d: int(d[1]), reverse=True)

        resblock_top_lst = []
        limit = min(topN, len(sorted_resblock_dict))
        for i in range(limit):
            resblock_top_lst.append(sorted_resblock_dict[i][0])
            i += 1

        # print hot resblock list
        user_resblock_dict = dict()
        user_resblock_dict["top_resblock"] = resblock_top_lst
        user_resblock_json = JSONEncoder().encode(user_resblock_dict)

        if len(resblock_top_lst) > 0:
            print '{phone}\t{timestamp}\t{user_resblock_json}'.format(
                        phone = phone,
                        timestamp = timestamp,
                        user_resblock_json = user_resblock_json)


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
    topN = int(sys.argv[1])
    FAV_SCORE = int(sys.argv[2])
    DTL_SCORE = int(sys.argv[3])

    get_user_resblock_top(topN, FAV_SCORE, DTL_SCORE)
