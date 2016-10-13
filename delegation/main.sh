#!/bin/bash
source conf/conf.sh

function get_raw_delegation
{
    SQL="select cust_pkid, phone_a, phone_b, phone_c, created_code, created_time, holder_code, holder_time, invalid_time from data_center.dim_merge_custdel_day where pt='${RUN_DAY}' and city_id='${CITY_ID}' and created_time>='${LEGAL_DELEGATION_START_DAY}';"
    hive -e "${SQL}"
}

function get_agent_info
{
    SQL="select uc_id, user_code, user_name, status, huji_address, mobile from dw.dw_uc_agent_info_da where pt='${RUN_DAY}' and (dp in ('4','5','6'));"
    hive -e "${SQL}"
}

function get_phone_log
{
    SQL="select b.agent_ucid, b.agent_code, b.agent_name, a.main_number, a.ext_number, a.caller_number, a.callee_number, a.start_time from stg.stg_lianjia_agent_phone_log_da a, stg.stg_lianjia_agent_phone_da b where a.pt='${RUN_DAY}' and b.pt='${RUN_DAY}' and a.start_time>='${PHONE_CALL_START_DAY}' and a.main_number = b.virtual_main_number and a.ext_number = b.virtual_ext_number;"
    hive -e "${SQL}"
}

function get_delegation
{
    SQL="select cust_pkid, phone_a, phone_b, phone_c, created_code, city_id, created_time from data_center.dim_merge_custdel_day where pt='${RUN_DAY}' and city_id='${CITY_ID}' and biz_type='${BIZ_TYPE}' and created_time>='${LEGAL_DELEGATION_START_DAY}';"
    hive -e "${SQL}"
}

function get_showing
{
    SQL="select cust_pkid, showing_broker_code, showing_begin_time from data_center.dim_merge_showing_day where pt='${RUN_DAY}' and city_id='${CITY_ID}' and biz_type='${BIZ_TYPE}' and showing_begin_time >= '${SHOWING_START_DAY}';"
    hive -e "${SQL}"
}


function get_feature
{
    get_raw_delegation > inner_data/raw_delegation.txt

    cat inner_data/raw_delegation.txt | python bin/get_cust_phone.py | sort -k1,1 > inner_data/phone_cust.txt

    cat inner_data/raw_delegation.txt | python bin/cust_del_list.py > inner_data/cust_del_list.txt
    cat inner_data/raw_delegation.txt | python bin/agent_del_list.py > inner_data/agent_del_list.txt
    cat inner_data/touring.txt | python bin/cust_touring_list.py > inner_data/cust_touring_list.txt
    cat inner_data/touring.txt | python bin/agent_touring_list.py > inner_data/agent_touring_list.txt

    cat data/legal_delegation.txt | python bin/cust_feature.py | sort -k2,2 > data/cust_feature.txt
    cat data/legal_delegation.txt | python bin/agent_feature.py | sort -k2,2 > data/agent_feature.txt
}

function get_legal_delegation
{
    get_agent_info > inner_data/agent_info.txt
    get_phone_log > inner_data/phone_log.txt
    get_delegation > inner_data/delegation.txt
    get_showing > inner_data/touring.txt
    cat inner_data/delegation.txt | python bin/delegation_filter.py | awk -F"\t" -vOFS="\t" '$3>="'${SAMPLE_START_DAY}'" && $3<="'${SAMPLE_END_DAY}'"' | sort -k3,3 -k1,1 -k2,2 > data/legal_delegation.txt
}

function usage
{
    echo "
            $0 start            [[ get legal_delegation; get agent_feature; get cust_feature ]]
            $0 legal_delegation [[ get legal_delegation ]]
            $0 feature          [[ get agent_feature; get cust_feature ]]
        "
}

function main
{
    case $1 in
        start )
            get_legal_delegation
            get_feature
            ;;
        legal_delegation )
            get_legal_delegation
            ;;
        feature )
            echo "Make Sure You Have Got data/legalt_delegation.txt!"
            get_feature
            ;;
        help | *)
            usage
            ;;
    esac
}

main $*
