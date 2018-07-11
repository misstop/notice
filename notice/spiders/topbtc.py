import logging
import re
import datetime
from notice.items import SecondBaseNoticeItem
from notice.settings import TOPBTC_CYCLE_TIME, CHECK_TIME_THRESHOLD
from pyquery import PyQuery as pq
import scrapy
import time
import json
import requests

class TopbtcSpider(scrapy.Spider):
    name = 'topbtc.com'
    base_url='https://www.topbtc.com'
    notice_url = 'https://www.topbtc.com/home/art/index.html'

    def start_requests(self, ):
        # while True:
            yield scrapy.Request(url=self.notice_url,
                    dont_filter=True,
                    callback=self.parse_item)
            # time.sleep(TOPBTC_CYCLE_TIME)
            # time.sleep(1)

    def parse_item(self, response):
        doc = pq(response.body.decode('utf8'))
        posts = doc('.panel-body .span6 a').items()
        post=list(posts)[0]
        item = SecondBaseNoticeItem()
        item['name'] = 'TOPBTC'
        item['resource'] = 'topbtc.com'

        item['url'] = self.base_url+post.attr('href')

        date = post('#ctime').text()
        year, mon, day= re.search('(\d+).*?(\d+).*?(\d+)', date).groups()
        item['time'] = "%s-%s-%s" % (year, mon, day)
        headers={
            "Accept-Language":"zh-CN,zh;q=0.9"
        }
        doc_detail=pq(requests.get(item['url'],headers=headers).text)
        item['title']=doc_detail('.span12 .panel .panel-heading span').text()
        item['main'] =doc_detail('.newsbody').text()

        logging.log(logging.DEBUG, '[BITFINE] Get item:', item)
        yield item

