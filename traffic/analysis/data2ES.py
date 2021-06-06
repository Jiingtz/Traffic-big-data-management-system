# -*- coding: utf-8 -*-
# @Time    : 2021/6/4 11:15
# @Author  : TongJing Zeng
# @Email   : 1529302504@qq.com
# @File    : data2ES.py

from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json

es = Elasticsearch(["localhost:6302"])

# 获取json数据
def get_data(filepath):
    with open(filepath, "r", encoding='utf-8') as f:
        data = json.load(f)
        # print(data)
    return data


# 数据导入elasticsearch
def insert2ES(items, idx, d_type):
    # 创建索引，忽略400错误（索引已存在）
    # create_idx = es.indices.create(index=idx, ignore=400)
    # print(create_idx)

    # # 批量快速写入
    action = [{
        "_index": idx,
        "_type": d_type,
        "_source": item,
        "_id": i,
    } for i, item in enumerate(items)]
    helpers.bulk(es, action)


# 随机抽取某一天的json数据
path = "./street"
originData = get_data(path)
data_list = []
for d in originData.items():
    data = {'road_name': d[0], 'way': d[1]}
    data_list.append(data)
    # print(list(d))

print(data_list[0])
insert2ES(data_list, 'road', '_doc')
