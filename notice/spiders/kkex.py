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


class KkexSpider(scrapy.Spider):
    name = 'kkex.com'
    mainUrl = "https://kkex.com"
    url = "https://kkex.com/api/v1/config"

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        jsonData = json.loads(response.text)
        url = jsonData['activities'][0]['url']
        html = requests.get(url, verify=False, timeout=20)
        soup = BeautifulSoup(html.text, 'html.parser')
        # print(soup)
        div = soup.find('div', attrs={"class": "paper"})
        title = div.find("div", attrs={"class": "article__desc"}).get_text().strip()  # 标题
        timeStamp = int(str(jsonData['activities'][0]['timestamp']).split(".")[0])  # 日期
        dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
        dateTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
        content = div.find("article").get_text().strip()  # 内容
        item = SecondBaseNoticeItem()
        item['name'] = 'Kkex'
        item['resource'] = 'kkex.com'
        item['url'] = url
        item['time'] = dateTime
        item['title'] = title
        item['main'] = content
        yield item