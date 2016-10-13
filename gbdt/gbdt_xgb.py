#!/bin/python
#coding=utf-8

import sys
sys.path.append('../')
import pandas as pd
import xgboost as xgb
import operator
import pdb
from matplotlib import pylab as plt


# params
params = {'eta': 0.01, 'gamma': 0, 'max_depth': 9, 'min_child_weight' : 10, 'colsample_bytree': 0.9, 'silent':0, 'objective':'binary:logistic', 'lambda' : 10, 'alpha' : 10}

# load data
def load_data(train_fname, test_fname):
    dtrain = xgb.DMatrix(train_fname)
    dtest = xgb.DMatrix(test_fname)
    return dtrain, dtest

# train model
def train_data(train_fname, test_fname):
    dtrain, dtest = load_data(train_fname, test_fname)
    num_round = 50

    # train data
    bst = xgb.train(params, dtrain, num_round)
    # dump model with feature map
    bst.dump_model('dump.raw.txt','featmap.txt')
    # make prediction
    importance = bst.get_fscore(fmap='xgb.fmap')
    importance = sorted(importance.items(), key=operator.itemgetter(1))

    df = pd.DataFrame(importance, columns=['feature', 'fscore'])
    df['fscore'] = df['fscore'] / df['fscore'].sum()

    plt.figure()
    df.plot()
    df.plot(kind='barh', x='feature', y='fscore', legend=False, figsize=(30, 20))
    plt.title('XGBoost Feature Importance')
    plt.xlabel('relative importance')
    plt.gcf().savefig('feature_importance_xgb.png')

# calc the avg & mse of train model
def checkRate(bst, dtest):

    preds = bst.predict(dtest)
    #xgb.plot_importance(bst)
    #preds = preds > 0.5

if __name__ == '__main__':
    train_fname = "train.txt"
    test_fname = "test.txt"
    train_data(train_fname, test_fname)
    #checkRate(bst, dtest)
