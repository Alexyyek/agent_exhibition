RUN_PATH="/home/work/yangyekang/agent/agent_exhibition"

#DICT
UN_MERGE_FEATURE_DICT = {"top_resblock":"common_resblock_cnt"}
CUSTOMER_SCORE_DICT = {"dtl" : 1, "fav" : 5}
AGENT_SCORE_DICT = {"touring" : 1, "contract" : 20}

#FILE
LEGAL_DELEGATION = RUN_PATH+"/data/legal_delegation"
CUSTOMER_RESBLOCK_FNAME = RUN_PATH+"/data/user_resblock"
AGENT_RESBLOCK_FNAME = RUN_PATH+"/data/agent_resblock"
CUSTOMER_FEATURE_FNAME = RUN_PATH+"/data/user_feature"
AGENT_FEATURE_FNAME = RUN_PATH+"/data/agent_feature"
CUSTOMER_STAT_FNAME = RUN_PATH+"/data/user_stat"
AGENT_STAT_FNAME = RUN_PATH+"/data/agent_stat"
CUSTOMER_ONLINE_FEATURE_FNAME = RUN_PATH+"/data/user_online_feature"
MARKET_TREND_FNAME = RUN_PATH+"/data/market_trend"

OUTPT_FNAME = RUN_PATH+"/data/feature_uniform"
