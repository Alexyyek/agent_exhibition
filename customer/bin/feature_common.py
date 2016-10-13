#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2014 lianjia.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: feature_common.py
Author: liuyu02(liuyu16@lianjia.com)
Date: 2016/07/30 12:47:09
Brief: feature common function
"""
import math
import optparse
import os
import shutil
import sys
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CommonFealibErr(Exception):
    """
        exception class
    """
    pass

class CommonFealib(object):
    def __init__(self):
        """
            init common feature definition
        """
        #resblock mean price
        self.meanPrice = {
                        "0": [0.0, 20000.0],
                        "1": [20000.0, 25000.0],
                        "2": [25000.0, 30000.0],
                        "3": [30000.0, 35000.0],
                        "4": [35000.0, 40000.0],
                        "5": [40000.0, 45000.0],
                        "6": [45000.0, 50000.0],
                        "7": [50000.0, 55000.0],
                        "8": [55000.0, 60000.0],
                        "9": [60000.0, 65000.0],
                        "10": [65000.0, 70000.0],
                        "11": [70000.0, 75000.0],
                        "12": [75000.0, 80000.0],
                        "13": [80000.0, 85000.0],
                        "14": [85000.0, 90000.0],
                        "15": [90000.0, 95000.0],
                        "16": [95000.0, 100000.0],
                        "17": [100000.0,  float("inf")]
                    }

        self.buildArea = {
                        "0": [0.0, 50.0],
                        "1": [50.0, 60.0],
                        "2": [60.0, 70.0],
                        "3": [70.0, 80.0],
                        "4": [80.0, 90.0],
                        "5": [90.0, 100.0],
                        "6": [100.0, 110.0],
                        "7": [110.0, 120.0],
                        "8": [120.0, 130.0],
                        "9": [130.0, 140.0],
                        "10": [140, float("inf")]
                    }
        self.buildYear = {
                        "0": [0.0, 5.0],
                        "1": [5.0, 10.0],
                        "2": [10.0, 15.0],
                        "3": [15.0, 20.0],
                        "4": [20.0, float("inf")]
                    }

        self.buildUsage = {
                         "0": "107500000001",
                         "1": "107500000003",
                         "2": "107500000004",
                         "3": "107500000005",
                         "4": "107500000006",
                         "5": "107500000007",
                         "6": "107500000008",
                         "7": "107500000009",
                         "8": "107500000010",
                         "9": "107500000012",
                         "10":"107500000013",
                         "11":"107500000014",
                         "12":"107500000015",
                         "13":"107500000011",
                         "14":"107500000016"
                     }

        self.feature_order = ["meanPrice", "buildArea", "buildYear", "buildUsage"]
        self.feature_type = {
                                 "meanPrice": "continue",
                                 "buildArea": "continue",
                                 "buildYear": "continue",
                                 "buildUsage": "discret"
                            }

        self.feature_transform = dict()
        for i in range(len(self.feature_order)):
            if i == 0:
                self.feature_transform[self.feature_order[i]] = 0
            else:
                self.feature_transform[self.feature_order[i]] = \
                    self.feature_transform[self.feature_order[i-1]] + len(eval("self." + self.feature_order[i-1]))
        self.feature_total_num = self.feature_transform[self.feature_order[-1]]+len(eval("self."+self.feature_order[-1])) - 1

        self.global_feature_order = \
                                   [\
                                    ("dtl",self.feature_total_num), \
                                    ("fav",self.feature_total_num), \
                                    ("touring",self.feature_total_num), \
                                    ("contract",self.feature_total_num), \
                                    ("agent_del_num",1), \
                                    ("cust_del_num",1), \
                                    ("agent_15_touring_num",1), \
                                    ("agent_15_touring_cust_num",1), \
                                    ("cust_15_touring_num",1), \
                                    ("cust_15_touring_agent_num",1), \
                                    ("common_resblock_cnt",1), \
                                    ("contract_cnt", 1), \
                                    ("touring_cnt", 1), \
                                    ("fav_cnt", 1), \
                                    ("dtl_cnt", 1)
                                   ]

        self.global_feature_init = dict()

        for i in range(len(self.global_feature_order)):
            if i == 0:
                self.global_feature_init[self.global_feature_order[i][0]] = 0
            else:
                self.global_feature_init[self.global_feature_order[i][0]] = \
                    self.global_feature_init[self.global_feature_order[i-1][0]] + self.global_feature_order[i-1][1]

        self.merge_global_feature_order = \
                                   [\
                                    ("cust",self.feature_total_num), \
                                    ("agent",self.feature_total_num), \
                                    ("agent_del_num",1), \
                                    ("cust_del_num",1), \
                                    ("agent_15_touring_num",1), \
                                    ("agent_15_touring_cust_num",1), \
                                    ("cust_15_touring_num",1), \
                                    ("cust_15_touring_agent_num",1), \
                                    ("common_resblock_cnt",1),\
                                    ("contract_cnt", 1), \
                                    ("touring_cnt", 1), \
                                    ("fav_cnt", 1), \
                                    ("dtl_cnt", 1)
                                   ]
        self.merge_map = {
                             "dtl":"cust", \
                             "fav":"cust", \
                             "touring":"agent",\
                             "contract":"agent"
                         }

        self.merge_global_feature_init = dict()

        for i in range(len(self.merge_global_feature_order)):
            if i == 0:
                self.merge_global_feature_init[self.merge_global_feature_order[i][0]] = 0
            else:
                self.merge_global_feature_init[self.merge_global_feature_order[i][0]] = \
                    self.merge_global_feature_init[self.merge_global_feature_order[i-1][0]] + self.merge_global_feature_order[i-1][1]

        self.continue_outlier = {
                           "meanPrice": [-float("inf"), 5000],
                           "buildArea": [-float("inf"), 10.0],
                           "buildYear": [-float("inf"), 1900.0]
                       }

        self.discret_outlier = {
                                   "buildUsage": ["-1", "0"]
                                }

        self.current_year = "2016"

    def printNoMergeFeatureDes(self, outfile):
        """
            print no merge feature  Description
        """
        file_path = os.path.dirname(outfile)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_w = open(outfile, 'w')
        all_str_tmp = ""
        for global_field in self.global_feature_order:
            if global_field[1] == 1:
                global_encode = self.globalEncoded(global_field[0],"1",0)
                all_str_tmp += "{encode}\t{desc}\tq\n".format(
                                                 encode=global_encode,
                                                 desc=global_field[0]
                                               )

            else:
                for local_field in self.feature_order:
                    feature_dict = eval("self." + local_field)
                    for i in range(len(feature_dict)):

                        if len(feature_dict[str(i)]) == 2:
                            real_desc=",".join( str(tmp_value)  for tmp_value in feature_dict[str(i)])
                        else:
                            real_desc=feature_dict[str(i)]

                        local_encoding = self.feature_transform[local_field] + i
                        gloabl_encoding = self.globalEncoded(global_field[0], local_encoding, 0)
                        all_str_tmp +=  "{encode}\t{global_field}{local_field}[{real_desc}]\tq\n".format(
                                                         encode=gloabl_encoding,
                                                         global_field=global_field[0],
                                                         local_field=local_field,
                                                         real_desc=real_desc
                                                       )
        file_w.write(all_str_tmp)
        file_w.close()

                                
    def printMergeFeatureDes(self, outfile):
        """
            print merge feature  Description
        """
        file_path = os.path.dirname(outfile)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_w = open(outfile, 'w')
        all_str_tmp = ""
        for global_field in self.global_feature_order:
            if global_field[0] == "fav" or global_field[0] ==  "contract":
                continue
            if global_field[1] == 1:
                global_encode = self.globalEncoded(global_field[0],"1",1)

                all_str_tmp += "{encode}\t{desc}\tq\n".format(
                                                 encode=global_encode,
                                                 desc=global_field[0]
                                               )
            else:
                for local_field in self.feature_order:
                    feature_dict = eval("self." + local_field)
                    for i in range(len(feature_dict)):

                        if len(feature_dict[str(i)]) == 2:
                            real_desc=",".join( str(tmp_value)  for tmp_value in feature_dict[str(i)])
                        else:
                            real_desc=feature_dict[str(i)]
                        merge_flied_type = ""
                        if global_field[0] in self.merge_map:
                            merge_flied_type = self.merge_map[global_field[0]]
                        else:
                            merge_flied_type = global_field[0]

                        local_encoding = self.feature_transform[local_field] + i
                        gloabl_encoding = self.globalEncoded(global_field[0], local_encoding, 1)
                        all_str_tmp += "{encode}\t{global_field}{local_field}[{real_desc}]\tq\n".format(
                                                         encode=gloabl_encoding,
                                                         global_field=merge_flied_type,
                                                         local_field=local_field,
                                                         real_desc=real_desc
                                                       )

        file_w.write(all_str_tmp)
        file_w.close()


    def globalEncoded(self, flied_type, local_code="noneed", is_merge=1):
        """
            is_merge=1 is dtl and fav merge to cust; touring and contract merge agent 

        """
        result_str = ""
        if is_merge == 1:
            result_str = self.globalMergeEncoded(flied_type, local_code)
        elif is_merge == 0:
            result_str = self.globalNoMergeEncoded(flied_type, local_code)
        else:
            raise CommonFealibErr("input is_merge: %s, not 1 or 0" % str(is_merge))
        return result_str


    def globalNoMergeEncoded(self, flied_type, local_code="noneed"):
        """
            feature global sort and convert uniform number
        """
        real_encode = 0
        if flied_type not in self.global_feature_init:
            raise CommonFealibErr("input flied type:[[[%s]]] not legal, legal type is:%s" \
                                  % (flied_type, json.dumps(self.global_feature_init)))
        if local_code == "noneed":
            real_encode = self.global_feature_init[flied_type] + 1
        else:
            real_encode = self.global_feature_init[flied_type] + int(local_code)

        return str(real_encode)

    def globalMergeEncoded(self, flied_type, local_code="noneed"):
        """
            feature global sort and convert uniform number
        """
        real_encode = 0

        if flied_type in self.merge_map:
            merge_flied_type = self.merge_map[flied_type]
        else:
            merge_flied_type = flied_type
        if merge_flied_type not in self.merge_global_feature_init:
            raise CommonFealibErr("input flied type:[[[%s]]] not legal, legal type is:%s" \
                                  % (merge_flied_type, json.dumps(self.merge_global_feature_init)))


        if local_code == "noneed":
            real_encode = self.merge_global_feature_init[merge_flied_type] + 1
        else:
            real_encode = self.merge_global_feature_init[merge_flied_type] + int(local_code)

        return str(real_encode)

    def dateDiff(self, date1, date2):
        """
            compute date1 and date2 diff 
        """
        year1 = date1[:4]
        year2 = date2[:4]
        year_diff = abs(int(year1) - int(year2))
        return year_diff
    
    def continueToDiscret(self, input_str, method):
        """
            input_str: continue input data
            method: "meanPrice", "buildArea", "buildYear"
        """
        rule_dict = eval("self.%s" % method)
        dealed_data = float(input_str)
        feature_key = ""
        for tmp_key in rule_dict:
            if dealed_data >= rule_dict[tmp_key][0] and dealed_data < rule_dict[tmp_key][1]:
                feature_key = tmp_key
                break
        if feature_key == "":
            raise CommonFealibErr("input:%s, not %s" %(input_str, method))
        else:
            return str(self.feature_transform[method] + int(feature_key))

    def discretTofea(self, input_str, method):
        """
            input_str: discret  input data
            method: buildUsage
        """
        rule_dict = eval("self.%s" % method)
        dealed_data = input_str
        feature_key = ""
        for tmp_key in rule_dict:
            if dealed_data == rule_dict[tmp_key]:
                feature_key = tmp_key
                break
        if feature_key == "":
            raise CommonFealibErr("input:%s, not in %s valid range" %(input_str, method))
        else:
            return str( self.feature_transform[method] + int(feature_key))

    def continueJudgeOutlier(self, input_str, method):
        """
            input_str: continue input data
            method: "meanPrice", "buildArea", "buildYear"
        """
        rule_dict = self.continue_outlier
        dealed_data = float(input_str)
        if dealed_data >= rule_dict[method][0] and dealed_data < rule_dict[method][1]:
            return False
        else:
            return True

    def discretJudgeOutlier(self, input_str, method):
        """
            input_str: discret  input data
            method: buildUsage
        """
        rule_dict = self.discret_outlier
        dealed_data = str(input_str)
        for tmp_value in rule_dict[method]:
            if dealed_data == tmp_value:
                return False
        return True

    def updateContinueFea(self, input_str, method, output_dict):
       
        """
            input_str: continue input data
            method: "meanPrice", "buildArea", "buildYear"
        """

        if self.continueJudgeOutlier(input_str, method):
            if method == "buildYear":
                real_input = self.dateDiff( self.current_year, input_str)
            else:
                real_input = input_str
            key_new = self.continueToDiscret(real_input, method)
            if key_new in output_dict:
                output_dict[key_new] += 1
            else:
                output_dict.update({key_new:1})


    def updateDiscretFea(self, input_str, method, output_dict):
        """
            input_str: discret  input data
            method: buildUsage
        """

        if self.discretJudgeOutlier(input_str, method):
            real_input = input_str
            key_new = self.discretTofea(real_input, method)
            if key_new in output_dict:
                output_dict[key_new] += 1
            else:
                output_dict.update({key_new:1})

    def updateFea(self, input_str, method, output_dict):
        """
            input_str: input value
            method: input value meaning  
            continue  method: "meanPrice", "buildArea", "buildYear"
            discret method: buildUsage
            fea_type="continue" or discret

        """
        fea_type = ""
        if method not in self.feature_type:
            raise CommonFealibErr("input method:%s, not correct method:%s" % (method, "|".join(self.feature_order)))
        fea_type = self.feature_type[method]

        if fea_type == "continue":
            self.updateContinueFea(input_str, method, output_dict)
        elif fea_type == "discret":
            self.updateDiscretFea(input_str, method, output_dict)

    
if __name__=='__main__':
    test = CommonFealib()

    test.printMergeFeatureDes("../inner_data/merge_feature_des")
    test.printNoMergeFeatureDes("../inner_data/nomerge_feature_des")
    outdict = dict()
    test.updateFea("2000", "buildYear", outdict)
    print outdict

