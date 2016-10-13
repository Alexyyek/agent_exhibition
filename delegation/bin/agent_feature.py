#!/bin/python
#coding=utf-8
from __future__ import print_function
from __future__ import division

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json
import datetime as dt
from collections import defaultdict

DELTA_DATE = -15

def run(input_stream):
    agent_del = dict()
    for line in open('inner_data/agent_del_list.txt', 'r'):
        vec = line.strip().split('\t')
        agent_del[vec[0]] = json.loads(vec[1])

    agent_touring = dict()
    for line in open('inner_data/agent_touring_list.txt', 'r'):
        vec = line.strip().split('\t')
        agent_touring[vec[0]] = json.loads(vec[1])

    agent_touring_num = defaultdict(int)
    agent_cust_set = defaultdict(set)
    agent_del_num = defaultdict(int)

    for line in input_stream:
        vec = line.strip().split('\t')
        phone = vec[0]
        agent_code = vec[1]
        del_date = vec[2]

        key = '\t'.join([agent_code, del_date])
        if key not in agent_touring_num:
            dead_date = dt.datetime.strptime(del_date, '%Y%m%d') + dt.timedelta(days=DELTA_DATE)
            if agent_code in agent_touring:
                for (cust_pkid, touring_date) in agent_touring[agent_code]:
                    if dead_date.strftime('%Y%m%d') <= touring_date < del_date:
                        agent_touring_num[key] += 1
                        agent_cust_set[key].add(cust_pkid)

        if key not in agent_del_num:
            for (cust_pkid, created_date, invalid_date) in agent_del[agent_code]:
                if del_date >= created_date and (invalid_date == "" or del_date < invalid_date):
                    agent_del_num[key] += 1

    agents = set(agent_touring_num.keys()).union(agent_del_num.keys())
    for agent in agents:
        feature = { 'agent_15_touring_num' : agent_touring_num[agent], 'agent_15_touring_cust_num' : len(agent_cust_set[agent]), 'agent_del_num' : agent_del_num[agent] }
        print(agent, json.dumps(feature), sep='\t')

if __name__ == '__main__':
    run(sys.stdin)
