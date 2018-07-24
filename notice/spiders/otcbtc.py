import logging
import re
import datetime
from notice.items import SecondBaseNoticeItem
from notice.settings import OTCBTC_CYCLE_TIME, CHECK_TIME_THRESHOLD
from pyquery import PyQuery as pq
import scrapy
import time
import json
import requests

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

class OtcbtcSpider(scrapy.Spider):
    name = 'otcbtc.com'
    base_url="https://support.otcbtc.com"
    notice_url = 'https://support.otcbtc.com/hc/zh-cn/categories/360000039452-%E5%85%AC%E5%91%8A%E4%B8%AD%E5%BF%83'

    def start_requests(self, ):
        # while True:
            # print("yield之前")
            yield scrapy.Request(url=self.notice_url,
                    dont_filter=True,
                    callback=self.parse_item)
            # print("yield之后")
            # time.sleep(OTCBTC_CYCLE_TIME)
            # time.sleep(1)
            # print("sleep之后")

    def parse_item(self, response):
        print("parse_item开始爬")
        doc = pq(response.body.decode('utf8'))
        posts = doc('.article-list').items()
        post=list(posts)[0]
        item = SecondBaseNoticeItem()
        item['name'] = 'OTCBTC'
        item['resource'] = 'otcbtc.com'

        item['url'] = self.base_url+post('li a').attr('href')

        doc_detail=pq(requests.get(item['url']).text)
        item['title']=doc_detail('.article-header h1').text()
        item['main'] =doc_detail('.article-body').text()

        date = doc_detail('.meta-data time').attr('datetime')
        item['time'] = utc2local(date).strftime("%Y-%m-%d %H:%M:%S")

        logging.log(logging.DEBUG, '[BITFINE] Get item:', item)
        print("yield item1之前")
        yield item
        print("yield item1之后")

        doc = pq(response.body.decode('utf8'))
        posts = doc('.article-list').items()
        post = list(posts)[1]
        item = SecondBaseNoticeItem()
        item['name'] = 'OTCBTC'
        item['resource'] = 'otcbtc.com'

        item['url'] = self.base_url + post('li a').attr('href')

        doc_detail = pq(requests.get(item['url']).text)
        item['title'] = doc_detail('.article-header h1').text()
        item['main'] = doc_detail('.article-body').text()

        date = doc_detail('.meta-data time').attr('datetime')
        # year, mon, day, hour, minit,second = re.search('(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+)', date).groups()

        item['time'] = utc2local(date).strftime("%Y-%m-%d %H:%M:%S")

        logging.log(logging.DEBUG, '[BITFINE] Get item:', item)
        print("yield item2之前")
        yield item
        print("yield item2之后")


