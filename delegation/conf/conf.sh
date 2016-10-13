#!/bin/bash
if [ $# -eq 0 ];
then
    export RUN_DAY=`date -d"-1 day" +%Y%m%d000000`
else
    export RUN_DAY="${1}000000"
fi
export CITY_ID='110000'
export BIZ_TYPE='200200000001'

#样本集legal_delegation最早开始时间
export LEGAL_DELEGATION_START_DAY='2016-04-01'
export LEGAL_DELEGATION_END_DAY='2016-07-31'
export SAMPLE_START_DAY=`date -d"${LEGAL_DELEGATION_START_DAY}" +%Y%m%d`
export SAMPLE_END_DAY=`date -d"${LEGAL_DELEGATION_END_DAY}" +%Y%m%d`

#400电话最早选取时间
#应当同${LEGAL_DELEGATION_START_DAY}保持一致或略微提前
export PHONE_CALL_START_DAY=${LEGAL_DELEGATION_START_DAY}

#计算经纪人和客户委托特征的RAW_DELEGATION文件的开始时间
#改时间应当至少早于${LEGAL_DELEGATION_START_DAY}两个月
export RAW_DELEGATION_START_DAY='2015-06-01'

#计算legal_delegation是否有七天带看的带看起始时间
#该时间应当晚于${LEGAL_DELEGATION_START_DAY}
export SHOWING_START_DAY='2016-01-01'
