#!/bin/bash
##执行类型
source "./conf/bash_conf.sh"
source ${BIN_PATH}"/common_lib.sh"
RUN_CUR_PATH=`pwd`
############################
##get run_time
############################
#get_time
judge_date
#echo "RUN_TIME="${RUN_TIME}
###########################
##get param for stat
##########################

CUR_RUN_TIME=`date -d ${RUN_TIME} +%Y%m%d`

function main()
{
    case $1 in
        start )
            produce_agent_feature
            produce_market_feature

        ;;
        agent )
            produce_agent_feature
        ;;
        market )
            produce_market_feature
        ;;
        eval_delegation | eval_del )
            produce_eval_delegation
        ;;
        eval_agent )
            produce_eval_agent_feature
        ;;
        start_eval )
            produce_eval_delegation
            produce_eval_agent_feature
            produce_eval_market_feature
        ;;
        help | *)
            usage_of_qct
        ;;
    esac

}

function usage_of_qct()
{
echo "
        $0 start           [[ produce agent_feature; agent_top_resblock; market_trend_feature]]
        $0 agent           [[ produce agent_feature; agent_top_resblock;]]
        $0 market          [[ produce agent_top_resblock]]
        $0 eval_delegation [[ produce eval delegation]]
        $0 eval_agent      [[ produce eval_agent_feature; eval_agent_top_resblock]]
        $0 start_eval      [[ produce eval delegation; eval_agent_feature; eval_agent_top_resblock;]]
        $0 help            [[ show parameter explain]]
     "
}

function produce_agent_feature()
{
    #################################################
    #####获取获取经纪人的带看，成交，和房屋数据表，输入时间为
    #####获取数据的pt 可以和end_date 一致，考虑pt可能会缺失 和end_date 是2个变量
    ###############################################
    sh -x "${BIN_PATH}/agent_showing_contract.sh"  ${CUR_RUN_TIME}
    if [[ $? == 0 ]]
    then
        print_log "agent showing contract raw data is success !!!!"-
    else
        print_log " agent_showing_contract is faild"
        exit 1
    fi
    
    ##################################################
    ######经纪人的历史带看和成交拼成json格式
    ################################################
    sh -x "${BIN_PATH}/hadoop_agent_history.sh" ${CUR_RUN_TIME}
    if [[ $? == 0 ]]
    then
        print_log "hadoop_agent_history is success !!!!"-
    else
        print_log "hadoop_agent_history is faild"
        exit 1
    fi
    
    #################################################
    #####经纪人特征抽取：依赖经纪人历史json，house_inf, resblock_price, legal_delegation
    ###############################################
    sh -x "${BIN_PATH}/hadoop_agent_feature.sh" ${CUR_RUN_TIME}
    if [[ $? == 0 ]]
    then
        print_log "hadoop_agent_feature is success !!!!"-
    else
        print_log "hadoop_agent_feature is faild"
        exit 1
    fi
    
    ################################################
    ####经纪人top20小区：依赖经纪人历史json，house_inf, resblock_price, legal_delegation
    ##############################################
    sh -x "${BIN_PATH}/hadoop_resblock_top.sh" ${CUR_RUN_TIME}
    if [[ $? == 0 ]]
    then
        print_log "hadoop_resblock_top is success !!!!"-
    else
        print_log "hadoop_resblock_top is faild"
        exit 1
    fi
}

function produce_market_feature()
{
    #############################################################
    ####market tend feature
    #############################################################
    sh -x "${BIN_PATH}/market_trend_stat.sh" ${CUR_RUN_TIME}
    if [[ $? == 0 ]]
    then
        print_log "market_trend_stat is success !!!!"-
    else
        print_log "market_trend_stat is faild"
        exit 1
    fi
}
function produce_eval_delegation()
{
    #######################################
    ####make eval delegaiton depend on: legal_delegation.txt user_team.txt
    #####output:trick_delegaiton.txt
    ###########################################
    sh -x "${BIN_PATH}/make_eval_delegation.sh" ${CUR_RUN_TIME}
    if [[ $? == 0 ]]
    then
        print_log "make_eval_delegation is success !!!!"-
    else
        print_log "make_eval_delegation is faild"
        exit 1
    fi

}
function produce_eval_agent_feature()
{
    #######################################
    ####make eval agent feature; depend on AGENT_CUSTOM_SHOWING_CONTRACT_JSON_MERGE LEGAL_DELEGATION RESBLOCK_PRICE HOUSE_FILE_NAME
    #####output:EVAL_AGENT_FEATURE
    ###########################################
    sh -x "${BIN_PATH}/hadoop_eval_agent_feature.sh" ${CUR_RUN_TIME}
    if [[ $? == 0 ]]
    then
        print_log "hadoop_eval_agent_feature is success !!!!"-
    else
        print_log "hadoop_eval_agent_feature is faild"
        exit 1
    fi


    #######################################
    ####make eval agent top20 resblock; depend on AGENT_CUSTOM_SHOWING_CONTRACT_JSON_MERGE LEGAL_DELEGATION RESBLOCK_PRICE HOUSE_FILE_NAME
    #####output:AGENT_RESBLOCK_TOP_PATH
    ###########################################
    sh -x "${BIN_PATH}/hadoop_eval_resblock_top.sh" ${CUR_RUN_TIME}
    if [[ $? == 0 ]]
    then
        print_log "hadoop_eval_resblock_top is success !!!!"-
    else
        print_log "hadoop_eval_resblock_top is faild"
        exit 1
    fi
}

cd ${BIN_PATH}

main $*

cd ${RUN_CUR_PATH}
##############################################
##update time file
#############################################
update_time
echo "NEXT_TIME"${NEXT_TIME}
echo ${NEXT_TIME} > ${RUN_DATA_PATH}"/run_time"
rm -rf ${RUN_DATA_PATH}"/run.doing"
exit 0
