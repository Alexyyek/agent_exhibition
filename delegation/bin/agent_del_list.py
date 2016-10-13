#!/bin/python
#coding=utf-8
from __future__ import print_function
from __future__ import division

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import json

from collections import defaultdict

def run(input_stream):
    agent_delegation = defaultdict(list)
    for line in input_stream:
        vec = line.strip('\n').split('\t')
        cust_pkid = vec[0]
        creator_code = vec[4]
        created_date = time.strftime('%Y%m%d', time.strptime(vec[5], '%Y-%m-%d %H:%M:%S'))
        holder_code = vec[6]
        holder_date = time.strftime('%Y%m%d', time.strptime(vec[7], '%Y-%m-%d %H:%M:%S'))
        if vec[8] != "":
            invalid_date = time.strftime('%Y%m%d', time.strptime(vec[8], '%Y-%m-%d %H:%M:%S'))
        else:
            invalid_date = ""

        if creator_code == holder_code or holder_code == 'NULL':
            delegation = (cust_pkid, created_date, invalid_date)
            agent_delegation[creator_code].append(delegation)
        else:
            delegation = (cust_pkid, created_date, holder_date)
            agent_delegation[creator_code].append(delegation)

            delegation = (cust_pkid, holder_date, invalid_date)
            agent_delegation[holder_code].append(delegation)

    for agent_code, delegations in agent_delegation.iteritems():
        delegations.sort(key=lambda x:x[1]+x[2])
        print(agent_code, json.dumps(delegations), sep='\t')

if __name__ == '__main__':
    run(sys.stdin)

