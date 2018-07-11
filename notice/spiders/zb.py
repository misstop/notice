import logging
import re
import datetime
from notice.items import SecondBaseNoticeItem
from pyquery import PyQuery as pq
import scrapy
import time
import json
import requests


class ZbSpider(scrapy.Spider):
    name = 'zb.com'
    base_url = "https://www.bitkk.com"
    notice_url = 'https://www.bitkk.com/i/blog'

    def start_requests(self, ):

            yield scrapy.Request(url=self.notice_url,
                                 dont_filter=True,
                                 callback=self.parse_item)


    def parse_item(self, response):
        doc = pq(response.body.decode('utf8'))
        posts = doc('.cbp_tmtimeline li').items()
        post = list(posts)[0]
        item = SecondBaseNoticeItem()
        item['name'] = 'ZB'
        item['resource'] = 'zb.com'

        item['url'] = self.base_url + post('.envor-post header h3 a').attr('href')

        item['title'] = post('.envor-post header h3 a').text()
        headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                   "Accept-Encoding": "gzip, deflate, br",
                   "Accept-Language": "zh-CN,zh;q=0.9",
                   "Connection": "keep-alive",
                   "Host": "www.bitkk.com",
                   "Upgrade-Insecure-Requests": "1",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
                   }
        doc_detail = pq(requests.get(item['url'],headers=headers).text)
        item['main'] = doc_detail('.page-content').text()

        date = doc_detail('p.align-center span').text()
        print(date)
        year, mon, day, hour, minit = re.search(r'(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+)', date).groups()

        item['time'] = "%s-%s-%s %s:%s:00" % (year, mon, day, hour, minit)

        logging.log(logging.DEBUG, '[BITFINE] Get item:', item)
        yield item
