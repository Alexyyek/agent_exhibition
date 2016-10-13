#!/bin/bash

RUN_MONTH_START=${RUN_MONTH_START}
RUN_MONTH_END=${RUN_MONTH_END}
RUN_DAY=${RUN_DAY}
city_id=${CITY_ID}

RUN_PATH=${RUN_PATH}

HADOOP_HOME=${GLOBAL_HADOOP_HOME}
PYTHON_HDFS_PATH=${PYTHON_HDFS_PATH}

while (( $RUN_MONTH_START <= $RUN_MONTH_END ))
do
    INPUT_PATH="${USER_ONLINE_PC_INPUT_PATH}/pt=${RUN_MONTH_START}*/*"
    OUTPUT_PATH="${USER_ONLINE_PC_OUTPUT_PATH}/${RUN_MONTH_START}"

    ${HADOOP_HOME}/bin/hadoop fs -rm -r ${OUTPUT_PATH}
    $HADOOP_HOME/bin/hadoop  jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.4.1.jar \
        -D mapreduce.job.name='extract_user_online_pc_yekang' \
        -D mapreduce.job.queuename='highPriority' \
        -D mapredude.job.priority=NORMAL \
        -D stream.num.map.output.key.fields=1 \
        -D num.key.fields.for.partition=1 \
        -D mapreduce.job.maps=100 \
        -D mapreduce.job.reduces=10 \
        -D mapreduce.map.memory.mb=2000 \
        -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
        -cacheArchive "${PYTHON_HDFS_PATH}#python" \
        -input ${INPUT_PATH} \
        -output ${OUTPUT_PATH} \
        -mapper "./python/bin/python extract_pc_map.py ${city_id}" \
        -reducer 'cat' \
        -file ${RUN_PATH}/bin/extract_pc_map.py

echo $RUN_MONTH_START
let "RUN_MONTH_START++"
done
