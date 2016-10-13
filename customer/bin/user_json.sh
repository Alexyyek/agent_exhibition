#!/bin/bash

RUN_DAY=${RUN_DAY}
RUN_PATH=${RUN_PATH}

START_DATE=${START_DATE}
END_DATE=${END_DATE}

INPUT_BROWSE_PATH=${USER_BROWSE_INPUT_PATH}
INPUT_FAV_PATH="${USER_FAV_INPUT_PATH}/*"
OUTPUT_PATH=${USER_ONLINE_OUTPUT_PATH}

UCID_MOBILE=${UCID_MOBILE}
SPIDER=${SPIDER}

HADOOP_HOME=${GLOBAL_HADOOP_HOME}
PYTHON_HDFS_PATH=${PYTHON_HDFS_PATH}

${HADOOP_HOME}/bin/hadoop fs -rm -r ${OUTPUT_PATH}
$HADOOP_HOME/bin/hadoop  jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.4.1.jar \
    -D mapreduce.job.name='extract_user_online_yekang' \
    -D mapreduce.job.queuename='highPriority' \
    -D mapreduce.map.memory.mb=4000 \
    -D mapreduce.reduce.memory.mb=8000 \
    -D mapredude.job.priority=NORMAL \
    -D num.key.fields.for.partition=1 \
    -D stream.num.map.output.key.fields=1 \
    -D mapreduce.job.maps=50 \
    -D mapreduce.job.reduces=10 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -cacheArchive "${PYTHON_HDFS_PATH}#python" \
    -input ${INPUT_BROWSE_PATH} \
    -input ${INPUT_FAV_PATH} \
    -output ${OUTPUT_PATH} \
    -mapper "./python/bin/python user_json_map.py ${START_DATE} ${END_DATE}" \
    -reducer "./python/bin/python user_json_reducer.py" \
    -file "${RUN_PATH}/bin/user_json_map.py" \
    -file "${RUN_PATH}/bin/user_json_reducer.py" \
    -cacheFile ${UCID_MOBILE}#ucid_mobile \
    -cacheFile ${SPIDER}#spider

echo ${RUN_DAY}
