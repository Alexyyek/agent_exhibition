export RUN_PATH="/home/work/liuyu/matchmaker/agent_feature"
#public param
export RUN_DATA_PATH=${RUN_PATH}"/run_data"
export BIN_PATH=${RUN_PATH}"/bin"
export DATA_PATH=${RUN_PATH}"/data"
export INNER_PATH=${RUN_PATH}"/inner_data"
export PYTHON_HDFS_PATH='/user/songxin/tools/python.tgz'
export GLOBAL_HADOOP_HOME="/home/work/bin/hadoop"
export INNER_DATA_PATH="${RUN_PATH}/inner_data"

#data control##############################
#RUN_TIME control run pt
export RUN_TIME="2016-08-03"
export AGENT_HISTORY_BEGAIN_DATE="20150601"
export END_DATE="20160731"
export SAMPLE_BEGAIN_DATE="20160401"
##to before 15 day
export MARKET_TREND_BEGAIN_DATE="20160301"
export CITY_CODE=110000
###to weight
export TOURING_WEIGHT="1"
export CONTRACT_WEIGHT="20"

###########################################



###external depend on data
export LEGAL_DELEGATION="/user/songxin/feature/legal_delegation.txt"
export LEGAL_DELEGATION_FILENAME="legal_delegation.txt"
export RESBLOCK_PRICE="/user/songxin/feature/resblock_price.txt"
export AGENT_TEAM="/user/songxin/feature/user_team.txt"
export AGENT_TEAM_FILENAME="user_team.txt"



##inner data
export HOUSE_FILE_NAME="house_info_${CITY_CODE}_${END_DATE}"
export HOUSE_INFO="/user/liuyu/agent_custom_match/house_info"

##agent history para
export AGENT_CUSTOM_SHOWING_CONTRACT='/user/hive/warehouse/data_center.db/agent_custom_showing_contract/pt='
export AGENT_CUSTOM_SHOWING_CONTRACT_JSON='/user/liuyu/agent_custom_match/showing_contract_json'
export AGENT_CUSTOM_SHOWING_CONTRACT_JSON_MERGE='/user/liuyu/agent_custom_match/showing_contract_json_merge'
export agent_json_inner_file_name="showing_contract_json${AGENT_HISTORY_BEGAIN_DATE}_${END_DATE}"

##agent feature make param
export AGENT_FEATURE="/user/liuyu/agent_custom_match/agent_feature"

export AGENT_FEATURE_MERGE_PATH="/user/yangyekang/agent/agent_show/feature/agent_feature"
export AGENT_FEATURE_MERGE_FILENAME="agent_feature_${SAMPLE_BEGAIN_DATE}_${END_DATE}"

##agent resblock to 20 param

export AGENT_RESBLOCK_TOP_PATH="/user/liuyu/agent_custom_match/agent_resblock_top"

export AGENT_RESBLOCK_TOP_MERGE_PATH="/user/yangyekang/agent/agent_show/feature/agent_resblock_top"
export AGENT_RESBLOCK_TOP_MERGE_FILENAME="agent_resblock_top_${SAMPLE_BEGAIN_DATE}_${END_DATE}"

##market tend
export MARKET_TREND_MERGE_HADOOP_PATH="/user/yangyekang/agent/agent_show/feature/market_trend"
export market_trend_detail="market_trend_every_${CITY_CODE}_${END_DATE}"
export market_trend_merge="market_trend_merge_${SAMPLE_BEGAIN_DATE}_${END_DATE}"

###eval delegation
export EVAL_DELEGATION_FILENAME="trick_legal_delegation.txt"
export EVAL_DELEGATION_HADOOP_PATH="/user/songxin/feature"

##eval agent feature make param
export EVAL_AGENT_FEATURE="/user/liuyu/agent_custom_match/eval_agent_feature"

export EVAL_AGENT_FEATURE_MERGE_PATH="/user/yangyekang/agent/agent_show/feature/eval_agent_feature"
export EVAL_AGENT_FEATURE_MERGE_FILENAME="agent_feature_${SAMPLE_BEGAIN_DATE}_${END_DATE}"

##eval agent resblock to 20 param

export EVAL_AGENT_RESBLOCK_TOP_PATH="/user/liuyu/agent_custom_match/eval_agent_resblock_top"

export EVAL_AGENT_RESBLOCK_TOP_MERGE_PATH="/user/yangyekang/agent/agent_show/feature/eval_agent_resblock_top"
export EVAL_AGENT_RESBLOCK_TOP_MERGE_FILENAME="agent_resblock_top_${SAMPLE_BEGAIN_DATE}_${END_DATE}"
