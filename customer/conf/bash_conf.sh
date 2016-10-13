export RUN_PATH="/home/work/yangyekang/agent/agent_exhibition"

export BIN_PATH=${RUN_PATH}"/bin"
export DATA_PATH=${RUN_PATH}"/data"
export GLOBAL_HADOOP_HOME="/home/work/bin/hadoop"
export PYTHON_HDFS_PATH='/user/songxin/tools/python.tgz'
export RUN_DAY=`date +%Y%m%d`
export RUN_LAST_DAY=`date -d -1"days" +%Y%m%d`

##pc & mobile
export RUN_MONTH_START=201603
export RUN_MONTH_END=201607
export CITY_ID=110000
export USER_ONLINE_PC_INPUT_PATH="/user/hive/warehouse/log_center.db/log_dw_details_pc_hour"
export USER_ONLINE_PC_OUTPUT_PATH="/user/yangyekang/online_data/pc"
export USER_ONLINE_MOBILE_INPUT_PATH="/user/hive/warehouse/log_center.db/log_dw_details_event_mobile_hour/pt=${RUN_MONTH_START}*/*"
export USER_ONLINE_MOBILE_OUTPT_PATH="/user/yangyekang/online_data/mobile/${RUN_MONTH_START}"

##uuid2ucid
export USER_BROWSE_PC_INPUT_PATH="/user/yangyekang/online_data/pc"
export USER_BROWSE_MOBILE_INPUT_PATH="/user/yangyekang/online_data/mobile"
export USER_BROWSE_OUTPUT_PATH="/user/yangyekang/online_data/online_ucid"

##user json
export USER_BROWSE_INPUT_PATH="/user/yangyekang/online_data/online_ucid"
export USER_FAV_INPUT_PATH="/user/yangyekang/online_data/fav"
export USER_ONLINE_OUTPUT_PATH="/user/yangyekang/online_data/user_online"

##user feature
export USER_FEATURE_INPUT_PATH="/user/yangyekang/online_data/user_online/"
export USER_FEATURE_OUTPUT_PATH="/user/yangyekang/agent/agent_show/feature/user_feature"

##user resblock top
export TOPN=20
export DTL_SCORE=1
export FAV_SCORE=5
export USER_RESBLOCK_INPUT_PATH="/user/yangyekang/online_data/user_online/"
export USER_RESBLOCK_OUTPUT_PATH="/user/yangyekang/agent/agent_show/feature/user_resblock_top"

##user dtl & fav feature before delegation
export DAY_DISTANCE=15
export USER_DTL_INPUT_PATH="/user/yangyekang/online_data/online_ucid"
export USER_FAV_INPUT_PATH="/user/yangyekang/online_data/fav/"
export USER_OUTPUT_PATH="/user/yangyekang/agent/agent_show/feature/user_online_feature"

##third part data
export START_DATE='2016-04-01'
export END_DATE='2016-07-31'
export LEGAL_DELEGATION="/user/songxin/feature/legal_delegation.txt"
export UUID_UCID_DICT="/user/yangyekang/online_data/tools/ucid_uuid_20160731"
export UCID_MOBILE="/user/songxin/tools/ucid_mobile/${RUN_LAST_DAY}.txt"
export HOUSE_DETAIL="/user/yangyekang/agent/tools/dim_merge_house_day_aug"
export RESBLOCK_PRICE="/user/songxin/feature/resblock_price.txt"
export SPIDER="/user/songxin/feature/spider.txt"
