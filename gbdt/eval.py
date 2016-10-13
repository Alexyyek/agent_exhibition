#!/bin/python

from __future__ import print_function
from __future__ import division

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def run(input_stream):
    line_num = 1
    pred = dict()
    for line in open('pred.txt', 'r'):
        prob = float(line.strip())
        if prob >= 0.5:
            pred[line_num] = 1
        else:
            pred[line_num] = 0
        line_num += 1

    line_num = 1
    TT, TN, NT, NN = 0, 0, 0, 0
    for line in input_stream:
        vec = line.strip().split('\t')
        result = int(vec[0])
        if pred[line_num] == 1 and result == 1:
            TT += 1
        elif pred[line_num] == 1 and result == 0:
            TN += 1
        elif pred[line_num] == 0 and result == 1:
            NT += 1
        else:
            NN += 1
        line_num += 1

    print('RECALL=', TT / (TT + NT))
    print('PRECISION=', TT / (TT + TN))
    print('ACCURACY=', (TT + NN) / (TT + TN + NT + NN))

if __name__ == '__main__':
    run(open('test.txt', 'r'))
