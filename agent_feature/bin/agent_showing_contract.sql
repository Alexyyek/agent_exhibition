-- =========================================================================
-- **创建人: 刘宇 liuyu02@lianjia.com 18601300804
-- **创建时间: 2016-07-22
-- **代码描述:经纪人展位经纪人画像
-- **涉及需求：
-- ** 
-- ** 
-- **维护人: 刘宇 liuyu02@lianjia.com 18601300804
-- **修改历史:
-- **    
-- **    
-- **    
-- **    
-- ===================META BEGIN=============================================
-- **依赖表列表:  
-- ** 
-- **-data_center.dim_merge_house_day
-- **-data_center.dim_merge_contract_day 合同表 （全量表）
-- **data_center.dim_merge_showing_house_day
-- **data_center.dim_merge_showing_day
-- ** 
-- **MID TABLE :
-- ** 
-- **OUTPU TTABLE: 
--变量
--cur_yyyy_mm_dd:2016-04-30
--cur_pt_yyyymmddhhnnss:201604300000
--cur_yyyymmdd:20160430
--next_one_yyyy_mm_dd:2016-05-01
--next_one_pt_yyyymmddhhnnss:2016-05-01
--city_code:${hiveconf:city_code}
--begain_date_yyyy_mm_dd:${hiveconf:begain_date_yyyy_mm_dd}
--end_date_yyyy_mm_dd:${hiveconf:end_date_yyyy_mm_dd}
--begain_date_yyyymmdd=`date -d ${begain_date} +%Y%m%d`
--begain_date_pt_yyyymmddhhnnss=${begain_date_yyyymmdd}'000000'
--
--end_date_yyyymmdd=`date -d ${end_date} +%Y%m%d`
--end_date_pt_yyyymmddhhnnss=${end_date}'000000'
-- 

--drop table if exists data_center.agent_custom_showing_contract;


create table if not exists data_center.agent_custom_showing_contract
(
    broker_code    string  comment "经纪人系统号"   
    ,flag          string  comment "业务类型touring contract"
    ,action_date   string  comment "业务发生时间"
    ,cust_pkid     string  comment "客源id"
    ,house_pkid    string  comment "房屋id"
    ,hdic_house_id bigint  comment "楼盘字典id"
) comment "经纪人带看成交表" 
partitioned by (pt string comment "日期" ) 
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n'
STORED AS TEXTFILE
;

DROP table if exists tmp.agent_custom_showing_detail_${hiveconf:begain_date_yyyymmdd}_${hiveconf:end_date_yyyymmdd};
CREATE TABLE tmp.agent_custom_showing_detail_${hiveconf:begain_date_yyyymmdd}_${hiveconf:end_date_yyyymmdd} AS
select 
    showing_broker_code as broker_code
    ,"touring" as flag
    ,show_date as action_date
    ,cust_pkid
    ,house_pkid
    ,hdic_house_id
from
(
    select
        ta.showing_broker_code
        ,ta.cust_pkid
        ,tb.showing_id
        ,tb.house_pkid
        ,tb.hdic_house_id
        ,substr(tb.created_time, 1, 10) as show_date
    from
    (
        select
            id
           ,cust_pkid
           ,showing_uid
           ,showing_broker_code
           ,city_id
        from data_center.dim_merge_showing_day
        where
            pt = '${hiveconf:cur_pt_yyyymmddhhnnss}'
            and city_id = '${hiveconf:city_code}'
    )ta 
    inner join
    (
        select
            id
            ,showing_id
            ,house_pkid
            ,hdic_house_id
            ,created_time
            ,city_id
        from data_center.dim_merge_showing_house_day
        where
            pt = '${hiveconf:cur_pt_yyyymmddhhnnss}'
            and substr(created_time, 1, 10) >= '${hiveconf:begain_date_yyyy_mm_dd}'
            and substr(created_time, 1, 10) <= '${hiveconf:end_date_yyyy_mm_dd}'
    )tb on ta.id = tb.showing_id 
           and ta.city_id = tb.city_id
    inner join
    (
        select
            house_pkid
            ,hdic_house_id
            ,district_code
            ,district_name
            ,bizcircle_code
            ,bizcircle_name
            ,resblock_id
            ,resblock_name
            ,city_id
        from data_center.dim_merge_house_day
        where
            pt = '${hiveconf:cur_pt_yyyymmddhhnnss}'
            and biz_type = '200200000001'
    )tc on substr(tb.house_pkid, -8) = substr(tc.house_pkid, -8)
           and tb.city_id = tc.city_id
           and tb.hdic_house_id = tc.hdic_house_id
)tall
group by showing_broker_code, house_pkid, cust_pkid, hdic_house_id, show_date
;


