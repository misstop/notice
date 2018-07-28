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


class AllcoinSpider(scrapy.Spider):
    name = 'bcex.top'
    mainUrl = "https://www.bcex.top"
    url = "https://www.bcex.top/news/"
    UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"

    def start_requests(self):
        header = {
            'Cookie': '',
            'User-Agent': self.UserAgent,
        }
        yield scrapy.Request(url=self.url, headers=header, callback=self.parse)

    def parse(self, response):
        cookie = response.headers['Set-Cookie']
        cookie = str(cookie, encoding="utf-8")
        print(cookie)
        Head = {
            'Cookie': cookie.replace("domain=allcoin.ca,", ""),
            'User-Agent': self.UserAgent,
        }
        html = requests.get(self.url, headers=Head, verify=False)
        soup = BeautifulSoup(html.text, 'html.parser')
        li = soup.find('li', attrs={"class": "hideli"})
        # print(li.get_text())
        # print(li.a.get("href"))
        url = self.mainUrl + li.a.get("href")  # 文章url
        html = requests.get(url, headers=Head, verify=False)
        soup = BeautifulSoup(html.text, 'html.parser')
        div = soup.find('div', attrs={"class": "newsarea_box"})
        title = div.h2.get_text().strip()  # 标题
        dateTime = div.p.get_text().strip()  # 日期
        content = div.find("div", attrs={"class": "paragraph"}).get_text().strip()
        item = SecondBaseNoticeItem()
        item['name'] = 'Bcex'
        item['resource'] = 'bcex.top'
        item['url'] = url
        item['time'] = dateTime
        item['title'] = title
        item['main'] = content
        yield item