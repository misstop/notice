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
    name = 'dragonex.im'
    mainUrl = "https://a.dragonex.im"
    url = "https://a.dragonex.im/article/getNotice"

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        jsonData = json.loads(response.text)
        jsonData = jsonData['data']['notices'][0]
        url = jsonData['redirect_url']
        # 获取id
        ids = re.findall(r"/article/(.*?)\?", url)
        id = ids[0]
        url = "https://a.dragonex.io/article/getArticle?article_id=" + str(id)
        html = requests.get(url, verify=False)
        jsonData = json.loads(html.text)
        jsonData = jsonData['data']
        title = jsonData['title']  # 标题
        content = jsonData['content']  # 内容
        p = re.compile('<[^>]+>')  # 去掉标签
        content = p.sub("", content)
        timeStamp = jsonData['update_time']  # 日期
        dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
        dateTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
        item = SecondBaseNoticeItem()
        item['name'] = 'Dragonex'
        item['resource'] = 'dragonex.im'
        item['url'] = url
        item['time'] = dateTime
        item['title'] = title
        item['main'] = content
        yield item