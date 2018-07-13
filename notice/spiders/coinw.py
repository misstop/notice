import logging
import re
import datetime
from notice.items import SecondBaseNoticeItem
from pyquery import PyQuery as pq
import scrapy
import time
import json
import requests

class CoinwSpider(scrapy.Spider):
    name = 'coinw.me'
    base_url="https://www.coinw.me"
    notice_url = 'https://www.coinw.me/newService/ourService.html?id=1'

    def start_requests(self, ):
        yield scrapy.Request(url=self.notice_url,
                dont_filter=True,
                callback=self.parse_item)


    def parse_item(self, response):
        doc = pq(response.body.decode('utf8'))
        posts = doc('main div.news-list').items()
        post=list(posts)[0]

        item = SecondBaseNoticeItem()
        item['name'] = 'Coinw'
        item['resource'] = 'coinw.me'

        item['url'] = self.base_url+post('a.link-1').attr('href')

        headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "__cdnuid=f8fb4bffaf1f60209e71c09fe9bcfc55; Hm_lvt_525b7a4b6599566fc46ec53565d28557=1528446808; JSESSIONID=01C71D91925EAF16C954EEBD5764F891; Hm_lpvt_525b7a4b6599566fc46ec53565d28557=1528450115",
            "Host": "www.coinw.me",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        }

        doc_detail=pq(requests.get(item['url'],headers=headers).text)
        item['title'] = doc_detail('.news-title h3').text()
        item['main'] =doc_detail('.news-article').text()
        date = doc_detail('div.news-title.ta-c.mb20 p span').text()
        year, mon, day,hour,mint,second = re.search('(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+)', date).groups()
        item['time'] = "%s-%s-%s %s:%s:%s" % (year, mon, day,hour,mint,second)
        logging.log(logging.DEBUG, '[BITFINE] Get item:', item)
        yield item

