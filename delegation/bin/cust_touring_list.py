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
    cust_phone = defaultdict(set)
    for line in open('inner_data/phone_cust.txt', 'r'):
        vec = line.strip().split('\t')
        cust_phone[vec[1]].add(vec[0])

    phone_touring = defaultdict(list)
    for line in input_stream:
        vec = line.strip('\n').split('\t')
        cust_pkid = vec[0]
        if cust_pkid not in cust_phone:
            continue
        agent_code = vec[1]
        touring_date = time.strftime('%Y%m%d', time.strptime(vec[2], '%Y-%m-%d %H:%M:%S'))
        for phone in cust_phone[cust_pkid]:
            phone_touring[phone].append((agent_code, touring_date))

    for phone, tourings in phone_touring.iteritems():
        tourings.sort(key=lambda x:x[1])
        print(phone, json.dumps(tourings), sep='\t')

if __name__ == '__main__':
    run(sys.stdin)

