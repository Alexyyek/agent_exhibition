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


def run(input_str):
    flag_agent = ""
    agent_dict = dict()
    for line in input_str:
        line_list = line.strip(' ').strip('\n').split('\t')
        if len(line_list) < 6:
            continue
        tmp_dict = dict()
        agent=line_list[0]
        action_type = line_list[1]
        tmp_dict.update({"ts":line_list[2].replace("-",'')})
        tmp_dict.update({"cust_pkid":line_list[3]})
        tmp_dict.update({"house_pkid":line_list[4]})
        tmp_dict.update({"hdic_id":line_list[5]})
        if flag_agent == "" or flag_agent == agent:
            flag_agent = agent
            add_data(tmp_dict, agent_dict, action_type)
        elif flag_agent != agent:
            print_data(flag_agent, agent_dict)
            flag_agent = agent
            agent_dict = dict()
            add_data(tmp_dict, agent_dict, action_type)
            
    if flag_agent != "":
        print_data(flag_agent, agent_dict)
        flag_agent = ""
        agent_dict = dict()


def add_data(input_dict, agent_dict, action_type):
    """
        add data into agent_dict
    """
    if action_type not in agent_dict:
        agent_dict.update({action_type:[]})
    agent_dict[action_type].append(input_dict)


def print_data(agent, agent_dict):
    """
        print data into json
    """
    #if "contract" in agent_dict:
    #    if "touring" in agent_dict:
    #        print "agent:%s\ttouring:%d\tcontract:%d" % (agent, len(agent_dict["touring"]), len(agent_dict["contract"]))

    print_str = "{agent}\t{agent_json}".format(
                                                agent = agent,
                                                agent_json = json.dumps(agent_dict)
                                               )
    print print_str


if __name__ == '__main__':
    run(sys.stdin)
