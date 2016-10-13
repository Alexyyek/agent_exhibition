#!/bin/bash
run_date=$1
#run_date="20160731"
#export RUN_PATH='/home/work/liuyu/matchmaker/liuyu'
#export CITY_CODE=110000
#export GLOBAL_HADOOP_HOME="/home/work/bin/hadoop"
#export HOUSE_INFO='/user/liuyu/agent_custom_match/house_info'
#export INNER_DATA_PATH="${RUN_PATH}/inner_data"
#export AGENT_HISTORY_BEGAIN_DATE="20150601"
#export END_DATE="20160731"
#export HOUSE_FILE_NAME="house_info_${CITY_CODE}_${END_DATE}"



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

house_detail=${HOUSE_FILE_NAME}


hive  -hiveconf cur_yyyy_mm_dd=${cur_yyyy_mm_dd} -hiveconf cur_yyyymmdd=${cur_yyyymmdd} -hiveconf cur_pt_yyyymmddhhnnss=${cur_pt_yyyymmddhhnnss} -hiveconf next_one_yyyy_mm_dd=${next_one_yyyy_mm_dd} -hiveconf next_one_yyyymmdd=${next_one_yyyymmdd} -hiveconf next_one_pt_yyyymmddhhnnss=${next_one_pt_yyyymmddhhnnss} -hiveconf city_code=${CITY_CODE} -hiveconf begain_date_yyyy_mm_dd=${begain_date} -hiveconf end_date_yyyy_mm_dd=${end_date} -hiveconf begain_date_yyyymmdd=${begain_date_yyyymmdd} -hiveconf begain_date_pt_yyyymmddhhnnss=${begain_date_pt_yyyymmddhhnnss} -hiveconf end_date_yyyymmdd=${end_date_yyyymmdd}  -hiveconf end_date_pt_yyyymmddhhnnss=${end_date_pt_yyyymmddhhnnss} -f ${RUN_PATH}/bin/agent_showing_contract.sql > ${INNER_DATA_PATH}/${house_detail}


${HADOOP_HOME}/bin/hadoop fs -rm  ${HOUSE_INFO}/${house_detail}
${HADOOP_HOME}/bin/hadoop fs -put ${INNER_DATA_PATH}/${house_detail} ${HOUSE_INFO}

if [ $? == 0 ] 
then
    echo "agent json merge is put success"
    exit 0
else
    echo "agent json merge  put  failed"
    exit -1
fi
