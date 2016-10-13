#!/bin/python
#coding=utf-8

import os
import sys
import pdb
import json
from feature_common import CommonFealib

sys.path.append("../conf")
import conf

reload(sys)
sys.setdefaultencoding=('utf-8')


class FeatureUniformCreator:

    # load feature [customer : dtl & fav],[agent : touring & contract]
    # @param input_fname
    # @param type_score_dict
    # @param isMerge
    def load_feature_merge(self, input_fname, type_score_dict, isMerge):

        user_dict = dict()

        for line in open(input_fname, 'r'):
            line = line.strip()
            user, timestamp, details = line.split('\t')
            key = '{user}\t{timestamp}'.format(
                    user = user,
                    timestamp = timestamp)
            details = json.loads(details)
            user_dict[key] = dict()
            if isMerge:
                details = self.get_merge(details, type_score_dict)
            else:
                details = self.get_no_merge(details)
            user_dict[key].update(details)

        return user_dict

    def get_merge(self, details, type_score_dict):

        common = CommonFealib()

        res_dict = dict()
        for user_type, user_value in details.iteritems():
            for feature_key, feature_val in user_value.iteritems():
                feature_key = common.globalEncoded(user_type, feature_key)
                if not res_dict.has_key(feature_key):
                    res_dict[feature_key] = feature_val * type_score_dict[user_type]
                else:
                    res_dict[feature_key] += feature_val * type_score_dict[user_type]
        return res_dict

    def get_no_merge(self, details):

        common = CommonFealib()

        res_dict = dict()
        for user_type, user_value in details.iteritems():
            for feature_key, feature_val in user_value.iteritems():
                feature_key = common.globalEncoded(user_type, feature_key, 0)
                res_dict[feature_key] = feature_val
        return res_dict

    # load feature [customer : online & offline],[agent : offline]
    # @param input_fname
    def load_feature(self, user_dict, input_fname, isMerge):

        common = CommonFealib()

        for line in open(input_fname, 'r'):
            line = line.strip()
            user, timestamp, details = line.split('\t')
            key = '{user}\t{timestamp}'.format(
                    user = user,
                    timestamp = timestamp)
            details = json.loads(details)
            for type, value in details.iteritems():
                if isMerge:
                    type = common.globalEncoded(type)
                else:
                    type = common.globalEncoded(type, 1, isMerge)
                if not user_dict.has_key(key):
                    user_dict[key] = dict()
                    user_dict[key][type] = value
                else:
                    user_dict[key][type] = value
        return user_dict

    # load feature similarity between customer and agent:resblock
    # @param input_fname
    def load_resblock(self, resblock_feature_fname):

        resblock_dict = dict()

        for line in open(resblock_feature_fname, 'r'):
            line = line.strip()
            user, timestamp, details = line.split('\t')
            key = '{user}\t{timestamp}'.format(
                    user = user,
                    timestamp = timestamp)
            details = json.loads(details)
            if not resblock_dict.has_key(key):
                resblock_dict[key] = dict()
                resblock_dict[key].update(details)
            else:
                resblock_dict[key].update(details)
        return resblock_dict

    # load feature with time influence
    # @param input_fname
    def load_market(self, market_feature_fname):

        market_trend_dict = dict()

        for line in open(market_feature_fname, 'r'):
            line = line.strip()
            timestamp, details = line.split('\t')
            details = json.loads(details)
            market_trend_dict[timestamp] = dict()
            market_trend_dict[timestamp].update(details)
        return market_trend_dict

def run(isMerge):

    #feature
    un_merge_feature_dict = conf.UN_MERGE_FEATURE_DICT
    customer_score_dict = conf.CUSTOMER_SCORE_DICT
    agent_score_dict = conf.AGENT_SCORE_DICT

    #file
    legal_delegation_fname = conf.LEGAL_DELEGATION
    customer_resblock_fname = conf.CUSTOMER_RESBLOCK_FNAME
    agent_resblock_fname = conf.AGENT_RESBLOCK_FNAME
    customer_feature_fname = conf.CUSTOMER_FEATURE_FNAME
    agent_feature_fname = conf.AGENT_FEATURE_FNAME
    customer_stat_fname = conf.CUSTOMER_STAT_FNAME
    agent_stat_fname = conf.AGENT_STAT_FNAME
    customer_online_feature_fname = conf.CUSTOMER_ONLINE_FEATURE_FNAME
    market_trend_fname = conf.MARKET_TREND_FNAME

    outpt_fname = conf.OUTPT_FNAME
    outpt_file = open(outpt_fname, 'w')

    #lib
    common = CommonFealib()
    creator = FeatureUniformCreator()

    #data
    customer_dict = creator.load_feature_merge(customer_feature_fname, customer_score_dict, isMerge)
    customer_dict = creator.load_feature(customer_dict, customer_stat_fname, isMerge)
    customer_dict = creator.load_feature(customer_dict, customer_online_feature_fname, isMerge)

    agent_dict = creator.load_feature_merge(agent_feature_fname, agent_score_dict, isMerge)
    agent_dict = creator.load_feature(agent_dict, agent_stat_fname, isMerge)

    customer_resblock_dict = creator.load_resblock(customer_resblock_fname)
    agent_resblock_dict = creator.load_resblock(agent_resblock_fname)
    market_trend_dict = creator.load_market(market_trend_fname)

    #feature uniform
    for line in open(legal_delegation_fname):
        customer, agent, timestamp, flag = line.strip().split('\t')
        agent_key = '{agent}\t{timestamp}'.format(agent = agent, timestamp = timestamp)
        customer_key = '{customer}\t{timestamp}'.format(customer = customer, timestamp = timestamp)
        outpt_dict = dict()

        # customer & agent feature
        if customer_dict.has_key(customer_key):
            for feature_key, feature_val in customer_dict[customer_key].iteritems():
                outpt_dict[feature_key] = feature_val


            if agent_dict.has_key(agent_key):
                for feature_key, feature_val in agent_dict[agent_key].iteritems():
                    outpt_dict[feature_key] = feature_val

            # similarity feature between customer and agent
            if customer_resblock_dict.has_key(customer_key) and agent_resblock_dict.has_key(agent_key):
                for feature_key in un_merge_feature_dict.keys():
                    customer_set = set(customer_resblock_dict[customer_key][feature_key])
                    agent_set = set(agent_resblock_dict[agent_key][feature_key])
                    intersection = customer_set.intersection(agent_set)
                    feature_key = common.globalEncoded(un_merge_feature_dict[feature_key], 1, isMerge)
                    outpt_dict[feature_key] = len(intersection)

            # market trend feature
            if market_trend_dict.has_key(timestamp):
                for type in market_trend_dict[timestamp]:
                    code = common.globalEncoded(type, 1, isMerge)
                    outpt_dict[code] = market_trend_dict[timestamp][type]

            outpt_str = '{flag}\t{customer}\t{agent}\t{timestamp}'.format(
                          flag = flag,
                          customer = customer,
                          agent = agent,
                          timestamp = timestamp)

            ordered_dict = sorted(outpt_dict.iteritems(), key=lambda d:int(d[0]), reverse = False)
            for item in ordered_dict:
                outpt_str += '\t' + str(item[0]) + ':' + str(item[1])
            outpt_file.write(outpt_str + '\n')

if __name__ == "__main__":
    isMerge = int(sys.argv[1])
    run(isMerge)
