#!/bin/python
from __future__ import print_function
from __future__ import division

import sys

def run(input_stream):
    cust = dict()
    for line in input_stream:
        vec = line.strip().split('\t')
        cust_pkid = vec[0]
        phone_a = vec[1].strip().replace(' ', '').replace('-', '')
        phone_b = vec[2].strip().replace(' ', '').replace('-', '')
        phone_c = vec[3].strip().replace(' ', '').replace('-', '')
        if phone_a != '00000000001' and phone_a != '0' and phone_a != '':
            print(phone_a, cust_pkid, sep='\t')
        if phone_b != '00000000001' and phone_b != '0' and phone_b != '' and phone_b != phone_a:
            print(phone_b, cust_pkid, sep='\t')
        if phone_c != '00000000001' and phone_c != '0' and phone_c != '' and phone_c != phone_a and phone_c != phone_b:
            print(phone_c, cust_pkid, sep='\t')

if __name__ == '__main__':
    run(sys.stdin)
