import logging
import re
import datetime
from notice.items import DayBaseNoticeItem
from notice.settings import KUCOIN_CYCLE_TIME, CHECK_TIME_THRESHOLD
from pyquery import PyQuery as pq
import scrapy
import time
import json


class KucoinSpider(scrapy.Spider):
    name = 'kucoin.com'
    notice_url = 'https://news.kucoin.com/category/%E5%85%AC%E5%91%8A/'

    def start_requests(self, ):
        # while True:
            yield scrapy.Request(url=self.notice_url,
                    dont_filter=True,
                    callback=self.parse_item)
            # time.sleep(KUCOIN_CYCLE_TIME)
            # time.sleep(1)

    def parse_item(self, response):
        doc = pq(response.body.decode('utf8'))
        posts = doc('#loop-container .type-post').items()
        post=list(posts)[0]

        date = post('article .post-header div span').text()

        year, mon, day = re.search('.*?(\d+).*?(\d+).*?(\d+)', date).groups()

        item = DayBaseNoticeItem()
        item['name']='kucoin'
        item['resource'] = 'kucoin.com'
        item['title'] = post('article .post-header h2 a').text()
        item['url'] =  post('article .post-header h2 a').attr('href')
        item['time'] = "%s-%s-%s"%(year,mon,day)
        item['main'] = post('.post-content').text()
        # 需求是去掉这个Comments closed 暂时去不掉
        # print(type(item['main']))
        # item['main']=re.match(r'(.*?)Comments closed$',item['main']).group(1)
        logging.log(logging.DEBUG, '[BITFINE] Get item:', item)
        yield item

