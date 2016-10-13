#!/bin/bash
run_date=$1

#run_date="20160731"
#export RUN_PATH='/home/work/liuyu/matchmaker/liuyu'
#export CITY_CODE=110000
#export END_DATE="20160731"
#export SAMPLE_BEGAIN_DATE="20160401"
#export MARKET_TREND_BEGAIN_DATE="20160301"
#export GLOBAL_HADOOP_HOME="/home/work/bin/hadoop"
#export INNER_DATA_PATH="${RUN_PATH}/inner_data"
#export MARKET_TREND_MERGE_HADOOP_PATH="/user/yangyekang/agent/agent_show/feature/market_trend"
#export market_trend_detail="market_trend_every_${CITY_CODE}_${END_DATE}"
#export market_trend_merge="market_trend_merge_${SAMPLE_BEGAIN_DATE}_${END_DATE}"

BEGAIN_DATE=${MARKET_TREND_BEGAIN_DATE}
TOPT=`date -d ${run_date} +%Y-%m-%d`
begain_date=`date -d ${BEGAIN_DATE} +%Y-%m-%d`
end_date=`date -d ${END_DATE} +%Y-%m-%d`

##########################
last_one_date=`date -d ${TOPT}"-1 days" +%Y-%m-%d`
last_one_OUTPT=`date -d ${last_one_date} +%Y%m%d`
last_one_pt=${last_one_OUTPT}'000000'

cur_yyyy_mm_dd=${TOPT}
cur_yyyymmdd=`date -d ${TOPT} +%Y%m%d`
cur_pt_yyyymmddhhnnss=${cur_yyyymmdd}'000000'
next_one_yyyy_mm_dd=`date -d ${TOPT}"+1 days" +%Y-%m-%d`
next_one_yyyymmdd=`date -d ${next_one_yyyy_mm_dd} +%Y%m%d` 
next_one_pt_yyyymmddhhnnss=${next_one_yyyymmdd}'000000'

begain_date_yyyymmdd=`date -d ${begain_date} +%Y%m%d`
begain_date_pt_yyyymmddhhnnss=${begain_date_yyyymmdd}'000000'

end_date_yyyymmdd=`date -d ${end_date} +%Y%m%d`
end_date_pt_yyyymmddhhnnss=${end_date}'000000'



hive  -hiveconf cur_yyyy_mm_dd=${cur_yyyy_mm_dd} -hiveconf cur_yyyymmdd=${cur_yyyymmdd} -hiveconf cur_pt_yyyymmddhhnnss=${cur_pt_yyyymmddhhnnss} -hiveconf next_one_yyyy_mm_dd=${next_one_yyyy_mm_dd} -hiveconf next_one_yyyymmdd=${next_one_yyyymmdd} -hiveconf next_one_pt_yyyymmddhhnnss=${next_one_pt_yyyymmddhhnnss} -hiveconf city_code=${CITY_CODE} -hiveconf begain_date_yyyy_mm_dd=${begain_date} -hiveconf end_date_yyyy_mm_dd=${end_date} -hiveconf begain_date_yyyymmdd=${begain_date_yyyymmdd} -hiveconf begain_date_pt_yyyymmddhhnnss=${begain_date_pt_yyyymmddhhnnss} -hiveconf end_date_yyyymmdd=${end_date_yyyymmdd}  -hiveconf end_date_pt_yyyymmddhhnnss=${end_date_pt_yyyymmddhhnnss} -f ${RUN_PATH}/bin/market_trend_stat.sql > ${INNER_DATA_PATH}/${market_trend_detail}

if [ $? == 0 ] 
then
    echo "market_trend_stat  is success"
else
    echo "market_trend_stat  failed"
    exit -1
fi
python market_trend_join.py "${INNER_DATA_PATH}/${market_trend_detail}" "${INNER_DATA_PATH}/${market_trend_merge}"

if [ $? == 0 ] 
then
    echo "market_trend_merge  is success"
else
    echo "market_trend_merge  failed"
    exit -1
fi
${HADOOP_HOME}/bin/hadoop fs -rm -r  ${MARKET_TREND_MERGE_HADOOP_PATH}/${market_trend_merge}
${HADOOP_HOME}/bin/hadoop fs -put "${INNER_DATA_PATH}/${market_trend_merge}" "${MARKET_TREND_MERGE_HADOOP_PATH}"


if [ $? == 0 ] 
then
    echo "market_trend_merge is put success"
    exit 0
else
    echo "market_trend_merge put  failed"
    exit -1
fi
