from notice.items import SecondBaseNoticeItem, DayBaseNoticeItem
from pyquery import PyQuery as pq
import scrapy
import time
import json
import pdb
import datetime


def string2datetime(str, format="%Y-%m-%dT%H:%M:%SZ"):
    return datetime.datetime.strptime(str, format)


def utc2local(utc_date):
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    res_time = string2datetime(utc_date) + offset
    print(res_time)
    return res_time


class OkexSpider(scrapy.Spider):
    name = 'fcoin.com'
    base_url = 'https://support.fcoin.com'
    notice_url = 'https://support.fcoin.com/hc/zh-cn/categories/360000333493-%E5%85%AC%E5%91%8A%E4%B8%AD%E5%BF%83'
    start_urls = [
        'https://support.fcoin.com/hc/zh-cn/sections/360000782633-%E6%9C%80%E6%96%B0%E5%85%AC%E5%91%8A',
        'https://support.fcoin.com/hc/zh-cn/sections/360001401593-%E5%88%9B%E4%B8%9A%E6%9D%BF'
    ]
    # def start_requests(self, ):
    #     yield scrapy.Request(url=self.notice_url,
    #                          dont_filter=True,
    #                          callback=self.parse_notice)

    def parse(self, response):
        doc = pq(response.body.decode('utf8'))
        notice = list(doc('.article-list li').items())[0]
        detail_url = notice('a').attr('href')
        notice_detail = pq(self.base_url + detail_url)

        item = DayBaseNoticeItem()
        item['name'] = 'fcoin'
        item['resource'] = 'fcoin.com'
        item['url'] = self.base_url + detail_url
        date = notice_detail('.meta-data time').attr('datetime')

        item['time'] = utc2local(date).strftime("%Y-%m-%d %H:%M:%S")

        item['title'] = notice_detail('.article-title').text().replace('\n', '')
        item['main'] = notice_detail('.article-body').text()
        yield item
