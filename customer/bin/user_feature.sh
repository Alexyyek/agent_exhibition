#!/bin/bash

RUN_DAY=${RUN_DAY}
RUN_PATH=${RUN_PATH}

INPUT_PATH=${USER_FEATURE_INPUT_PATH}
OUTPUT_PATH=${USER_FEATURE_OUTPUT_PATH}

LEGAL_DELEGATION=${LEGAL_DELEGATION}
HOUSE_DETAIL=${HOUSE_DETAIL}
RESBLOCK_PRICE=${RESBLOCK_PRICE}

HADOOP_HOME=${GLOBAL_HADOOP_HOME}
PYTHON_HDFS_PATH=${PYTHON_HDFS_PATH}

${HADOOP_HOME}/bin/hadoop fs -rm -r ${OUTPUT_PATH}
$HADOOP_HOME/bin/hadoop  jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.4.1.jar \
    -D mapreduce.job.name='user_online_feature_yekang' \
    -D mapreduce.job.queuename='highPriority' \
    -D mapredude.job.priority=NORMAL \
    -D stream.num.map.output.key.fields=1 \
    -D num.key.fields.for.partition=1 \
    -D mapreduce.job.maps=20 \
    -D mapreduce.job.reduces=10 \
    -D mapreduce.map.memory.mb=4000 \
    -D mapreduce.reduce.memory.mb=4000 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -cacheArchive "${PYTHON_HDFS_PATH}#python" \
    -input ${INPUT_PATH} \
    -output ${OUTPUT_PATH} \
    -mapper './python/bin/python user_feature_map.py' \
    -reducer "./python/bin/python user_feature_reducer.py" \
    -file "${RUN_PATH}/bin/user_feature_map.py" \
    -file "${RUN_PATH}/bin/user_feature_reducer.py" \
    -file "${RUN_PATH}/bin/feature_common.py" \
    -cacheFile "${LEGAL_DELEGATION}#legal_delegation" \
    -cacheFile "${HOUSE_DETAIL}#house_detail" \
    -cacheFile "${RESBLOCK_PRICE}#resblock_price"

echo ${RUN_DAY}