DROP table if exists tmp.agent_custom_contract_detail_${hiveconf:begain_date_yyyymmdd}_${hiveconf:end_date_yyyymmdd};
CREATE TABLE tmp.agent_custom_contract_detail_${hiveconf:begain_date_yyyymmdd}_${hiveconf:end_date_yyyymmdd} AS
select
    created_code as broker_code
    ,"contract" as flag
    ,contract_date as action_date
    ,new_cust_pkid as cust_pkid
    ,house_pkid
    ,hdic_house_id
from
(

    select
        ta.created_code
        ,ta.contract_date
        ,ta.new_cust_pkid
        ,ta.cust_pkid
        ,ta.hdic_house_id
        ,tb.house_pkid
    from
    (
        select
             created_code
            ,substr(created_time, 1, 10) as contract_date
            ,cott_pkid
            ,case length(cust_pkid)
                 when 10 then concat('5010', substr(cust_pkid, -8))
                 when 11 then concat('501', substr(cust_pkid, -9))
                 when 12 then concat('50', substr(cust_pkid, -10))
                 else null end as new_cust_pkid

            ,cust_pkid
            ,house_pkid
            ,hdic_house_id
            ,city_id
    
         from data_center.dim_merge_contract_day
         where
             pt = '${hiveconf:cur_pt_yyyymmddhhnnss}'
             and biz_type=200200000001
             and state!='200800000005'
             and state!='200800000006'
             and city_id='${hiveconf:city_code}'
             and substr(created_time, 1, 10) >= '${hiveconf:begain_date_yyyy_mm_dd}'
             and substr(created_time, 1, 10) <= '${hiveconf:end_date_yyyy_mm_dd}'
    )ta
    inner join
    (
        select
            house_pkid
            ,hdic_house_id
            ,district_code
            ,district_name
            ,bizcircle_code
            ,bizcircle_name
            ,resblock_id
            ,resblock_name
            ,city_id
        from data_center.dim_merge_house_day
        where
            pt = '${hiveconf:cur_pt_yyyymmddhhnnss}'
            and biz_type = '200200000001'
    )tb on substr(ta.house_pkid, -8) = substr(tb.house_pkid, -8)
           and ta.city_id = tb.city_id
           and ta.hdic_house_id = tb.hdic_house_id

)tall 
group by created_code, cust_pkid, new_cust_pkid, house_pkid, hdic_house_id, contract_date
;

insert overwrite table data_center.agent_custom_showing_contract partition(pt='${hiveconf:begain_date_yyyymmdd}_${hiveconf:end_date_yyyymmdd}')
--计算今天
select 
    * 
from 
    tmp.agent_custom_showing_detail_${hiveconf:begain_date_yyyymmdd}_${hiveconf:end_date_yyyymmdd}
union
select 
    * 
from 
    tmp.agent_custom_contract_detail_${hiveconf:begain_date_yyyymmdd}_${hiveconf:end_date_yyyymmdd}
;

select
    house_pkid
    ,hdic_house_id
    ,resblock_id
    ,resblock_name
    ,nvl(build_end_year, '0')
    ,nvl(build_area, 0)
    ,nvl(house_usage_code, '-1')
    ,city_id
from data_center.dim_merge_house_day
where
    pt = '${hiveconf:cur_pt_yyyymmddhhnnss}'
    and biz_type = '200200000001'
    and city_id='${hiveconf:city_code}'
;
--DROP table if exists tmp.agent_custom_showing_detail_${hiveconf:begain_date_yyyymmdd}_${hiveconf:end_date_yyyymmdd};
--DROP table if exists tmp.agent_custom_contract_detail_${hiveconf:begain_date_yyyymmdd}_${hiveconf:end_date_yyyymmdd};
