#!/bin/bash

RUN_DAY=${RUN_DAY}
RUN_PATH=${RUN_PATH}

INPUT_DTL_PATH=${USER_DTL_INPUT_PATH}
INPUT_FAV_PATH="${USER_FAV_INPUT_PATH}/*"
OUTPUT_PATH=${USER_FEATURE_OUTPUT_PATH}

DAY_DISTANCE=${DAY_DISTANCE}
LEGAL_DELEGATION=${LEGAL_DELEGATION}
UCID_MOBILE=${UCID_MOBILE}

HADOOP_HOME=${GLOBAL_HADOOP_HOME}
PYTHON_HDFS_PATH=${PYTHON_HDFS_PATH}

${HADOOP_HOME}/bin/hadoop fs -rm -r ${OUTPUT_PATH}
$HADOOP_HOME/bin/hadoop  jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.4.1.jar \
    -D mapreduce.job.name='extract_user_online_feature_yekang' \
    -D mapreduce.job.queuename='highPriority' \
    -D mapreduce.map.memory.mb=2000 \
    -D mapreduce.reduce.memory.mb=4000 \
    -D mapredude.job.priority=NORMAL \
    -D stream.num.map.output.key.fields=1 \
    -D mapreduce.job.maps=100 \
    -D mapreduce.job.reduces=10 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -cacheArchive "${PYTHON_HDFS_PATH}#python" \
    -input ${INPUT_DTL_PATH} \
    -input ${INPUT_FAV_PATH} \
    -output ${OUTPUT_PATH} \
    -mapper './python/bin/python feature_before_del_map.py' \
    -reducer "./python/bin/python feature_before_del_reducer.py ${DAY_DISTANCE}" \
    -file ${RUN_PATH}/bin/feature_before_del_map.py \
    -file ${RUN_PATH}/bin/feature_before_del_reducer.py \
    -cacheFile ${UCID_MOBILE}#ucid_mobile \
    -cacheFile ${LEGAL_DELEGATION}#legal_delegation

echo ${RUN_DAY}
