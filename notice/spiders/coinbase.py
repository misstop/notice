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


class CoinbaseSpider(scrapy.Spider):
    name = 'coinbase.com'
    mainUrl = "https://blog.coinbase.com"
    url = "https://blog.coinbase.com/"

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)
        div = soup.find('div', attrs={"class": "u-paddingTop30"})
        url = div.a.get("href")  # 文章url
        dateTime = div.time.get("datetime").strip()  # 日期
        # print(url)
        # https://blog.coinbase.com/announcing-a-new-way-to-spend-your-coinbase-crypto-e-gift-cards-59687ff77c13?source=collection_home---5------0----------------
        html = requests.get(url, verify=False, timeout=20)
        soup = BeautifulSoup(html.text, 'html.parser')
        div = soup.find('div', attrs={"class": "postArticle-content"})
        title = div.h1.get_text().strip()  # 标题
        content = ""
        for c in div.findAll("p", attrs={"class": "graf--p"}):
            content = content + c.get_text().strip()  # 内容
        item = SecondBaseNoticeItem()
        item['name'] = 'Coinbase'
        item['resource'] = 'coinbase.com'
        item['url'] = url
        item['time'] = dateTime
        item['title'] = title
        item['main'] = content
        yield item