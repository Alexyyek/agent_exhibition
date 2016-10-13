#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2014 lianjia.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: market_trend_join.py
Author: liuyu02(liuyu16@lianjia.com)
Date: 2016/07/28 21:14:09
Brief: make market 15 showing and 15 contract
"""
import optparse
import os
import shutil
import sys
import ConfigParser
import json
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

begain_date = "2016-04-01"
end_date = "2016-07-31"
date_format = "%Y-%m-%d"
date_param = {"begain_date": begain_date, 
              "end_date": end_date, 
              "date_format":date_format }




def parser_every_data(input_file, output_dict):
    """
        parser showing and contact for everyday
    """
    file_r = open(input_file, 'r')
    for line in file_r:
        line_list = line.strip('\n').strip(' ').split('\t')
        action_type = line_list[0]
        action_date = line_list[1]
        action_cnt = line_list[2]
        if action_type not in output_dict:
            output_dict[action_type] = dict()
        output_dict[action_type][action_date] = int(action_cnt)

    file_r.close()

def merge_date_data(date_param, output_dict, acion_type, date_span, input_every_dict):
    """
        date_param = {begain_date:"", end_date:"", date_format:""}
        acion_type = "contract_cnt" "touring_cnt"
    """
    date_format = date_param["date_format"]
    d0 = datetime.datetime.strptime(date_param["begain_date"], date_format)
    d1 = datetime.datetime.strptime(date_param["end_date"], date_format)
    while d0 <= d1:
        merge_date_str = []
        make_date_list(d0, date_span, merge_date_str)
        merge_cnt = 0
        for tmp_date_str in merge_date_str:
            if tmp_date_str in input_every_dict[acion_type]:
                merge_cnt += input_every_dict[acion_type][tmp_date_str]
            else:
                print acion_type + "\t" + tmp_date_str
        output_dict.update({d0.strftime(date_format): merge_cnt})
        d0 = d0 + datetime.timedelta(days=1)


def make_date_list(input_end_date, date_span, output_list):
    """
        make date list 
    """
#    end_date = datetime.datetime.strptime(end_date_str, date_format)
    for i in range(date_span):
        tmp_date = input_end_date - datetime.timedelta(days=i)
        tmp_date_str = tmp_date.strftime(date_format)
        output_list.append(tmp_date_str)
    output_list.sort()
        
def print_market_feature(contract_input_dict,touring_input_dict, out_file):
    """
        action_type: contract_cnt, touring_cnt
    """
    file_w = open(out_file, "w")
    tmp_str = ""
    for tmp_date in touring_input_dict:
        tmp_dict = {"touring_cnt": touring_input_dict[tmp_date]}

        if tmp_date in contract_input_dict:
            tmp_dict.update({"contract_cnt": contract_input_dict[tmp_date]})
        tmp_str += "{key}\t{feature}\n".format(
                                             key = tmp_date.replace("-", ""),
                                             feature = json.dumps(tmp_dict)
                                           )
    file_w.write(tmp_str)
    file_w.close()



if __name__ == '__main__':
    input_file = sys.argv[1]
    out_file = sys.argv[2]

    house_every_dict = dict()
    parser_every_data(input_file, house_every_dict)
#    print house_every_dict

    contract_cnt_dict = dict()
    merge_date_data(date_param, contract_cnt_dict, "contract_cnt", 15, house_every_dict)

    touring_cnt_dict = dict()
    merge_date_data(date_param, touring_cnt_dict, "touring_cnt", 15, house_every_dict)

    print_market_feature(contract_cnt_dict, touring_cnt_dict, out_file)
