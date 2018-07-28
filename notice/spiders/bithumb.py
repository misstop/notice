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


class BithumbSpider(scrapy.Spider):
    name = 'bithumb.cafe'
    mainUrl = "https://bithumb.cafe"
    url = "https://bithumb.cafe/notice"

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)
        div = soup.find('div', attrs={"id": "primary-fullwidth"})
        url = div.article.div.a.get("href")  # 文章url
        head = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
        html = requests.get(url=url, headers=head, timeout=20)
        soup = BeautifulSoup(html.text, 'html.parser')
        div = soup.find('div', attrs={"id": "primary-left"})
        title = div.h3.get_text().strip()  # 标题
        dateTime = div.find("li", attrs={"class": "posted-date"}).get_text().strip()  # 日期
        content = div.find("div", attrs={"class": "entry-content"}).get_text().strip()  # 内容
        item = SecondBaseNoticeItem()
        item['name'] = 'Bithumb'
        item['resource'] = 'bithumb.cafe'
        item['url'] = url
        item['time'] = dateTime
        item['title'] = title
        item['main'] = content
        yield item