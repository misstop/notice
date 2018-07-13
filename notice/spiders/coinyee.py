import logging
import re
import datetime
from notice.items import DayBaseNoticeItem
from pyquery import PyQuery as pq
import scrapy
import time
import json
import requests

class CoinyeeSpider(scrapy.Spider):
    name = 'coinyee.io'
    notice_url = 'http://www.coinyee.io/article/category/1'

    def start_requests(self, ):
            yield scrapy.Request(url=self.notice_url,
                    dont_filter=True,
                    callback=self.parse_item)

    def parse_item(self, response):
        doc = pq(response.body.decode('utf8'))
        posts = doc('.article_list').items()
        post=list(posts)[0]
        item = DayBaseNoticeItem()
        item['name'] = 'coinyee'
        item['resource'] = 'coinyee.io'

        item['url'] = post('li a').attr('href')

        doc_detail = pq(requests.get(item['url']).text)
        item['title'] = doc_detail('.faq_title').text()
        item['main'] = doc_detail('.faq_content').text()

        date = doc_detail('.faq_dateline').text()
        year, mon, day, hour, minit, second = re.search('.*?(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+).*?', date).groups()
        item['time'] = "%s-%s-%s %s:%s:%s" % (year, mon, day, hour, minit, second)

        logging.log(logging.DEBUG, '[BITFINE] Get item:', item)
        yield item
