# -*- coding: utf-8 -*-
# @Time    : 18/03/2018
# @Author  : Luke

import scrapy
from scrapy import Request

from ..items import Tc58Item
from ..pipelines import Tc58ItemLoader
from ..utils import *

region_path = os.path.join(utils_path, 'data', 'regions')


class tc58Spider(scrapy.Spider):
    name = 'tc58'
    allowed_domains = ["58.com"]
    regions = []
    start_urls = ['http://sh.58.com/pudongxinqu/zufang/0/?PGTID=0d30000a-0058-3ec1-098b-aaf98ffdfa19&ClickID=2']

    def load_regions(self):
        # 加载区域
        with open(region_path, 'r') as f:
            for line in f.readlines():
                self.regions.append(line.split(' ')[0])

    def start_requests(self):
        # 生成区域urls
        self.load_regions()
        random.shuffle(self.regions)
        for region in self.regions:
            for i in range(1, 4):
                url = 'http://sh.58.com/{}/zufang/0/pn{}/?ClickID=2&{}'.format(region, i,random_key_value())
                yield Request(url, callback=self.parse)

    def parse(self, response):
        # 解析区域urls，生成对应url
        xpath = '/html/body/div[3]/div[1]/div[5]/div[2]/ul/li/div/h2/a/@href'
        urls = response.xpath(xpath).extract()
        for url in urls:
            if collection.find_one({'_id': url}):  # 不爬重复数据
                continue
            yield Request(url, callback=self.parse1)

    def parse1(self, response):
        base_xpath = '/html/body/div[4]/div[2]/div[2]/div[1]/div[1]'
        loader = Tc58ItemLoader(item=Tc58Item(), response=response)
        loader.add_xpath('title', '/html/body/div[4]/div[1]/h1/text()')
        loader.add_value('link', response.url)
        loader.add_xpath('price', base_xpath + '/div/span[1]/b/text()')
        loader.add_xpath('estate', base_xpath + '/ul/li[4]/span[2]/a/text()')
        loader.add_xpath('address', base_xpath + '/ul/li[6]/span[2]/text()')
        loader.add_xpath('description', '/html/body/div[4]/div[3]/div[1]/div[1]/ul/li[3]/span[2]//text()')
        loader.add_xpath('date', '/html/body/div[4]/div[1]/p/text()[1]')
        return loader.load_item()


class Tc58RegionSpider(scrapy.Spider):
    # 爬取对应的区域列表
    name = "tc58_regions"
    allowed_domains = ["58.com"]
    start_urls = [
        'http://sh.58.com/pudongxinqu/chuzu/0/'
    ]

    def parse(self, response):
        base_xpath = '/html/body/div[3]/div[1]/div[3]/dl[1]/dd/div/a'

        pinyins = response.xpath(base_xpath + '/@href').extract()
        names = response.xpath(base_xpath + '/text()').extract()

        results = [(u.split('/')[1], t.strip()) for u, t in zip(pinyins, names)]
        with open(region_path, 'w') as f:
            for p, n in results:
                f.writelines(p + ' ' + n + '\n')
