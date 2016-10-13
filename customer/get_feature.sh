#!/bin/bash
source "./conf/bash_conf.sh"

RUN_PATH=${RUN_PATH}

cd ${RUN_PATH}/data

hadoop fs -getmerge /user/songxin/feature/legal_delegation.txt legal_delegation

hadoop fs -getmerge /user/yangyekang/agent/agent_show/feature/user_feature user_feature

hadoop fs -getmerge /user/songxin/feature/cust_feature.txt user_stat

hadoop fs -getmerge /user/yangyekang/agent/agent_show/feature/user_resblock_top user_resblock

hadoop fs -getmerge /user/yangyekang/agent/agent_show/feature/user_online_feature user_online_feature

hadoop fs -getmerge /user/yangyekang/agent/agent_show/feature/agent_feature agent_feature

hadoop fs -getmerge /user/songxin/feature/agent_feature.txt agent_stat

hadoop fs -getmerge /user/yangyekang/agent/agent_show/feature/agent_resblock_top agent_resblock

hadoop fs -getmerge /user/yangyekang/agent/agent_show/feature/market_trend market_trend

cd ${RUN_PATH}/bin
# merge : 1
# not merge : 0
python feature_uniform.py 1
