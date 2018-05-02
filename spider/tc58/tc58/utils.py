# -*- coding: utf-8 -*-
# @Time    : 18/03/2018
# @Author  : Luke

import math
import os
import random

import numpy as np
import pymongo
from fake_useragent import UserAgent

MINPRICE = 2000     # 最低价格
MAXPRICE = 3500     # 最高价格
MAXDISTANCE = 7     # 距离目标地点与可选地点之间的距离之和
CITY = "上海"         # 城市
NB_ROOM = {'1室', '2室', }    # 房间数

COOKIE = None
proxies = [
    "http://localhost:1087",
    ''
]                       # 代理地址

ak = "" #百度lbs服务key，请自行申请（http://lbsyun.baidu.com/apiconsole/key）
# 若使用其他lbs服务，请同时修改pipelines中的 get_lbs 函数

# GPS， (longitude，latitude）
# primary
GPS1 = {"lat": 31.239777,
        "lng": 121.669717}  # 目标地点的gps信息
# Secondary                 # 可选地点gps信息
GPS2 = [
    # {"lat": 31.219828,
    #  "lng": 121.662625},  # 唐镇地铁站
    # {"lat": 31.216703,
    #  "lng": 121.627179},  # 广兰路地铁站
    {"lat": 31.269485,
     "lng": 121.64549},  # 金海路地铁站
    {"lat": 31.272188,
     "lng": 121.663},  # 顾唐路地铁站
    {"lat": 31.274649,
     "lng": 121.674609},  # 明雷路地铁站
    {"lat": 31.26994,
     "lng": 121.634401}  # 金吉路地铁站
]
locations = [              # 与GPS2对应的地点名
    # "唐镇地铁站",
    # "广兰路地铁站",
    "金海路地铁站",
    "顾唐路地铁站",
    "明雷路地铁站",
    "金吉路地铁站",
]


def get_collection(host, db, collection):
    client = pymongo.MongoClient(host)
    db = client[db]
    collection = db[collection]
    return collection

collection = get_collection('localhost', 'mydb', 'rent_info')       # 保存mango表信息


RADIUS = 6378.137  # km

utils_path = os.path.abspath(__file__)
utils_path = os.path.split(utils_path)[0]


def write_files(file_path, list: iter):
    length = len(list)
    with open(file_path, 'w') as f:
        for i, item in list:
            if hasattr(item, '__len__'):
                f.writelines(' '.join(item))
            else:
                f.writelines(item)
            if i < length:
                f.writelines('\n')


def random_interval():
    print('generate interval')
    return np.random.rand() * 5


ua = UserAgent(use_cache_server=False, verify_ssl=False)


def random_agent():
    headers = {'User-Agent': ua.random}
    return headers


def gps2distance(origin, destination):
    lat1, lon1 = origin['lat'], origin['lng']
    lat2, lon2 = destination['lat'], destination['lng']

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = RADIUS * c

    return d


alphabet = [chr(c) for c in range(97, 123)]


def random_string():
    length = random.randint(3, 7)
    return ''.join([random.choice(alphabet) for _ in range(length)])


def random_key_value():
    key = random_string()
    value = random_string()
    return key + '=' + value


if __name__ == '__main__':
    print(random_key_value())
