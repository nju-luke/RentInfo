# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

import pymongo
from .utils import *
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
import datetime
import requests


import re

room_pattern = re.compile('\d{1}室')

class Tc58Pipeline(object):


    def process_item(self, item, spider):
        # todo 筛选数据
        item_ = dict(item)
        item_['_id'] = item_['link']
        gps = self.get_lbs(item_)
        if gps:
            item_['room_nb'] = self.get_room_nb(item_)
            item_['distance1'] = self.distance1(gps)
            item_['distance2'] = self.distance2(gps)
            item_['status'] = self.filter(item_)
        collection.insert_one(item_)
        return item

    def get_room_nb(self,item_):
        results = room_pattern.findall(item_['title'])
        if len(results) > 0:
            return results[0]

    def filter(self, item_):
        # status: 0:未读 1:不错 4:不考虑
        if int(item_['price']) > MAXPRICE or \
            int(item_['price']) < MINPRICE or \
            item_['distance1'] + item_['distance2'] > MAXDISTANCE or \
            not self.is_match_room_nb(item_):
            return 4
        return 0

    def is_match_room_nb(self,item_):
        if item_['room_nb'] in NB_ROOM:
            return True
        return False

    def get_lbs(self, item_):
        url = 'http://api.map.baidu.com/place/v2/search?query={}' \
              '&region={}&output=json&ak={}'.format(item_['estate']+item_['address'],CITY,ak)
        url = url.replace('暂无信息','')
        response = requests.get(url)

        results = json.loads(response.text)
        if 'results' in results and len(results['results']) > 0:
            gps = results['results'][0]['location']
            return gps
        return None

    def distance1(self,gps):
        # 返回目标地点的距离
        return gps2distance(gps, GPS1)

    def distance2(self,gps):
        # 返回其余地点中最近地点名称及距离
        distances = []
        for gps2 in GPS2:
            distances.append(gps2distance(gps, gps2))
        indices = np.argsort(distances)
        return distances[indices[0]]
        # return [locations[indices[0]],distances[indices[0]]]



class MyTakeFirst():
    def __call__(self, values):
        for value in values:
            if value is not None and value != '':
                return value.strip()

class ToDate():
    def get_number(self,value):
        try:
            return float(value[:2])
        except ValueError:
            return float(value[0])

    def __call__(self,values):
        value = values[0].strip()
        if '小时前' in value:
            number = self.get_number(value)
            act_time = datetime.datetime.now() - datetime.timedelta(hours=float(number))
            return act_time.strftime('%m-%d:%H')
        if '分钟前' in value:
            number = self.get_number(value)
            act_time = datetime.datetime.now() - datetime.timedelta(minutes=float(number))
            return act_time.strftime('%m-%d:%H')
        if '1天前' in value:
            act_time = datetime.datetime.now() - datetime.timedelta(days=1)
            return act_time.strftime('%m-%d')
        if '2天前' in value:
            act_time = datetime.datetime.now() - datetime.timedelta(days=2)
            return act_time.strftime('%m-%d')
        return value


class Tc58ItemLoader(ItemLoader):
    # 对筛选出的item进行处理
    default_output_processor = MyTakeFirst()
    date_out = ToDate()



