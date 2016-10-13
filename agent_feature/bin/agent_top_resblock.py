#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2014 lianjia.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: make_agent_json.py
Author: liuyu02(liuyu16@lianjia.com)
Date: 2016/07/28 21:14:09
Brief: make agent json
"""
import optparse
import os
import shutil
import sys
import ConfigParser
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


house_field_list = ["house_pkid", "hdic_id", "resblock_id", "resblock_name", "buildYear", "buildArea", "buildUsage"]
meanPrice_fliedname = "meanPrice"
action_type_list = ["touring", "contract"]
weight_dict = {action_type_list[0]: "touring_weight", action_type_list[1]: "contract_weight"}
top_resblock_feature_name = "top_resblock"


def mapper(input_str):
    """
        parser legal_delegation
    """
    for line in input_str:
        line_list = line.strip(' ').strip('\n').split('\t')
        if len(line_list) < 3:
            continue
        agent_id = line_list[1]
        ts = line_list[2]
        print "{agent_id}\t{timestamp}".format(
                                          agent_id = agent_id,
                                          timestamp = ts
                                       )

def parser_meanprice(input_file, out_dict):
    """
        parser resblok meanprice
    """
    file_r = open(input_file, 'r')
    for line in file_r:
        line_list = line.strip(' ').strip('\n').split('\t')
        if len(line_list) < 3:
            continue
        res_id = line_list[0]
        price = line_list[2]
        out_dict.update({res_id: price})
    file_r.close()


def parser_house(input_file, meanprice_dict, out_dict):
    """
        parser house to dict:
        key is house_pkid 
    """
    file_r = open(input_file, 'r')
    for line in file_r:
        line_list = line.strip(' ').strip('\n').split('\t')
        if len(line_list) < len(house_field_list):
            continue
        tmp_dict = dict()
        house_pkid = line_list[0]
        for i in range(1, len(house_field_list)):
            tmp_dict.update({house_field_list[i]:line_list[i]})

        if line_list[2] in meanprice_dict:
            tmp_dict.update({meanPrice_fliedname: meanprice_dict[line_list[2]]})
        else:
            tmp_dict.update({meanPrice_fliedname:0})

        out_dict.update({house_pkid:tmp_dict})
    file_r.close()

def parser_agent_json(input_file, out_dict):
    """
        parser agent json to dict:
        key is agent_code
    """
    file_r = open(input_file, 'r')
    for line in file_r:
        line_list = line.strip(' ').strip('\n').split('\t')
        if len(line_list) < 2:
            continue
        agent_id = line_list[0]

        agent_info = dict()
        agent_info = json.loads(line_list[1])
        out_dict.update({agent_id:agent_info})
    file_r.close()

def reducer(input_str):
    ##meanprice
    meanprice_dict = dict()
    parser_meanprice("resblock_meanprice", meanprice_dict)
    house_dict = dict()
    parser_house("house_detail", meanprice_dict, house_dict)
    meanprice_dict = dict()
    agent_dict = dict()
    parser_agent_json("agent_json", agent_dict)


    flag_agent = ""
    flag_ts = ""
    feature_dict = dict()
    for line in input_str:
        line_list = line.strip(' ').strip('\n').split('\t')
        if len(line_list) < 2:
            continue
        agent=line_list[0]
        ts = line_list[1]
        if agent not in agent_dict:
            continue

        if (flag_agent == ""  and flag_ts == "") or (flag_agent == agent and flag_ts == ts):
            flag_agent = agent
            flag_ts = ts
        elif flag_agent != agent or flag_ts != ts:
            agent_info_dict = agent_dict[flag_agent]
            add_data(feature_dict, flag_agent, flag_ts, agent_info_dict, house_dict)
            print_data(feature_dict, flag_agent, flag_ts)
            flag_ts = ts
            flag_agent = agent
            feature_dict = dict()
            
    if flag_agent != "":
        add_data(feature_dict, flag_agent, flag_ts, agent_info_dict, house_dict)
        print_data(feature_dict, flag_agent, flag_ts)
        flag_agent = ""
        flag_ts = ""
        feature_dict = dict()


def add_data(output_dict, agent, ts, agent_info_dict, house_dict):
    """
        add data into agent_dict
    """
    tmp_dict = dict()
    for action_type in action_type_list:
        if action_type in agent_info_dict:
            for action_info in agent_info_dict[action_type]:
                if ts > action_info["ts"]:
                    house_pkid = action_info["house_pkid"]
                    if house_pkid in house_dict:
                        resblock_id = house_dict[house_pkid][house_field_list[2]]
                        if resblock_id in tmp_dict:
                            tmp_dict[resblock_id] += 1 * eval(weight_dict[action_type])
                        else:
                            tmp_dict[resblock_id] = 1 * eval(weight_dict[action_type])


    sorted_resblock = []
    resblock_dict = tmp_dict
    sorted_resblock = sorted(resblock_dict.iteritems(), key=lambda resblock_dict:resblock_dict[1], reverse = True)
    output_dict.update({top_resblock_feature_name:[]})
    if len(sorted_resblock) > 20:
        max_len = 20
    else:
        max_len = len(sorted_resblock)
    for i in range(max_len):
        tmp_res = sorted_resblock[i]
        output_dict[top_resblock_feature_name].append(tmp_res[0])



def print_data(input_dict, agent, ts):
    """
        print data into json
    """
    #if "contract" in agent_dict:
    #    if "touring" in agent_dict:
    #        print "agent:%s\ttouring:%d\tcontract:%d" % (agent, len(agent_dict["touring"]), len(agent_dict["contract"]))

    print_str = "{agent}\t{ts}\t{feature_json}".format(
                                                agent = agent,
                                                ts = ts,
                                                feature_json = json.dumps(input_dict)
                                               )
    print print_str


if __name__ == '__main__':
    #touring_weight=1
    #contract_weight=20

    if sys.argv[1] == "mapper":
        mapper(sys.stdin)
    elif sys.argv[1] == "reducer":
        touring_weight = int(sys.argv[2])
        contract_weight = int(sys.argv[3])
        reducer(sys.stdin)
