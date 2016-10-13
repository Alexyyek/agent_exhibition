#!/bin/bash
RUN_DATE=$1

#RUN_DATE='20160731'
##test
#export GLOBAL_HADOOP_HOME="/home/work/bin/hadoop"
#export PYTHON_HDFS_PATH='/user/songxin/tools/python.tgz'
#export RUN_PATH='/home/work/liuyu/matchmaker/liuyu'
#export AGENT_HISTORY_BEGAIN_DATE="20150601"
#export END_DATE="20160731"

#export AGENT_CUSTOM_SHOWING_CONTRACT='/user/hive/warehouse/data_center.db/agent_custom_showing_contract/pt='
#export AGENT_CUSTOM_SHOWING_CONTRACT_JSON='/user/liuyu/agent_custom_match/showing_contract_json'
#export AGENT_CUSTOM_SHOWING_CONTRACT_JSON_MERGE='/user/liuyu/agent_custom_match/showing_contract_json_merge'
#export agent_json_inner_file_name="showing_contract_json${begain_date}_${end_date}"
#export INNER_PATH="${RUN_PATH}/inner_data"

begain_date=${AGENT_HISTORY_BEGAIN_DATE}
end_date=${END_DATE}


INPUT_PATH="${AGENT_CUSTOM_SHOWING_CONTRACT}${begain_date}_${end_date}/0*"
OUTPUT_PATH="${AGENT_CUSTOM_SHOWING_CONTRACT_JSON}/${begain_date}_${end_date}"

HADOOP_HOME=${GLOBAL_HADOOP_HOME}

${HADOOP_HOME}/bin/hadoop fs -rm -r ${OUTPUT_PATH}
$HADOOP_HOME/bin/hadoop  jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.4.1.jar \
    -jobconf mapred.job.name='agent_custom_agent_vector_liuyu' \
    -jobconf mapreduce.job.queuename="highPriority" \
    -jobconf mapred.job.priority=NORMAL \
    -jobconf stream.map.output.field.separator="\t" \
    -jobconf stream.num.map.output.key.fields=3 \
    -jobconf num.key.fields.for.partition=1 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -jobconf mapred.map.tasks=40 \
    -jobconf mapred.reduce.tasks=40 \
    -cacheArchive "${PYTHON_HDFS_PATH}#python" \
    -input ${INPUT_PATH} \
    -output ${OUTPUT_PATH} \
    -mapper 'cat' \
    -reducer './python/bin/python make_agent_json.py' \
    -file make_agent_json.py

if [ $? == 0 ] 
then
    echo "resblock_seg_inverse_index is success"
else
    echo "resblock_seg_inverse_index is failed"
    exit -1
fi
${HADOOP_HOME}/bin/hadoop fs -getmerge "${OUTPUT_PATH}/part*" "${INNER_PATH}/${agent_json_inner_file_name}"
if [ $? == 0 ] 
then
    echo "agent json merge is success"
else
    echo "agent json merge  is failed"
    exit -1
fi
${HADOOP_HOME}/bin/hadoop fs -rm -r ${AGENT_CUSTOM_SHOWING_CONTRACT_JSON_MERGE}/${agent_json_inner_file_name}
${HADOOP_HOME}/bin/hadoop fs -put ${INNER_PATH}/${agent_json_inner_file_name} ${AGENT_CUSTOM_SHOWING_CONTRACT_JSON_MERGE}

if [ $? == 0 ] 
then
    echo "agent json merge is put success"
    exit 0
else
    echo "agent json merge  put  failed"
    exit -1
fi
