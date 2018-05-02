# -*- coding: utf-8 -*-
# @Time    : 03/04/2018
# @Author  : Luke
#
# import requests
#
# proxies = {"http": "http://localhost:8087", "https": "http://localhost4:8087", }
# res = requests.get("http://ip.myhostadmin.net/", proxies=proxies, verify=False)
# print (res.content)

from fake_useragent import UserAgent
import scrapy


ua = UserAgent(verify_ssl=False)

for i in range(100):
    ua_ = ua.random