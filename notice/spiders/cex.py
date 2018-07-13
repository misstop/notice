import logging
import re
import datetime
from notice.items import SecondBaseNoticeItem
from pyquery import PyQuery as pq
import scrapy
import time
import json
import requests

class CexSpider(scrapy.Spider):
    name = 'cex.plus'
    base_url='http://cex.plus'
    notice_url = 'http://cex.plus/Art/index/id/1.html'

    def start_requests(self, ):

            yield scrapy.Request(url=self.notice_url,
                    dont_filter=True,
                    callback=self.parse_item)


    def parse_item(self, response):
        doc = pq(response.body.decode('utf8'))
        posts = doc('.table').items()
        post=list(posts)[0]
        item = SecondBaseNoticeItem()
        item['name'] = 'CEX.COM'
        item['resource'] = 'cex.plus'

        item['url'] = self.base_url+post('td a.abs-hover').attr('href')

        date = post('.date').text()
        year, mon, day,hour, minit,second= re.search('(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+)', date).groups()
        item['time'] = "%s-%s-%s %s:%s:%s" % (year, mon, day,hour, minit,second)

        doc_detail=pq(requests.get(item['url']).text)
        item['title']=doc_detail('.detail h1').text()
        item['main'] =doc_detail('.txt').text()

        logging.log(logging.DEBUG, '[BITFINE] Get item:', item)
        yield item

