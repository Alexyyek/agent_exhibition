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
    cust_delegation = defaultdict(list)
    for line in input_stream:
        vec = line.strip('\n').split('\t')
        cust_pkid = vec[0]
        phone_a = vec[1].strip().replace(' ', '').replace('-', '')
        phone_b = vec[2].strip().replace(' ', '').replace('-', '')
        phone_c = vec[3].strip().replace(' ', '').replace('-', '')
        phones = set()

        if phone_a != '0' and phone_a !='00000000001' and phone_a != '00000000' and phone_a != '':
            phones.add(phone_a)
        if phone_b != '0' and phone_b !='00000000001' and phone_b != '00000000' and phone_b != '':
            phones.add(phone_b)
        if phone_c != '0' and phone_c !='00000000001' and phone_c != '00000000' and phone_c != '':
            phones.add(phone_c)

        creator_code = vec[4]
        created_date = time.strftime('%Y%m%d', time.strptime(vec[5], '%Y-%m-%d %H:%M:%S'))
        if vec[8] != "":
            invalid_date = time.strftime('%Y%m%d', time.strptime(vec[8], '%Y-%m-%d %H:%M:%S'))
        else:
            invalid_date = ""

        delegation = (creator_code, created_date, invalid_date)
        for phone in phones:
            cust_delegation[phone].append(delegation)

    for phone, delegations in cust_delegation.iteritems():
        delegations.sort(key=lambda x:x[1]+x[2])
        print(phone, json.dumps(delegations), sep='\t')

if __name__ == '__main__':
    run(sys.stdin)

