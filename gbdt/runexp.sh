#!/bin/bash
# map feature using indicator encoding, also produce featmap.txt

# training and output the models
./xgboost matchmaker.conf
# output prediction task=pred
./xgboost matchmaker.conf task=pred model_in=0050.model
python eval.py
# print the boosters of 0050.model in dump.raw.txt
./xgboost matchmaker.conf task=dump model_in=0050.model name_dump=dump.raw.txt
# use the feature map in printing for better visualization
#./xgboost matchmaker.conf task=dump model_in=0050.model fmap=featmap_merge.txt name_dump=dump.nice.txt
