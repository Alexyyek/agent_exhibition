#!/bin/bash

RUN_DAY=${RUN_DAY}
RUN_PATH=${RUN_PATH}

PC_INPUT_PATH="${USER_BROWSE_PC_INPUT_PATH}/20160*/*"
MOBILE_INPUT_PATH="${USER_BROWSE_MOBILE_INPUT_PATH}/20160*/*"
OUTPUT_PATH=${USER_BROWSE_OUTPUT_PATH}
UUID_UCID_DICT=${UUID_UCID_DICT}

HADOOP_HOME=${GLOBAL_HADOOP_HOME}
PYTHON_HDFS_PATH=${PYTHON_HDFS_PATH}

${HADOOP_HOME}/bin/hadoop fs -rm -r ${OUTPUT_PATH}
$HADOOP_HOME/bin/hadoop  jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.4.1.jar \
    -D mapreduce.job.name='online_browse_yekang' \
    -D mapreduce.job.queuename='highPriority' \
    -D mapredude.job.priority=NORMAL \
    -D stream.num.map.output.key.fields=1 \
    -D num.key.fields.for.partition=1 \
    -D mapreduce.job.maps=100 \
    -D mapreduce.job.reduces=10 \
    -D mapreduce.map.memory.mb=2000 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -cacheArchive "${PYTHON_HDFS_PATH}#python" \
    -input ${PC_INPUT_PATH} \
    -input ${MOBILE_INPUT_PATH} \
    -output ${OUTPUT_PATH} \
    -mapper './python/bin/python uuid_2_ucid_map.py' \
    -reducer 'cat' \
    -file "${RUN_PATH}/bin/uuid_2_ucid_map.py" \
    -cacheFile ${UUID_UCID_DICT}#uuid_dict
