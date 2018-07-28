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
    name = 'coinex.com'
    mainUrl = "https://www.coinex.com"
    url = "https://www.coinex.com/announcement"
    Head = {
        'Accept-Language': 'zh_Hans_CN',
        'timezone': '-8',
    }

    def start_requests(self):
        yield scrapy.Request(url=self.url, headers=self.Head, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)
        a = soup.find('a', attrs={"class": "msgLink"})
        url = self.mainUrl + a.get("href")  # 文章url
        html = requests.get(url, headers=self.Head, verify=False, timeout=20)
        soup = BeautifulSoup(html.text, 'html.parser')
        div = soup.find('div', attrs={"class": "msgContainer"})
        title = div.h3.get_text().strip()  # 标题
        dateTime = div.find("p", attrs={"class": "msgTime"}).get_text().strip()  # 日期
        content = div.find("div", attrs={"class": "via-article"}).get_text().strip()  # 内容
        item = SecondBaseNoticeItem()
        item['name'] = 'Coinex'
        item['resource'] = 'coinex.com'
        item['url'] = url
        item['time'] = dateTime
        item['title'] = title
        item['main'] = content
        yield item