#!/bin/bash
source conf/conf.sh

function get_raw_delegation
{
    SQL="select cust_pkid, phone_a, phone_b, phone_c, created_code, created_time, holder_code, holder_time, invalid_time from data_center.dim_merge_custdel_day where pt='${RUN_DAY}' and city_id='${CITY_ID}' and created_time>='${LEGAL_DELEGATION_START_DAY}';"
    hive -e "${SQL}"
}

get_raw_delegation > data/raw_delegation.txt

cat data/raw_delegation.txt | python bin/get_cust_phone.py | sort -k1,1 > data/phone_cust.txt

cat data/raw_delegation.txt | python bin/cust_del_list.py > data/cust_del_list.txt
cat data/raw_delegation.txt | python bin/agent_del_list.py > data/agent_del_list.txt
cat data/touring.txt | python bin/cust_touring_list.py > data/cust_touring_list.txt
cat data/touring.txt | python bin/agent_touring_list.py > data/agent_touring_list.txt

cat data/legal_delegation.txt | python bin/cust_feature.py | sort -k2,2 > data/cust_feature.txt
cat data/legal_delegation.txt | python bin/agent_feature.py | sort -k2,2 > data/agent_feature.txt
