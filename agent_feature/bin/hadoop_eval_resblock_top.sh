#!/bin/bash

RUN_DATE=$1

#RUN_DATE='20160731'
##test
#export PYTHON_HDFS_PATH='/user/songxin/tools/python.tgz'
#export RUN_PATH='/home/work/liuyu/matchmaker/agent_feature'
#export GLOBAL_HADOOP_HOME="/home/work/bin/hadoop"
#export INNER_DATA_PATH="${RUN_PATH}/inner_data"
#export AGENT_HISTORY_BEGAIN_DATE="20150601"
#export END_DATE="20160731"
#export SAMPLE_BEGAIN_DATE="20160401"
#export CITY_CODE=110000
#
#export AGENT_CUSTOM_SHOWING_CONTRACT_JSON_MERGE='/user/liuyu/agent_custom_match/showing_contract_json_merge'
#export agent_json_inner_file_name="showing_contract_json${AGENT_HISTORY_BEGAIN_DATE}_${END_DATE}"
#
#export LEGAL_DELEGATION="/user/songxin/feature/legal_delegation.txt"
#export RESBLOCK_PRICE="/user/songxin/feature/resblock_price.txt"
#
#export HOUSE_FILE_NAME="house_info_${CITY_CODE}_${END_DATE}"
#export HOUSE_INFO="/user/liuyu/agent_custom_match/house_info"
#export EVAL_DELEGATION_FILENAME="trick_legal_delegation.txt"
#export EVAL_DELEGATION_HADOOP_PATH="/user/songxin/feature"
#
#export EVAL_AGENT_RESBLOCK_TOP_PATH="/user/liuyu/agent_custom_match/eval_agent_resblock_top"
#
#export EVAL_AGENT_RESBLOCK_TOP_MERGE_PATH="/user/yangyekang/agent/agent_show/feature/eval_agent_resblock_top"
#export EVAL_AGENT_RESBLOCK_TOP_MERGE_FILENAME="agent_resblock_top_${SAMPLE_BEGAIN_DATE}_${END_DATE}"
#export TOURING_WEIGHT="1"
#export CONTRACT_WEIGHT="20"


end_date=${END_DATE}
begain_date=${SAMPLE_BEGAIN_DATE}

INPUT_PATH="${EVAL_DELEGATION_HADOOP_PATH}/${EVAL_DELEGATION_FILENAME}"

OUTPUT_PATH="${AGENT_RESBLOCK_TOP_PATH}/${begain_date}_${end_date}"

HADOOP_HOME=${GLOBAL_HADOOP_HOME}


${HADOOP_HOME}/bin/hadoop fs -rm -r ${OUTPUT_PATH}
$HADOOP_HOME/bin/hadoop  jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.4.1.jar \
    -jobconf mapred.job.name='eval_resblok_top_liuyu' \
    -jobconf mapreduce.job.queuename="highPriority" \
    -jobconf mapred.job.priority=NORMAL \
    -jobconf stream.map.output.field.separator="\t" \
    -jobconf stream.num.map.output.key.fields=2 \
    -jobconf num.key.fields.for.partition=1 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -jobconf mapred.map.tasks=100 \
    -jobconf mapred.reduce.tasks=71 \
    -jobconf mapreduce.reduce.memory.mb=16384 \
    -cacheArchive "${PYTHON_HDFS_PATH}#python" \
    -input ${INPUT_PATH} \
    -output ${OUTPUT_PATH} \
    -file "${RUN_PATH}/bin/agent_top_resblock.py"  \
    -cacheFile ${AGENT_CUSTOM_SHOWING_CONTRACT_JSON_MERGE}/${agent_json_inner_file_name}#agent_json \
    -cacheFile ${HOUSE_INFO}/${HOUSE_FILE_NAME}#house_detail \
    -cacheFile ${RESBLOCK_PRICE}#resblock_meanprice \
    -mapper "./python/bin/python agent_top_resblock.py mapper " \
    -reducer "./python/bin/python agent_top_resblock.py reducer ${TOURING_WEIGHT} ${CONTRACT_WEIGHT}"


if [ $? == 0 ] 
then
    echo "resblock_seg_inverse_index is success"
else
    echo "resblock_seg_inverse_index is failed"
    exit -1
fi

${HADOOP_HOME}/bin/hadoop fs -getmerge "${OUTPUT_PATH}/part*" "${INNER_DATA_PATH}/${EVAL_AGENT_RESBLOCK_TOP_MERGE_FILENAME}"
if [ $? == 0 ] 
then
    echo "agent feature merge is success"
else
    echo "agent feature merge  is failed"
    exit -1
fi
${HADOOP_HOME}/bin/hadoop fs -rm -r ${EVAL_AGENT_RESBLOCK_TOP_MERGE_PATH}/${EVAL_AGENT_RESBLOCK_TOP_MERGE_FILENAME}
${HADOOP_HOME}/bin/hadoop fs -put ${INNER_DATA_PATH}/${EVAL_AGENT_RESBLOCK_TOP_MERGE_FILENAME} ${EVAL_AGENT_RESBLOCK_TOP_MERGE_PATH}

if [ $? == 0 ] 
then
    echo "agent feature merge is put success"
    exit 0
else
    echo "agent feature merge  put  failed"
    exit -1
fi
