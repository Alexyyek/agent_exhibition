#!/bin/python
#coding=utf-8
from __future__ import print_function
from __future__ import division

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import datetime as dt

DELTA_DATE = 7

def run(input_stream):
    agent = dict()
    for line in open("inner_data/agent_info.txt", "r"):
        vec = line.strip().split('\t')
        agent_ucid = vec[0]
        agent_code = vec[1]
        agent[agent_ucid] = agent_code

    call = dict()
    for line in open("inner_data/phone_log.txt", "r"):
        vec = line.strip().split('\t')
        agent_ucid = vec[0]
        if agent_ucid != 'NULL' and agent_ucid in agent:
            agent_code = agent[agent_ucid]
        else:
            agent_code = vec[1]

        caller_number = vec[5].strip().replace(' ', '').replace('-', '')
        if caller_number == '00000000001':
            continue
        callee_number = vec[6].strip().replace(' ', '').replace('-', '')
        start_time = vec[7]
        call_date = time.strftime('%Y%m%d', time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
        call[':'.join([agent_code, caller_number])] = call_date

    touring = dict()
    for line in open("inner_data/touring.txt", "r"):
        vec = line.strip().split('\t')
        cust_pkid = vec[0]
        agent_code = vec[1]
        touring_date = time.strftime('%Y%m%d', time.strptime(vec[2], '%Y-%m-%d %H:%M:%S'))
        touring_key = ':'.join([agent_code, cust_pkid])
        if touring_key not in touring:
            touring[touring_key] = touring_date
        elif touring_date < touring[touring_key]:
            touring[touring_key] = touring_date

    for line in input_stream:
        vec = line.strip().split('\t')
        cust_pkid = vec[0]
        phone_a = vec[1].strip().replace(' ', '').replace('-', '')
        phone_b = vec[2].strip().replace(' ', '').replace('-', '')
        phone_c = vec[3].strip().replace(' ', '').replace('-', '')
        created_code = vec[4]
        created_date = time.strftime('%Y%m%d', time.strptime(vec[6], '%Y-%m-%d %H:%M:%S'))

        if ':'.join([created_code, phone_a]) in call:
            phone = phone_a
        elif ':'.join([created_code, phone_b]) in call:
            phone = phone_b
        elif ':'.join([created_code, phone_c]) in call:
            phone = phone_c
        else:
            continue

        if created_date < call[':'.join([created_code, phone])]: #委托时间在通话时间之前，过滤掉
            continue

        dead_date = dt.datetime.strptime(created_date, '%Y%m%d') + dt.timedelta(days=DELTA_DATE)
        touring_key = ':'.join([created_code, cust_pkid])
        if touring_key in touring and dead_date.strftime('%Y%m%d') >= touring[touring_key]:
            valid = True
        else:
            valid = False

        print(phone, created_code, created_date, valid, sep='\t')

if __name__ == '__main__':
    run(sys.stdin)
