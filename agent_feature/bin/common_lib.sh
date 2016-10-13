#!/bin/bash
function get_time()
#获取本次运行的时间
{
    RUN_TIME=`cat $RUN_DATA_PATH"/run_time"`
}


function judge_date()
#获取本次运行的时间,如为空取运行前一天
{
    if [ ! -n "${RUN_TIME}" ]
    then
        ${RUN_TIME}=`date -d "yesterday" +%Y-%m-%d`
    else
        echo "RUN_TIME = pt, is ${RUN_TIME}"
    fi

}


function print_log()
##print log
#param is print string
{
    echo "==========================="
    echo "run log:${1}"
    echo "==========================="
}

function update_time()
{
    NEXT_TIME=`date -d ${RUN_TIME}"+1 days" +%Y-%m-%d`
}
