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
    agent_touring = defaultdict(list)
    for line in input_stream:
        vec = line.strip('\n').split('\t')
        cust_pkid = vec[0]
        agent_code = vec[1]
        touring_date = time.strftime('%Y%m%d', time.strptime(vec[2], '%Y-%m-%d %H:%M:%S'))
        agent_touring[agent_code].append((cust_pkid, touring_date))

    for agent_code, tourings in agent_touring.iteritems():
        tourings.sort(key=lambda x:x[1])
        print(agent_code, json.dumps(tourings), sep='\t')

if __name__ == '__main__':
    run(sys.stdin)

