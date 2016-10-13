#!/bin/python
#coding=utf-8

res_dict = dict()
line_num = 1
for line in open('pred.txt','r'):
    line = float(line.strip())
    if line > 0.5:
        line = 1
    else:
        line = 0
    res_dict[line_num] = line
    line_num += 1

line_num = 1
for line in open('merge_after/test_6','r'):
    line = line.strip()
    phone, agent, ts, flag, details = line.split('\t',4)
    print phone + '\t' + agent + '\t' + ts + '\t' + str(res_dict[line_num]) + '\t' + flag
    line_num += 1
