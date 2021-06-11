# coding=utf-8
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from elasticsearch import Elasticsearch
import pymysql

param = {
    'host': '127.0.0.1',
    'db': 'baidumap',
    'charset': 'utf8',
    'user': 'root',
    'password': 'ztj19991124',
    'port': 3306,
}
conn = pymysql.Connect(**param)
cursor = conn.cursor()

es = Elasticsearch(["127.0.0.1:6302"])
indexName = "road"


# 主页面
def index(request):
    return render(request, 'index.html')


# 地图页面
def Map(request):
    try:
        road_name = request.POST.get('searchRoad')
        query = es.search(body={
            "query": {
                "term": {
                    "road_name.keyword": {
                        "value": road_name,
                    }
                }
            }
        }, index=indexName, scroll='5m', size=1)
        originList = query["hits"]["hits"]
        road_path = originList[0]['_source']['way']
        return JsonResponse({'road_path': road_path}, safe=False)
    except:
        return render(request, 'Map.html')


# 搜索联想
def associate(request):
    searchData = request.POST.get('searchData')
    data = []
    try:
        query = es.search(body={
            "query": {
                "fuzzy": {
                    "road_name": {
                        "value": searchData,
                    }
                }
            }
        }, index=indexName, scroll='5m', size=10)
        originList = query["hits"]["hits"]
        data = []
        for d in originList:
            data.append(d['_source']['road_name'])
    except:
        print('正在联想！')
    # print(data)
    return JsonResponse({'association': data}, safe=False)


# 路线规划
def pathPlanning(request):
    try:
        pathList = eval(request.POST.get('pathList'))
        nodes = []
        for path in pathList:
            # print(path['path'])
            for node in path['path']:
                if [node['lng'], node['lat']] not in nodes:
                    nodes.append([node['lng'], node['lat']])
        print(nodes)
        return JsonResponse({'nodes': nodes}, safe=False)
    except:
        return render(request, 'Map.html')