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
    cust_del = dict()
    for line in open('inner_data/cust_del_list.txt', 'r'):
        vec = line.strip().split('\t')
        cust_del[vec[0]] = json.loads(vec[1])

    cust_touring = dict()
    for line in open('inner_data/cust_touring_list.txt', 'r'):
        vec = line.strip().split('\t')
        cust_touring[vec[0]] = json.loads(vec[1])

    cust_touring_num = defaultdict(int)
    cust_agent_set = defaultdict(set)
    cust_del_num = defaultdict(int)

    for line in input_stream:
        vec = line.strip().split('\t')
        phone = vec[0]
        agent_code = vec[1]
        del_date = vec[2]

        key = '\t'.join([phone, del_date])
        if key not in cust_touring_num and phone in cust_touring:
            dead_date = dt.datetime.strptime(del_date, '%Y%m%d') + dt.timedelta(days=DELTA_DATE)
            for (agent_code, touring_date) in cust_touring[phone]:
                if dead_date.strftime('%Y%m%d') <= touring_date < del_date:
                    cust_touring_num[key] += 1
                    cust_agent_set[key].add(agent_code)

        if key not in cust_del_num and phone in cust_del:
            for (agent_code, created_date, invalid_date) in cust_del[phone]:
                if del_date >= created_date and (invalid_date == "" or del_date < invalid_date):
                    cust_del_num[key] += 1

    custs = set(cust_touring_num.keys()).union(cust_del_num.keys())
    for cust in custs:
        feature = { 'cust_15_touring_num' : cust_touring_num[cust], 'cust_15_touring_agent_num' : len(cust_agent_set[cust]), 'cust_del_num' : cust_del_num[cust] }
        print(cust, json.dumps(feature), sep='\t')

if __name__ == '__main__':
    run(sys.stdin)
