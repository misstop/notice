from notice.items import SecondBaseNoticeItem
from pyquery import PyQuery as pq
import scrapy
import time
import json
import pdb
import datetime
import requests
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


class CoinexSpider(scrapy.Spider):
    name = 'hitbtc.com'
    mainUrl = "https://blog.hitbtc.com"
    url = "https://blog.hitbtc.com/"
    Head = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"
    }

    def start_requests(self):
        yield scrapy.Request(url=self.url, headers=self.Head, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)
        article = soup.find('article')
        # print(html.text)
        url = article.h2.a.get("href")  # 文章url
        html = requests.get(url, headers=self.Head, verify=False, timeout=20)
        soup = BeautifulSoup(html.text, 'html.parser')
        article = soup.find('article')
        title = article.h1.get_text().strip()  # 标题
        dateTime = article.time.get_text().strip()  # 日期
        content = article.find("div", attrs={"class": "entry-content"}).get_text().strip()  # 内容
        item = SecondBaseNoticeItem()
        item['name'] = 'Hitbtc'
        item['resource'] = 'hitbtc.com'
        item['url'] = url
        item['time'] = dateTime
        item['title'] = title
        item['main'] = content
        yield item