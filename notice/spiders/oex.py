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


class OexSpider(scrapy.Spider):
    name = 'oex.top'
    base_url = 'https://www.oex.top'

    def start_requests(self):
        header = {
            'Cookie': "oex_lan=zh_TW",
            # 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
        }
        yield scrapy.Request(url=self.base_url, headers=header, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find('div', attrs={"id": "indexnewsList"})
        url = self.base_url + div.p.a.get("href")  # 文章url
        html = requests.get(url, verify=False, timeout=20)
        soup = BeautifulSoup(html.text, 'html.parser')
        div = soup.find('div', attrs={"class": "article-leftbg"})
        title = div.h2.get_text().strip()  # 标题
        dateTime = div.find("div", attrs={"class": "article-info"}).span.get_text().strip().split(": ")[1]  # 日期
        content = div.find("div", attrs={"class": "article-content"}).get_text().strip() # 内容
        item = SecondBaseNoticeItem()
        item['name'] = 'Oex'
        item['resource'] = 'oex.top'
        item['url'] = url
        item['time'] = dateTime
        item['title'] = title
        item['main'] = content
        yield item