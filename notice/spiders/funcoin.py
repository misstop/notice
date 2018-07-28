from notice.items import SecondBaseNoticeItem
from pyquery import PyQuery as pq
import scrapy
import time
import json
import pdb
import datetime
import requests
import re
from bs4 import BeautifulSoup
from collections import OrderedDict


def string2datetime(str,format="%Y-%m-%dT%H:%M:%SZ"):
    return datetime.datetime.strptime(str,format)


def utc2local(utc_date):
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    res_time = string2datetime(utc_date) + offset
    print(res_time)
    return res_time


class DragonexSpider(scrapy.Spider):
    name = 'funcoin.co'
    mainUrl = "http://server.funcoin.co"
    url = "http://server.funcoin.co/index/init?ids="

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        jsonData = json.loads(response.text)
        jsonData = jsonData['data']['gonggao'][0]
        article_id = jsonData['article_id']
        url = "http://server.funcoin.co/article/detail?article_id=" + str(article_id) + "&language=1"
        html = requests.get(url, verify=False)
        jsonData = json.loads(html.text)
        jsonData = jsonData['data']
        title = jsonData['title']  # 标题
        content = jsonData['content']  # 内容
        p = re.compile('<[^>]+>')  # 去掉标签
        content = p.sub("", content)
        dateTime = jsonData['create_at']
        item = SecondBaseNoticeItem()
        item['name'] = 'Fucoin'
        item['resource'] = 'fucoin.co'
        item['url'] = url
        item['time'] = dateTime
        item['title'] = title
        item['main'] = content
        yield item