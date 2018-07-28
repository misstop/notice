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


class DigifinexSpider(scrapy.Spider):
    name = 'digifinex.com'
    mainUrl = "https://www.digifinex.com"
    url = "https://www.digifinex.com/notice"

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        ul = soup.find('ul', attrs={"id": "newList"})
        url = self.mainUrl + ul.li.a.get("href")  # 文章url
        html = requests.get(url, verify=False)
        soup = BeautifulSoup(html.text, 'html.parser')
        div = soup.find('div', attrs={"id": "product"})
        title = div.h2.get_text().strip()  # 标题
        dateTime = div.p.get_text().strip()  # 日期
        content = div.find("div", attrs={"class": "paragraph"}).get_text().strip()
        item = SecondBaseNoticeItem()
        item['name'] = 'Digifinex'
        item['resource'] = 'digifinex.com'
        item['url'] = url
        item['time'] = dateTime
        item['title'] = title
        item['main'] = content
        yield item