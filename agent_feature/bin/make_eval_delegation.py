#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2014 lianjia.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: make_eval_delegation
Author: liuyu02(liuyu16@lianjia.com)
Date: 2016/07/28 21:14:09
Brief: make eval delegation
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
sys.path.append("./")

def parser_origin_delegation(input_file, output_list, agent_team_dict, team_agent_dict):
    """
       parser origin delegaion
    """
    file_r = open(input_file, 'r')
    for line in file_r:
        line_list = line.strip("\n").strip(" ").split("\t")
        if len(line) < 4:
            continue
        phone = line[0]
        agent_id = line[1]
        timestamp = line[2]
        label = line[3]
        dict_key = "{phone}\t{agent_id}\t{timestamp}".format(
                                                               phone = phone,
                                                               agent_id = agent_id,
                                                               timestamp = timestamp,

                                                           )
        output_list.append(
                        "{line}\t{is_make}".format(line = line.strip("\n").strip(" "), is_make="origin")
                       )
        if agent_id in agent_team_dict:
            agent_team = agent_team_dict[agent_id]
            for other_agent in team_agent_dict[agent_team]:
                if other_agent != agent_id:
                    output_list.append(
                                    "{phone}\t{agent}\t{timestamp}\t{label}\t{is_make}".format(
                                                                            phone = phone,
                                                                            agent = other_agent,
                                                                            timestamp = timestamp,
                                                                            label = label,
                                                                            is_make="trick")
                                              )

    file_r.close()


def parser_agent_team(input_file, agent_team_dict, team_agent_dict):
    """
       parser data to get agent and team map
    """
    file_r = open(input_file, 'r')
    for line in file_r:
        line_list = line.strip("\n").strip(" ").split("\t")
        if len(line) < 5:
            continue
        agent_code = line[1]
        agent_team = line[2]
        #agent team
        agent_team_dict[agent_code] = agent_team
        #team agent
        if agent_team not in team_agent_dict:
            team_agent_dict[agent_team] = set()
            team_agent_dict[agent_team].add(agent_code)
        else:
            team_agent_dict[agent_team].add(agent_code)

    file_r.close()


def print_trick_delegation(input_file, input_list):
    """
       print trick delegation 
    """
    file_w = open(input_file, "w")
    tmp_str = "\n".join(input_list)
    file_w.write(tmp_str)
    file_w.close()
if __name__=='__main__':
    origin_delegation = sys.argv[1]
    user_team = sys.argv[2]
    trick_delegation = sys.argv[3]
    #origin_delegation = "../inner_data/legal_delegation.txt"
    #user_team = "../inner_data/user_team.txt"
    #trick_delegation = "../inner_data/trick_delegaiton.txt"

    agent_team_dict = dict()
    team_agent_dict = dict()
    trick_delegation_list = list()


    parser_agent_team(user_team, agent_team_dict, team_agent_dict)
    parser_origin_delegation(origin_delegation, trick_delegation_list, agent_team_dict, team_agent_dict)
    print_trick_delegation(trick_delegation, trick_delegation_list)
