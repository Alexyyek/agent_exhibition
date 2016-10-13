#!/bin/bash
#RUN_DATE=$1

RUN_DATE='20160731'
#test
export PYTHON_HDFS_PATH='/user/songxin/tools/python.tgz'
export RUN_PATH='/home/work/liuyu/matchmaker/liuyu'
export GLOBAL_HADOOP_HOME="/home/work/bin/hadoop"
export INNER_DATA_PATH="${RUN_PATH}/inner_data"
export AGENT_HISTORY_BEGAIN_DATE="20150601"
export END_DATE="20160731"
export SAMPLE_BEGAIN_DATE="20160401"
export CITY_CODE=110000

export LEGAL_DELEGATION="/user/songxin/feature/legal_delegation.txt"
export LEGAL_DELEGATION_FILENAME="legal_delegation.txt"
export AGENT_TEAM="/user/songxin/feature/user_team.txt"
export AGENT_TEAM_FILENAME="user_team.txt"

export EVAL_DELEGATION_FILENAME="trick_legal_delegation.txt"
export EVAL_DELEGATION_HADOOP_PATH="/user/songxin/feature"

rm -rf "${INNER_DATA_PATH}/${LEGAL_DELEGATION_FILENAME}"
${HADOOP_HOME}/bin/hadoop fs -get "${LEGAL_DELEGATION}" "${INNER_DATA_PATH}"
if [ $? == 0 ] 
then
    echo "get legal_delegation is success"
else
    echo "legal_delegation  is failed"
    exit -1
fi
rm -rf "${INNER_DATA_PATH}/${AGENT_TEAM_FILENAME}"
${HADOOP_HOME}/bin/hadoop fs -get "${AGENT_TEAM}" "${INNER_DATA_PATH}"
if [ $? == 0 ] 
then
    echo "get agetn_team is success"
else
    echo "get agent_team  is failed"
    exit -1
fi


python make_eval_delegation.py "${INNER_DATA_PATH}/${LEGAL_DELEGATION_FILENAME}" "${INNER_DATA_PATH}/${AGENT_TEAM_FILENAME}" "${INNER_DATA_PATH}/${EVAL_DELEGATION_FILENAME}"


${HADOOP_HOME}/bin/hadoop fs -rm -r "${EVAL_DELEGATION_HADOOP_PATH}/${EVAL_DELEGATION_FILENAME}"
${HADOOP_HOME}/bin/hadoop fs -put "${INNER_DATA_PATH}/${EVAL_DELEGATION_FILENAME}" "${EVAL_DELEGATION_HADOOP_PATH}"

if [ $? == 0 ] 
then
    echo "agent feature merge is put success"
    exit 0
else
    echo "agent feature merge  put  failed"
    exit -1
fi
