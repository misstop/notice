import logging
import re
import datetime
from notice.items import DayBaseNoticeItem
from notice.settings import BITFINEX_CYCLE_TIME, CHECK_TIME_THRESHOLD
from pyquery import PyQuery as pq
import scrapy
import time
import json


class BitfinexSpider(scrapy.Spider):
    name = 'bitfinex.com'
    notice_url = 'https://www.bitfinex.com/posts?locale=zh-TW'

    def start_requests(self, ):
        # while True:
            yield scrapy.Request(url=self.notice_url, 
                    dont_filter=True, 
                    callback=self.parse_item)
            # time.sleep(BITFINEX_CYCLE_TIME)
            # time.sleep(3)

    def parse_item(self, response):
        doc = pq(response.body.decode('utf8'))
        post = list(doc('#posts-page .section').items())[0]
        date = post('h5 span').text()
        mon, day, year = re.search('.*?(\d+).*?(\d+).*?(\d+)', date).groups()
        mon = mon if int(mon) > 10 else '0' + mon
        item = DayBaseNoticeItem()
        item['name'] = 'bitfinex'
        item['resource'] = 'bitfinex.com'
        item['title'] = post('h5 a').text()
        item['url'] =  'https://bitfinex.com' + post('h5 a').attr('href')
        item['time'] = '-'.join([year, mon, day])
        item['main'] = post('p').text()
        item['summary'] = item['title'][0:10]
        yield item

